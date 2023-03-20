import os
from models import BillParseParameters, BillSearchParameters, FileParameters
import constants
from models import InputParameters
from PyQt5.QtCore import QThread
import main
from PyQt5 import QtCore, QtGui, QtWidgets


class MainThread(QThread):
    def __init__(self, input_parameters: InputParameters, window):
        super().__init__()
        self.input_parameters = input_parameters
        self.window = window

    def run(self) -> None:
        main.main(input_parameters=self.input_parameters, window=self.window)
        return


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1100, 830)
        font = QtGui.QFont()
        font.setPointSize(14)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("QGroupBox{border: \"0\"}\n"
"QTextEdit{font: 14pt \"MS Shell Dlg 2\";}\n"
"\n"
"")
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 1100, 830))
        self.tabWidget.setObjectName("tabWidget")
        self.bill_search_parameters_tab = QtWidgets.QWidget()
        self.bill_search_parameters_tab.setObjectName("bill_search_parameters_tab")
        self.bill_search_parameters_groupBox = QtWidgets.QGroupBox(self.bill_search_parameters_tab)
        self.bill_search_parameters_groupBox.setGeometry(QtCore.QRect(150, 35, 780, 280))
        self.bill_search_parameters_groupBox.setStyleSheet("")
        self.bill_search_parameters_groupBox.setTitle("")
        self.bill_search_parameters_groupBox.setObjectName("bill_search_parameters_groupBox")
        self.bill_search_parameters_verticalLayout = QtWidgets.QVBoxLayout(self.bill_search_parameters_groupBox)
        self.bill_search_parameters_verticalLayout.setContentsMargins(11, -1, -1, -1)
        self.bill_search_parameters_verticalLayout.setObjectName("bill_search_parameters_verticalLayout")
        self.session_groupBox = QtWidgets.QGroupBox(self.bill_search_parameters_groupBox)
        self.session_groupBox.setAutoFillBackground(False)
        self.session_groupBox.setTitle("")
        self.session_groupBox.setCheckable(False)
        self.session_groupBox.setObjectName("session_groupBox")
        self.session_label = QtWidgets.QLabel(self.session_groupBox)
        self.session_label.setGeometry(QtCore.QRect(0, 0, 200, 40))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(14)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.session_label.setFont(font)
        self.session_label.setObjectName("session_label")
        self.session_comboBox = QtWidgets.QComboBox(self.session_groupBox)
        self.session_comboBox.setGeometry(QtCore.QRect(310, 0, 200, 40))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.session_comboBox.setFont(font)
        self.session_comboBox.setStyleSheet("font: 14pt \"MS Shell Dlg 2\";")
        self.session_comboBox.setObjectName("session_comboBox")
        self.session_comboBox.addItem("")
        self.session_comboBox.addItem("")
        self.session_comboBox.addItem("")
        self.session_comboBox.addItem("")
        self.session_comboBox.addItem("")
        self.session_comboBox.addItem("")
        self.session_comboBox.addItem("")
        self.session_comboBox.addItem("")
        self.session_comboBox.addItem("")
        self.session_comboBox.addItem("")
        self.bill_search_parameters_verticalLayout.addWidget(self.session_groupBox)
        self.registration_number_groupBox = QtWidgets.QGroupBox(self.bill_search_parameters_groupBox)
        self.registration_number_groupBox.setTabletTracking(False)
        self.registration_number_groupBox.setStyleSheet("")
        self.registration_number_groupBox.setTitle("")
        self.registration_number_groupBox.setCheckable(False)
        self.registration_number_groupBox.setObjectName("registration_number_groupBox")
        self.registration_n_label = QtWidgets.QLabel(self.registration_number_groupBox)
        self.registration_n_label.setGeometry(QtCore.QRect(0, 0, 200, 40))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(14)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.registration_n_label.setFont(font)
        self.registration_n_label.setObjectName("registration_n_label")
        self.registration_number_compare_operation_comboBox = QtWidgets.QComboBox(self.registration_number_groupBox)
        self.registration_number_compare_operation_comboBox.setGeometry(QtCore.QRect(310, 0, 200, 40))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.registration_number_compare_operation_comboBox.setFont(font)
        self.registration_number_compare_operation_comboBox.setStyleSheet("font: 14pt \"MS Shell Dlg 2\";")
        self.registration_number_compare_operation_comboBox.setObjectName("registration_number_compare_operation_comboBox")
        self.registration_number_compare_operation_comboBox.addItem("")
        self.registration_number_compare_operation_comboBox.addItem("")
        self.registration_number_compare_operation_comboBox.addItem("")
        self.registration_number_textEdit = QtWidgets.QTextEdit(self.registration_number_groupBox)
        self.registration_number_textEdit.setGeometry(QtCore.QRect(550, 0, 200, 40))
        self.registration_number_textEdit.setPlaceholderText("")
        self.registration_number_textEdit.setObjectName("registration_number_textEdit")
        self.bill_search_parameters_verticalLayout.addWidget(self.registration_number_groupBox)
        self.registration_date_groupBox = QtWidgets.QGroupBox(self.bill_search_parameters_groupBox)
        self.registration_date_groupBox.setTitle("")
        self.registration_date_groupBox.setObjectName("registration_date_groupBox")
        self.registration_date_label = QtWidgets.QLabel(self.registration_date_groupBox)
        self.registration_date_label.setGeometry(QtCore.QRect(0, 0, 200, 40))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(14)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.registration_date_label.setFont(font)
        self.registration_date_label.setObjectName("registration_date_label")
        self.registration_range_start_dateEdit = QtWidgets.QDateEdit(self.registration_date_groupBox)
        self.registration_range_start_dateEdit.setGeometry(QtCore.QRect(310, 0, 200, 40))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(14)
        self.registration_range_start_dateEdit.setFont(font)
        self.registration_range_start_dateEdit.setDateTime(QtCore.QDateTime(QtCore.QDate(2022, 1, 1), QtCore.QTime(0, 0, 0)))
        self.registration_range_start_dateEdit.setDate(QtCore.QDate(2022, 1, 1))
        self.registration_range_start_dateEdit.setObjectName("registration_range_start_dateEdit")
        self.registration_range_end_dateEdit = QtWidgets.QDateEdit(self.registration_date_groupBox)
        self.registration_range_end_dateEdit.setGeometry(QtCore.QRect(550, 0, 200, 40))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(14)
        self.registration_range_end_dateEdit.setFont(font)
        self.registration_range_end_dateEdit.setDate(QtCore.QDate(2023, 1, 1))
        self.registration_range_end_dateEdit.setObjectName("registration_range_end_dateEdit")
        self.bill_search_parameters_verticalLayout.addWidget(self.registration_date_groupBox)
        self.name_groupBox = QtWidgets.QGroupBox(self.bill_search_parameters_groupBox)
        self.name_groupBox.setTitle("")
        self.name_groupBox.setObjectName("name_groupBox")
        self.name_label = QtWidgets.QLabel(self.name_groupBox)
        self.name_label.setGeometry(QtCore.QRect(0, 0, 270, 40))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(14)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.name_label.setFont(font)
        self.name_label.setObjectName("name_label")
        self.name_textEdit = QtWidgets.QTextEdit(self.name_groupBox)
        self.name_textEdit.setGeometry(QtCore.QRect(310, 0, 440, 40))
        self.name_textEdit.setObjectName("name_textEdit")
        self.bill_search_parameters_verticalLayout.addWidget(self.name_groupBox)
        self.start_parsing_pushButton = QtWidgets.QPushButton(self.bill_search_parameters_tab)
        self.start_parsing_pushButton.setGeometry(QtCore.QRect(350, 550, 431, 71))
        self.start_parsing_pushButton.setStyleSheet("font: 75 14pt \"MS Shell Dlg 2\";")
        self.start_parsing_pushButton.setObjectName("start_parsing_pushButton")
        self.progressBar = QtWidgets.QProgressBar(self.bill_search_parameters_tab)
        self.progressBar.setGeometry(QtCore.QRect(350, 650, 468, 30))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.tabWidget.addTab(self.bill_search_parameters_tab, "")
        self.bill_parse_parameters_tab = QtWidgets.QWidget()
        self.bill_parse_parameters_tab.setEnabled(True)
        self.bill_parse_parameters_tab.setObjectName("bill_parse_parameters_tab")
        self.bill_parse_parameters_groupBox = QtWidgets.QGroupBox(self.bill_parse_parameters_tab)
        self.bill_parse_parameters_groupBox.setGeometry(QtCore.QRect(0, 0, 1090, 800))
        self.bill_parse_parameters_groupBox.setTitle("")
        self.bill_parse_parameters_groupBox.setObjectName("bill_parse_parameters_groupBox")
        self.fields_to_parse_groupBox = QtWidgets.QGroupBox(self.bill_parse_parameters_groupBox)
        self.fields_to_parse_groupBox.setGeometry(QtCore.QRect(0, 0, 230, 40))
        self.fields_to_parse_groupBox.setStyleSheet("QCheckBox{font: 12pt \"MS Shell Dlg 2\";}")
        self.fields_to_parse_groupBox.setTitle("")
        self.fields_to_parse_groupBox.setObjectName("fields_to_parse_groupBox")
        self.fields_to_parse_lable = QtWidgets.QLabel(self.fields_to_parse_groupBox)
        self.fields_to_parse_lable.setGeometry(QtCore.QRect(0, 0, 230, 40))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.fields_to_parse_lable.setFont(font)
        self.fields_to_parse_lable.setStyleSheet("")
        self.fields_to_parse_lable.setObjectName("fields_to_parse_lable")
        self.fields_to_parse_verticalGroupBox = QtWidgets.QGroupBox(self.fields_to_parse_groupBox)
        self.fields_to_parse_verticalGroupBox.setGeometry(QtCore.QRect(0, 0, 0, 0))
        self.fields_to_parse_verticalGroupBox.setObjectName("fields_to_parse_verticalGroupBox")
        self.fields_to_parse_verticalLayout = QtWidgets.QVBoxLayout(self.fields_to_parse_verticalGroupBox)
        self.fields_to_parse_verticalLayout.setObjectName("fields_to_parse_verticalLayout")
        self.file_format_parameters_verticalGroupBox = QtWidgets.QGroupBox(self.bill_parse_parameters_groupBox)
        self.file_format_parameters_verticalGroupBox.setGeometry(QtCore.QRect(300, 670, 550, 60))
        self.file_format_parameters_verticalGroupBox.setStyleSheet("font: 14pt \"MS Shell Dlg 2\";")
        self.file_format_parameters_verticalGroupBox.setTitle("")
        self.file_format_parameters_verticalGroupBox.setObjectName("file_format_parameters_verticalGroupBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.file_format_parameters_verticalGroupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.file_format_label_9 = QtWidgets.QLabel(self.file_format_parameters_verticalGroupBox)
        self.file_format_label_9.setObjectName("file_format_label_9")
        self.horizontalLayout.addWidget(self.file_format_label_9)
        self.xlsx_file_format_radioButton_9 = QtWidgets.QRadioButton(self.file_format_parameters_verticalGroupBox)
        self.xlsx_file_format_radioButton_9.setAutoFillBackground(False)
        self.xlsx_file_format_radioButton_9.setChecked(True)
        self.xlsx_file_format_radioButton_9.setObjectName("xlsx_file_format_radioButton_9")
        self.horizontalLayout.addWidget(self.xlsx_file_format_radioButton_9)
        self.csv_file_format_radioButton_9 = QtWidgets.QRadioButton(self.file_format_parameters_verticalGroupBox)
        self.csv_file_format_radioButton_9.setObjectName("csv_file_format_radioButton_9")
        self.horizontalLayout.addWidget(self.csv_file_format_radioButton_9)
        self.radioButton = QtWidgets.QRadioButton(self.file_format_parameters_verticalGroupBox)
        self.radioButton.setObjectName("radioButton")
        self.horizontalLayout.addWidget(self.radioButton)
        self.directory_verticalGroupBox = QtWidgets.QGroupBox(self.bill_parse_parameters_groupBox)
        self.directory_verticalGroupBox.setGeometry(QtCore.QRect(300, 600, 500, 57))
        self.directory_verticalGroupBox.setTitle("")
        self.directory_verticalGroupBox.setObjectName("directory_verticalGroupBox")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.directory_verticalGroupBox)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.directory_pushButton = QtWidgets.QPushButton(self.directory_verticalGroupBox)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.directory_pushButton.setFont(font)
        self.directory_pushButton.setObjectName("directory_pushButton")
        self.horizontalLayout_2.addWidget(self.directory_pushButton)
        self.directrory_textEdit = QtWidgets.QTextEdit(self.directory_verticalGroupBox)
        self.directrory_textEdit.setObjectName("directrory_textEdit")
        self.horizontalLayout_2.addWidget(self.directrory_textEdit)
        self.tabWidget.addTab(self.bill_parse_parameters_tab, "")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # ----------------------------------------------------------------------------------------------------------------------

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
        fname = str(QtWidgets.QFileDialog.getExistingDirectory(QtWidgets.QFileDialog(), 'Оберіть директорію')).replace('/', '\\')
        self.directrory_textEdit.setText(fname)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Парсер законопроектів"))
        self.session_label.setText(_translate("MainWindow", "<html><head/><body><p>Сесія реєстрації:</p></body></html>"))
        self.session_comboBox.setItemText(0, _translate("MainWindow", "Всі сесії IX скл."))
        self.session_comboBox.setItemText(1, _translate("MainWindow", "IX скл. 9 сесія"))
        self.session_comboBox.setItemText(2, _translate("MainWindow", "IX скл. 8 сесія"))
        self.session_comboBox.setItemText(3, _translate("MainWindow", "IX скл. 7 сесія"))
        self.session_comboBox.setItemText(4, _translate("MainWindow", "IX скл. 6 сесія"))
        self.session_comboBox.setItemText(5, _translate("MainWindow", "IX скл. 5 сесія"))
        self.session_comboBox.setItemText(6, _translate("MainWindow", "IX скл. 4 сесія"))
        self.session_comboBox.setItemText(7, _translate("MainWindow", "IX скл. 3 сесія"))
        self.session_comboBox.setItemText(8, _translate("MainWindow", "IX скл. 2 сесія"))
        self.session_comboBox.setItemText(9, _translate("MainWindow", "IX скл. 1 сесія"))
        self.registration_n_label.setText(_translate("MainWindow", "<html><head/><body><p>№ реєстрації:</p></body></html>"))
        self.registration_number_compare_operation_comboBox.setItemText(0, _translate("MainWindow", "Містить"))
        self.registration_number_compare_operation_comboBox.setItemText(1, _translate("MainWindow", "Дорівнює"))
        self.registration_number_compare_operation_comboBox.setItemText(2, _translate("MainWindow", "Перелік"))
        self.registration_date_label.setText(_translate("MainWindow", "<html><head/><body><p>Дата реєстрації:</p></body></html>"))
        self.name_label.setText(_translate("MainWindow", "<html><head/><body><p>Назва (слова з назви):</p></body></html>"))
        self.start_parsing_pushButton.setText(_translate("MainWindow", "Старт"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.bill_search_parameters_tab), _translate("MainWindow", "Параметри пошуку"))
        self.fields_to_parse_lable.setText(_translate("MainWindow", "Поля для парсингу"))
        self.file_format_label_9.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">Формат:</span></p></body></html>"))
        self.xlsx_file_format_radioButton_9.setText(_translate("MainWindow", "xlsx"))
        self.csv_file_format_radioButton_9.setText(_translate("MainWindow", "csv"))
        self.radioButton.setText(_translate("MainWindow", "json"))
        self.directory_pushButton.setText(_translate("MainWindow", "Директорія"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.bill_parse_parameters_tab), _translate("MainWindow", "Параметри парсингу"))
