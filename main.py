from pipeline import BillParserPipeline
import bill_parser
from PyQt5.QtWidgets import QApplication
import sys
from models import InputParameters
import main_window
import qt_app
from PyQt5.QtWidgets import QMainWindow


def main(input_parameters: InputParameters, window) -> None:
    try:
        serch_parameters = input_parameters.search_parameters
        parse_parameters = input_parameters.parse_parameters
        file_parameters = input_parameters.file_parameters

        bill_cards = bill_parser.run(serch_parameters, parse_parameters, window)

        pipeline = BillParserPipeline(
            bill_cards=bill_cards,
            parse_parameters=parse_parameters,
            file_format=file_parameters.file_format,
            path=file_parameters.dir
        )
        pipeline.save_bill_cards()
    except Exception as ex:
        print(ex)


if __name__ == '__main__':
    # app = QApplication(sys.argv)
    # window = main_window.UI()
    # window.show()
    # app.exec_()

    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = qt_app.Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


