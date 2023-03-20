import os
import time

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow
from models import BillParseParameters, BillSearchParameters, FileParameters
import constants
from models import InputParameters
from PyQt5.QtCore import QThread
import main


class MainThread(QThread):
    def __init__(self, input_parameters: InputParameters, window):
        super().__init__()
        self.input_parameters = input_parameters
        self.window = window

    def run(self) -> None:
        main.main(input_parameters=self.input_parameters, window=self.window)
        return


class UI(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi("qt_app.ui", self)

        # fields_to_parse_groupBox and fields_to_parse_verticalGroupBox filling
        for (name, text, y) in zip(BillParseParameters.__annotations__.keys(), constants.TABLE_FIELDS,
                                   range(40, 40*len(constants.TABLE_FIELDS)+40, 40)):
            name = f'{name}_checkBox'
            self.__dict__[name] = QtWidgets.QCheckBox(self.fields_to_parse_verticalGroupBox)
            self.__dict__[name].setObjectName(name)
            self.__dict__[name].setChecked(True)
            self.__dict__[name].setText(text)
            self.fields_to_parse_verticalLayout.addWidget(self.__dict__[name])

        self.fields_to_parse_groupBox.setGeometry(30, 15, 550,
                                                  len(self.fields_to_parse_verticalGroupBox.children())*40+40)
        self.fields_to_parse_verticalGroupBox.setGeometry(0, 40, 550,
                                                          len(self.fields_to_parse_verticalGroupBox.children())*40)

        # set default text to directrory_textEdit
        self.directrory_textEdit.setText(os.getcwd())

        # directory_pushButton connection
        self.directory_pushButton.clicked.connect(self._show_dir_dialog)

        # start_parsing_pushButton connection
        self.start_parsing_pushButton.clicked.connect(self._grab_input_parameters)

        # progress_bar
        self.pbar_max_value = 1
        self.progressBar.setMinimum(0)

    def set_progress_bar(self, max_value):
        self.progressBar.setValue(0)
        self.pbar_max_value = max_value
        self.progressBar.setMaximum(max_value)

    def triger_progress_bar(self):
        value = int(self.progressBar.value())
        self.progressBar.setValue(value + 1)

    def _grab_input_parameters(self) -> None:

        input_parameters = InputParameters(
            search_parameters=self._grab_search_parameters(),
            parse_parameters=self._grab_parse_parameters(),
            file_parameters=self._grab_file_parameters(),
        )

        self.main_thread_instanc = MainThread(input_parameters, window=self)
        self.main_thread_instanc.start()

    def _grab_file_parameters(self) -> FileParameters:
        file_parameters = FileParameters()
        for field in self.file_format_parameters_verticalGroupBox.children()[2:]:
            if field.isChecked():
                file_parameters.file_format = field.text()

        file_parameters.dir = self.directrory_textEdit.toPlainText()
        return file_parameters

    def _grab_parse_parameters(self) -> BillParseParameters:
        parse_parameters = BillParseParameters()
        for field, key in zip(self.fields_to_parse_verticalGroupBox.children()[1:],
                              BillParseParameters.__annotations__.keys()):
            if not field.isChecked():
                parse_parameters.__dict__[key] = False

        return parse_parameters

    def _grab_search_parameters(self) -> BillSearchParameters:
        grab_functions = {
            'QComboBox': lambda cb: cb.currentText(),
            'QDateEdit': lambda de: str(de.date().toPyDate()),
            'QTextEdit': lambda te: te.toPlainText(),
        }

        search_parameters = BillSearchParameters()
        for group in self.bill_search_parameters_groupBox.findChildren(QtWidgets.QGroupBox):
            for item in group.children():
                if (class_name := item.__class__.__name__) in grab_functions.keys():
                    value = grab_functions[class_name](item)
                else:
                    continue

                key = '_'.join(item.objectName().split('_')[:-1])
                search_parameters.__dict__[key] = value

        return search_parameters

    def _show_dir_dialog(self):
        fname = str(QtWidgets.QFileDialog.getExistingDirectory(self, 'Оберіть директорію')).replace('/', '\\')
        self.directrory_textEdit.setText(fname)
