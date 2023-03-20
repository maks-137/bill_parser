import asyncio

from bs4 import BeautifulSoup
from models import BillCard, BillSearchParameters, BillParseParameters, DocumentsDownloadParameters, BillDocuments, \
    BillItem
from fake_useragent import UserAgent
import aiohttp
from typing import Generator

ua = UserAgent()
headers = {'User-Agent': ua.random}


parse_functions = {
    'text': {
        'parse_number': lambda div: div.text.split('від')[0].strip(),
        'parse_date': lambda div: div.text.split('від')[1].strip(),
        'parse_text': lambda div: div.text.strip(),
        'parse_comma_splited': lambda div: [item.strip() for item in div.text.split(',')],
        'parse_divs': lambda div: [item.text.strip() for item in div.find_all('div')],
        'parse_related_to_work_documents': lambda div:
            [item.find('a').text.strip() for item in div.find_all('div', class_='related-files')],
    },

    'links': {
        'parse_all_a': lambda div: [a for a in div.find_all('a')],
        'parse_related_to_work_documents':
            lambda div: [div.find('a') for div in div.find_all('div', class_='related-files')]
    }
}


field_function_pairs = {
    'text': {
        'registration_number': parse_functions['text']['parse_number'],
        'registration_date':  parse_functions['text']['parse_date'],
        'act_number': parse_functions['text']['parse_number'],
        'act_date': parse_functions['text']['parse_date'],
        'session': parse_functions['text']['parse_text'],
        'rubric': parse_functions['text']['parse_text'],
        'subject_of_law': parse_functions['text']['parse_text'],
        'initiator': parse_functions['text']['parse_comma_splited'],
        'main_committee': parse_functions['text']['parse_text'],
        'other_committees': parse_functions['text']['parse_divs'],
        'governing_documents': parse_functions['text']['parse_divs'],
        'related_to_work_documents': parse_functions['text']['parse_related_to_work_documents'],
    },

    'links': {
        'governing_documents': parse_functions['links']['parse_all_a'],
        'related_to_work_documents': parse_functions['links']['parse_related_to_work_documents']
    }
}


async def _create_iter_tasks(search_parameters: BillSearchParameters, parse_parameters: BillParseParameters,
                              download_parameters: DocumentsDownloadParameters) \
                        -> tuple[Generator[BillCard, None, None], Generator[BillDocuments, None, None]]:

    async with aiohttp.ClientSession() as session:
        response = await session.post(
            url='https://itd.rada.gov.ua/billInfo/Bills/searchResults',
            data=search_parameters.get_in_payload_format(),
            headers=headers
        )

        response_text = await response.text()
        soup = BeautifulSoup(response_text, 'lxml')
        page_number = soup.find('div', class_='pagination').find_all('button')[-2].text.strip()

        bill_items = []
        for n in range(1, int(page_number)-160):
            search_parameters = BillSearchParameters(**search_parameters.__dict__)
            search_parameters.page = n
            items = await _create_parse_tasks(1, session, search_parameters, parse_parameters, download_parameters)
            bill_items += items

        bill_cards = (item.card for item in bill_items if item.card.registration_number)
        bill_documents = (item.documents for item in bill_items if item.card.registration_number)

        return bill_cards, bill_documents


async def _create_parse_tasks(request_count, session, search_parameters: BillSearchParameters, parse_parameters: BillParseParameters,
                              download_parameters: DocumentsDownloadParameters) \
                        -> list[BillItem]:

    request_parameters = {'url': 'https://itd.rada.gov.ua/billInfo/Bills/searchResults',
                          'data': search_parameters.get_in_payload_format(),
                          'headers': headers
                          }

    async with session.post(**request_parameters) as response:
        print('sreq')
        if response.status != 200:
            if request_count == 3:
                return []
            await asyncio.sleep(5)
            r = await _create_parse_tasks(request_count+1, session, search_parameters, parse_parameters,
                                          download_parameters)
            return r

        response_text = await response.text()
        soup = BeautifulSoup(response_text, 'lxml')
        bills_urls = [item['href'] for item in soup.find_all('a', class_='link-blue')]

        parse_tasks = []
        for url in bills_urls:
            task = asyncio.create_task(_parse_data(1, session, url, download_parameters, parse_parameters))
            parse_tasks.append(task)

        bill_items = await asyncio.gather(*parse_tasks)

        return list(bill_items)


async def _parse_data(request_count, session, url, download_parameters, parse_parameters) -> BillItem:
    async with session.get(url=url, headers=headers) as response:
        print('creq')
        if response.status != 200:
            if request_count == 3:
                print('bad')
                print(response.url)
                return BillItem()
            await asyncio.sleep(3)
            r = await _parse_data(request_count+1, session, url, download_parameters, parse_parameters)
            return r

        response_text = await response.text()
        soup = BeautifulSoup(response_text, 'lxml')
        try:
            card = _parse_bill_card(soup, parse_parameters)
        except IndexError:
            return BillItem()

        documents = _parse_documents(soup, download_parameters)

        return BillItem(card=card, documents=documents)


def _parse_documents(soup: BeautifulSoup, download_parameters: DocumentsDownloadParameters) -> BillDocuments:
    info_divs = [div.find_all('div')[1] for div in soup.find_all('div', class_='row')[-3:-1]]
    registration_number = parse_functions['text']['parse_number'](soup.find('div', class_='row').find_all('div')[1])
    links = dict()
    for div, (key, flag) in zip(info_divs, download_parameters.__dict__.items()):
        if flag:
            a_elements = field_function_pairs['links'][key](div)
            item = {}
            for a in a_elements:
                doc_name = a.text.strip()

                if doc_name in item.keys():
                    for i in range(1, len(a_elements)+1):
                        if (alt_name := f"{doc_name}({i})") not in item.keys():
                            doc_name = alt_name
                            break

                item[doc_name] = f"https://itd.rada.gov.ua/{a.get('href')}"

            links[key] = item

    return BillDocuments(registration_number, **links)


def _parse_bill_card(soup: BeautifulSoup, parse_parameters: BillParseParameters) -> BillCard:
    info_divs = [div.find_all('div')[1] for div in soup.find_all('div', class_='row')[:-1]]
    info_divs.insert(1, info_divs[0])

    if len(info_divs) == 12:
        del info_divs[4]
        info_divs.insert(3, info_divs[2])

    elif len(info_divs) == 11:
        if len(info_divs[2].text.split('від')) == 1:
            del info_divs[3]
        else:
            info_divs.insert(3, info_divs[2])

    if len(info_divs) == 10:
        info_divs.insert(2, False)
        info_divs.insert(3, False)

    bill_info = {}
    for div, (key, flag) in zip(info_divs, parse_parameters.__dict__.items()):
        if flag and div:
            bill_info[key] = field_function_pairs['text'][key](div)

    return BillCard(**bill_info)


def run(search_parameters: BillSearchParameters, parse_parameters: BillParseParameters,
        download_parameters: DocumentsDownloadParameters)\
        -> tuple[Generator[BillCard, None, None], Generator[BillDocuments, None, None]]:

    loop = asyncio.get_event_loop()
    bill_cards, bill_documents = loop.run_until_complete(_create_iter_tasks(search_parameters, parse_parameters, download_parameters))

    return bill_cards, bill_documents

# run(search_parameters=BillSearchParameters(), parse_parameters=BillParseParameters(), download_parameters=DocumentsDownloadParameters())

