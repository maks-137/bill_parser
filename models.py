from dataclasses import dataclass
from constants import PAYLOAD_KEYWORDS, PAYLOAD_FIELDS
from typing import NamedTuple


@dataclass
class DocumentsDownloadParameters:
    governing_documents: bool = True
    related_to_work_documents: bool = True


class BillDocuments(NamedTuple):
    registration_number: str = ''
    governing_documents: dict[str, str] = {}
    related_to_work_documents: dict[str, str] = {}


@dataclass
class BillParseParameters:
    registration_number: bool = True
    registration_date: bool = True
    act_number: bool = True
    act_date: bool = True
    session: bool = True
    rubric: bool = True
    subject_of_law: bool = True
    initiator: bool = True
    main_committee: bool = True
    other_committees: bool = True
    governing_documents: bool = True
    related_to_work_documents: bool = True


class BillCard(NamedTuple):
    registration_number: str = ''
    registration_date: str = ''
    act_number: str = ''
    act_date: str = ''
    session: str = ''
    rubric: str = ''
    subject_of_law: str = ''
    initiator: list[str] = []
    main_committee: str = ''
    other_committees: list[str] = []
    governing_documents: list[str] = []
    related_to_work_documents: list[str] = []


@dataclass
class BillSearchParameters:
    session: str = 'Всі сесії IX скл.'
    registration_number_compare_operation: str = 'Містить'
    registration_number: str = ''
    registration_range_start: str = ''
    registration_range_end: str = ''
    name: str = ''
    detail_view: bool = False
    page: int = 1
    per_page: int = 50

    def get_in_payload_format(self):
        data = {}
        for k, v in zip(PAYLOAD_FIELDS, self.__dict__.values()):
            if k in PAYLOAD_KEYWORDS:
                data[k] = PAYLOAD_KEYWORDS[k][v]
            else:
                data[k] = v

        return data


class BillItem(NamedTuple):
    card: BillCard = BillCard()
    documents: BillDocuments = BillDocuments()


@dataclass
class FileParameters:
    file_format: str = ''
    dir: str = ''


@dataclass
class InputParameters:
    search_parameters: BillSearchParameters
    parse_parameters: BillParseParameters
    file_parameters: FileParameters
    download_parameters: DocumentsDownloadParameters

