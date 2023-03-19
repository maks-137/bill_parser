import time

import requests
from bs4 import BeautifulSoup
from models import BillCard, BillSearchParameters, BillParseParameters, DocumentsDownloadParameters, BillDocuments,\
    BillItem
from fake_useragent import UserAgent


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


def run(search_parameters: BillSearchParameters, parse_parameters: BillParseParameters,
        download_parameters: DocumentsDownloadParameters) -> list[BillItem]:
    ua = UserAgent()
    response = requests.post(
        url='https://itd.rada.gov.ua/billInfo/Bills/searchResults',
        data=search_parameters.get_in_payload_format(),
        headers={'User-Agent': ua.random}
    )

    soup = BeautifulSoup(response.text, 'lxml')
    links_to_bills = (item['href'] for item in soup.find_all('a', class_='link-blue'))
    bill_items = []
    for link in links_to_bills:
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'lxml')
        card = _parse_bill_card(soup, parse_parameters)
        documents = _parse_documents(soup, download_parameters)

        bill_items.append(BillItem(card=card, documents=documents))

    for item in bill_items:
        print(item)


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


run(search_parameters=BillSearchParameters(), parse_parameters=BillParseParameters(), download_parameters=DocumentsDownloadParameters())
