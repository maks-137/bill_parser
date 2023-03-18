import os

import requests
from models import BillDocuments, DocumentsDownloadParameters
from typing import Generator


def download_documents(documents: Generator[BillDocuments, None, None],
                       download_parameters: DocumentsDownloadParameters, path: str) -> None:

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
                document = requests.get(link, stream=True)
                doc_type = doc_types[document.headers['Content-Type']]
                with open(fr"{full_dir}\{name}.{doc_type}", 'wb',) as file:
                    for chunk in document.iter_content():
                        file.write(chunk)

                print(name)

                break

            break

        break


# documents = (i for i in [BillDocumentsModel(registration_number='0142',
#     governing_documents={'doc': 'https://itd.rada.gov.ua/billInfo/Bills/pubFile/24770'},
#     related_to_work_documents={})])
#
# download_parameters = BillDownloadModel(governing_documents=True, related_to_work_documents=True)
#
# download_documents(documents=documents, download_parameters=download_parameters)


