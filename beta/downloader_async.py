import asyncio
import os
import time

import requests
from models import BillDocuments, DocumentsDownloadParameters
from typing import Generator
import aiohttp

from fake_useragent import UserAgent

ua = UserAgent()



async def download_documents(documents: Generator[BillDocuments, None, None],
                       download_parameters: DocumentsDownloadParameters, path: str) -> None:
    tasks = []

    doc_types = {
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'docx',
        'application/pdf': 'pdf',
    }

    rubric_dir_names = {
        'governing_documents': 'Текст законопроекту та супровідні документи',
        'related_to_work_documents': "Документи, пов'язані із роботою",
    }

    if not download_parameters.governing_documents and not download_parameters.related_to_work_documents:
        return

    for key, flag, in download_parameters.__dict__.items():
        if not flag:
            del rubric_dir_names[key]

    for item in documents:

        for doc_rubric, dir_name in rubric_dir_names.items():
            full_dir = fr"{path}\{item.registration_number}\{dir_name}"
            if not os.path.exists(os.path.join(os.getcwd(), full_dir)):
                os.makedirs(full_dir)

            for name, link in item._asdict()[doc_rubric].items():
                task = asyncio.create_task(download(url=link, full_dir=full_dir, name=name))
                tasks.append(task)

    await asyncio.gather(*tasks)


async def download(url, full_dir, name):

    doc_types = {
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'docx',
        'application/pdf': 'pdf',
        'text/html': 'docx',
    }

    async with aiohttp.ClientSession() as session:
        response = await session.get(url=url, headers={'User-agent': ua.random})

        if response.status != 200:
            print('invalid request (file)')

        doc_type = doc_types[response.headers['Content-Type']]
        with open(fr"{full_dir}\{name}.{doc_type}", 'wb', ) as file:
            while True:
                chunk = await response.content.read()
                if not chunk:
                    break
                file.write(chunk)

        print(name)


def run(documents, download_parameters, path):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        download_documents(documents=documents, download_parameters=download_parameters, path=path))








#
# documents = (i for i in [BillDocuments(registration_number='0142',
#                                        governing_documents={
#                                            'Проект Закону (24.01.2022)': 'https://itd.rada.gov.ua/billInfo/Bills/pubFile/1182227',
#                                            'Фінансово-економічне обгрунтування (24.01.2022)': 'https://itd.rada.gov.ua/billInfo/Bills/pubFile/1182222',
#                                            'Пояснювальна записка (24.01.2022)': 'https://itd.rada.gov.ua/billInfo/Bills/pubFile/1182226',
#                                            'Подання (24.01.2022)': 'https://itd.rada.gov.ua/billInfo/Bills/pubFile/1182224',
#                                            'Проект Постанови до Закону (іншого Акта) (24.01.2022)': 'https://itd.rada.gov.ua/billInfo/Bills/pubFile/1182225',
#                                            'Текст міжнародного договору (24.01.2022)': 'https://itd.rada.gov.ua/billInfo/Bills/pubFile/1182223',
#                                        },
#                                        related_to_work_documents={})])
#
# download_parameters = DocumentsDownloadParameters(governing_documents=True, related_to_work_documents=True)
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(
#     download_documents(documents=documents, download_parameters=download_parameters, path=r'E:\Python\bill_parser'))