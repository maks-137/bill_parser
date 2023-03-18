import asyncio
import sys
import time

import aiohttp
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
from models import BillSearchParameters

ua = UserAgent()


async def parse_data(session, url):
    async with session.get(url, headers={'User-Agent': ua.random}) as response:
        response_text = await response.text()
        soup = BeautifulSoup(response_text, 'lxml')
        if response.status != 200:
            await asyncio.sleep(1)
            await parse_data(session=session, url=url)


async def create_tasks(search_parameters):
    async with aiohttp.ClientSession() as session:
        response = await session.post(
            url='https://itd.rada.gov.ua/billInfo/Bills/searchResults',
            data=search_parameters.get_in_payload_format(),
            headers={'User-Agent': ua.random}
        )

        response_text = await response.text()
        soup = BeautifulSoup(response_text, 'lxml')
        links_to_bills = (item['href'] for item in soup.find_all('a', class_='link-blue'))
        tasks = []
        for link in links_to_bills:
            task = asyncio.create_task(parse_data(session=session, url=link))
            tasks.append(task)

        r = await asyncio.gather(*tasks)


loop = asyncio.get_event_loop()
start = time.time()
loop.run_until_complete(create_tasks(search_parameters=BillSearchParameters()))
print(time.time() - start)

