import csv
import json

from openpyxl import Workbook
import constants
from typing import Generator
from models import BillCard, BillParseParameters


class BillParserPipeline:
    def __init__(self, bill_cards: Generator[BillCard, None, None], parse_parameters: BillParseParameters,
                 file_format: str, path: str):
        self.bill_cards = bill_cards
        self.parse_parameters = parse_parameters.__dict__.values()
        self.file_format = file_format
        self.path = path
        self.file_name = 'result'

    def save_bill_cards(self) -> None:
        filtered_bill_cards = self._filter_bills()
        filtered_table_fields = [field for field, flag in zip(constants.TABLE_FIELDS, self.parse_parameters) if flag]

        save_functions = {
            'xlsx': '_save_bill_cards_as_xlsx',
            'csv': '_save_bill_cards_as_csv',
            'json': '_save_bill_cards_as_json'
        }

        BillParserPipeline.__dict__[save_functions[self.file_format]](
            self=self,
            bill_cards=filtered_bill_cards,
            table_fields=filtered_table_fields
        )

    def _save_bill_cards_as_xlsx(self, bill_cards: Generator[Generator, None, None], table_fields: Generator)\
            -> None:
        wb = Workbook()
        ws = wb.active
        ws.append(table_fields)

        for bill_card in bill_cards:
            bill_card = (', '.join(value) if isinstance(value, list) else value for value in bill_card)
            ws.append(bill_card)

        wb.save(fr'{self.path}\{self.file_name}.xlsx')

    def _save_bill_cards_as_csv(self, bill_cards: Generator[Generator, None, None], table_fields: Generator)\
            -> None:
        file = open(fr'{self.path}\{self.file_name}.csv', 'w', encoding='utf-8')
        writer = csv.writer(file)
        writer.writerow(table_fields)

        for bill_card in bill_cards:
            bill_card = (', '.join(value) if isinstance(value, list) else value for value in bill_card)
            writer.writerow(bill_card)

    def _save_bill_cards_as_json(self, bill_cards: Generator[Generator, None, None], table_fields: Generator)\
            -> None:
        items = []
        for bill_card in bill_cards:
            item = {}
            for field, value in zip(table_fields, bill_card):
                item[field] = value
            items.append(item)

        with open(fr'{self.path}\{self.file_name}.json', 'w', encoding='utf-8') as file:
            json.dump(items, file, ensure_ascii=False)

    def _filter_bills(self) -> Generator[Generator, None, None]:
        for bill_card in self.bill_cards:

            filtered_bill_card = (value for value, flag in zip(bill_card, self.parse_parameters) if flag)
            yield filtered_bill_card
