from pipeline import BillParserPipeline
import bill_parser
from PyQt5.QtWidgets import QApplication
import sys
import main_window
from models import InputParameters
import downloader


def main(input_parameters: InputParameters) -> None:
    try:
        serch_parameters = input_parameters.search_parameters
        parse_parameters = input_parameters.parse_parameters
        download_parameters = input_parameters.download_parameters
        file_parameters = input_parameters.file_parameters

        bill_items = bill_parser.run(serch_parameters, parse_parameters, download_parameters)
        bill_cards = (item.card for item in bill_items)
        bill_documents = (item.documents for item in bill_items)

        del bill_items

        pipeline = BillParserPipeline(
            bill_cards=bill_cards,
            parse_parameters=parse_parameters,
            file_format=file_parameters.file_format,
            path=file_parameters.dir
        )
        pipeline.save_bill_cards()

        downloader.download_documents(documents=bill_documents, download_parameters=download_parameters,
                                      path=file_parameters.dir)

        print('FINISH')

    except Exception as ex:
        print(ex)
        return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = main_window.UI()
    window.show()
    app.exec_()
