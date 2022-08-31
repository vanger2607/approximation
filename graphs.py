from datetime import datetime

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMessageBox, QTableWidget, QTableWidgetItem
from PyQt5.QtWidgets import QPushButton, QApplication, QDialog, QLineEdit, QLabel, QFileDialog, \
    QColorDialog, QInputDialog, QPlainTextEdit
from pyqtgraph import PlotWidget
from pyqtgraph import exporters
from pyqtgraph import mkBrush
from random import randint

import sqlite3
from work_with_csv import graph_log, approximation, evidence
from errors import IncorrectinputError, InquiryError, ColorError, FileNone
from PyQt5 import QtCore, QtWidgets

WHITE = ['#ffffff', '#fefefe', '#fcfcfc', '#fdfdfd', '#fbfbfb', '#fafafa', '#f9f9f9', '#f8f8f8', '#f7f7f7', '#f6f6f6',
         '#f5f5f5', '#f4f4f4', '#f3f3f3', '#f2f2f2', '#f1f1f1', '#f0f0f0', '#efefef', '#eeeeee', '#ededed',
         '#ececec', '#ebebeb', '#eaeaea', '#e9e9e9', '#e8e8e8', '#e7e7e7', '#e6e6e6', '#e5e5e5', '#e4e4e4',
         '#e3e3e3', '#e2e2e2', '#e1e1e1', '#e0e0e0', '#dfdfdf', '#dedede', '#dfdfdf', '#dedede', '#dddddd',
         '#dcdcdc', '#dbdbdb', '#dadada', '#d9d9d9', '#d8d8d8', '#d7d7d7', '#d6d6d6', '#d5d5d5',
         '#d4d4d4', '#d3d3d3', '#d2d2d2', '#d1d1d1', '#d0d0d0', '#cfcfcf', '#cecece', '#cdcdcd', '#cccccc',
         '#cbcbcb', '#cacaca', '#c9c9c9', '#c8c8c8', '#c7c7c7', '#c6c6c6', '#c5c5c5', '#c4c4c4', '#c3c3c3',
         '#c2c2c2', '#c1c1c1', '#c0c0c0', '#bfbfbf', '#bebebe', '#bdbdbd']


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1114, 897)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 327, 253))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.addbutton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.addbutton.setObjectName("addbutton")
        self.verticalLayout.addWidget(self.addbutton)
        self.deletebutton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.deletebutton.setObjectName("deletebutton")
        self.verticalLayout.addWidget(self.deletebutton)
        self.color_change = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.color_change.setObjectName("color_change")
        self.verticalLayout.addWidget(self.color_change)
        self.drawing = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.drawing.setObjectName("drawing")
        self.verticalLayout.addWidget(self.drawing)
        self.drawing_second_file = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.drawing_second_file.setObjectName("drawing_second_file")
        self.verticalLayout.addWidget(self.drawing_second_file)
        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.tablebutton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.tablebutton.setObjectName("tablebutton")
        self.verticalLayout.addWidget(self.tablebutton)
        self.db_button = QtWidgets.QPushButton(self.centralwidget)
        self.db_button.setGeometry(QtCore.QRect(752, 40, 261, 28))
        self.db_button.setObjectName("db_button")
        self.allfiles = QtWidgets.QListWidget(self.centralwidget)
        self.allfiles.setGeometry(QtCore.QRect(195, 261, 601, 361))
        self.allfiles.setObjectName("allfiles")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1114, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.addbutton.setText(_translate("MainWindow", "добавить файл"))
        self.deletebutton.setText(_translate("MainWindow", "удалить файл"))
        self.color_change.setText(_translate("MainWindow", "выбрать цвет для графика"))
        self.drawing.setText(_translate("MainWindow", "нарисовать график"))
        self.drawing_second_file.setText(_translate("MainWindow", "нарисовать логарифмированный график"))
        self.pushButton.setText(_translate("MainWindow", "аппроксимировать выбранный график"))
        self.tablebutton.setText(_translate("MainWindow", "Работа с данными и вывод реузльтата на экран"))
        self.db_button.setText(_translate("MainWindow", "перейти к работе с базой данных"))


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.dct_of_color = {}
        self.setupUi(self)
        self.addbutton.clicked.connect(self.add_file)
        self.deletebutton.clicked.connect(self.delete_file)
        self.drawing.clicked.connect(self.draw_graphic)
        self.drawing_second_file.clicked.connect(self.draw_logging_graph)
        self.lst_of_files = []
        self.pushButton.clicked.connect(self.draw_apro)
        self.color_change.clicked.connect(self.changecol)
        self.db_button.clicked.connect(self.work_with_db)
        self.tablebutton.clicked.connect(self.table_with_info)

    def draw_graphic(self):
        try:
            graph = GraphView()
            assert len(self.lst_of_files) > 0

            for number, file_name in enumerate(self.lst_of_files):
                x, y = evidence(file_name)
                if not (x and y):
                    raise IncorrectinputError
                graph.draw(self.lst_of_files[number], x, y, self.color_for_graph(file_name))
            graph.exec_()
        except AssertionError:
            error = QMessageBox.critical(self, 'ERROR', 'пустой график Вы можете нарисовать сами\n'
                                                        '(добавьте файлы из которых будут взяты точки)')
        except IncorrectinputError:
            error = QMessageBox.critical(self, 'ERROR', 'некорректный файл')

    def draw_logging_graph(self):
        """рисует график у которого элементы начинаются с элемента, который
        равен 0.5+-1 и его индекс больше максимального, x - градусы y - время(прологированное)"""
        try:
            if self.allfiles.currentRow() == -1:
                raise FileNone
            x, y = graph_log(self.lst_of_files[self.allfiles.currentRow()])
            assert x and y

            con = sqlite3.connect('bia.sqlite')
            cur = con.cursor()
            date = datetime.now()
            year = str(date.year)
            month = str(date.month)
            day = str(date.day)
            time = str(date.time())
            time = time[0:5]
            filename = self.allfiles.item(self.allfiles.currentRow()).text()
            if "#" in filename:
                filename = filename[:filename.find("#")]
            filename = filename.strip()
            cur.execute("  INSERT INTO graphs(filename, year, month, day, time,type) "
                        "VALUES(?, ?, ?, ?, ?, ?)",
                        (filename, year, month, day, time, 'логарифмированный'))
            con.commit()
            con.close()
            graph = GraphView()
            graph.draw(self.lst_of_files[self.allfiles.currentRow()], x, y,
                       self.color_for_graph(self.lst_of_files[self.allfiles.currentRow()]))
            graph.exec_()



        except FileNone:
            error = QMessageBox.critical(self, 'ERROR', 'Я верю, Вы сможете тыкнуть на файлик!!!')
        except AssertionError:
            error = QMessageBox.critical(self, 'ERROR', 'некорректный файл')

    def draw_apro(self):
        """рисует аппроксимированный график"""
        try:
            good_size = 5
            if self.allfiles.currentRow() == -1:
                raise FileNone
            file = self.lst_of_files[self.allfiles.currentRow()]
            x, y, coef_a, coef_b, coef_p = approximation(file)  # получаем аппраксимированные точки
            assert x and y and coef_b and coef_a and coef_p
            size, ok_pressed = QInputDialog.getInt(
                self, "Размер точки", "укажите размер точек на графике",
                5, 1, 30, 1)
            if ok_pressed:
                good_size = size

            con = sqlite3.connect('bia.sqlite')
            cur = con.cursor()
            date = datetime.now()
            year = str(date.year)
            month = str(date.month)
            day = str(date.day)
            time = str(date.time())
            time = time[0:5]
            filename = self.allfiles.item(self.allfiles.currentRow()).text()
            if "#" in filename:
                filename = filename[:filename.find("#")]
            filename = filename.strip()
            cur.execute("  INSERT INTO graphs(filename, year, month, day, time,type) "
                        "VALUES(?, ?, ?, ?, ?, ?)",
                        (filename, year, month, day, time, 'аппроксимирующий'))
            con.commit()
            con.close()
            x1, y1 = graph_log(file)  # получаем пролагированные точки
            graph = GraphView()
            graph.draw_2(file, x, y, self.color_for_graph(self.lst_of_files[self.allfiles.currentRow()]),
                         x1, y1, coef_a, coef_b, coef_p, good_size)
            graph.exec_()
        except FileNone:
            error = QMessageBox.critical(self, 'ERROR', 'Собираетесь сделать гениально открытие и спасти мир, \n'
                                                        'но так и не научились выбирать файл?!')
        except AssertionError:
            error = QMessageBox.critical(self, 'ERROR', 'некорректный файл')

    def add_file(self):
        """добавляет файл в список файлов"""
        try:
            fname = QFileDialog.getOpenFileName(self, 'Open file', '', "*.*")
            file_name = str(fname[0])
            assert file_name
            self.lst_of_files.append(file_name)
            self.dct_of_color[file_name] = 0
            file_name = file_name.split('/')[-1]

            self.allfiles.addItem(file_name)
        except AssertionError:
            pass

    def changecol(self):
        """выдает окно с выбором цвета, после чего добавляет в словарь файл: цвет"""
        try:
            if self.allfiles.currentRow() == -1:
                raise FileNone
            color = QColorDialog.getColor()
            name_color = color.name()
            if name_color in WHITE:
                raise AssertionError
            self.dct_of_color[self.lst_of_files[self.allfiles.currentRow()]] = color
            new_item = self.allfiles.item(self.allfiles.currentRow())
            new_item.setText(new_item.text().split(' ')[0] + f' {name_color}')
        except AssertionError:
            error = QMessageBox.critical(self, 'ERROR', 'подбирайте цвета тщательнее, если не хотите разглядывать '
                                                        'белые графики на белом фоне')
        except FileNone:
            error = QMessageBox.critical(self, 'ERROR', 'Сначала нажмите на файл, которому будете менять цвет')

    def color_for_graph(self, file_name: str):
        """проверяет ест ли у графика цвет, если нет, то дает ему случайный"""
        if file_name in self.dct_of_color and self.dct_of_color[file_name] != 0:
            color = self.dct_of_color[file_name]
        else:
            color = (randint(10, 255), randint(0, 255), randint(0, 255))
        return color

    def delete_file(self):
        """удаляет файл из списка файлов"""
        selected_file = self.allfiles.currentRow()

        try:
            assert selected_file > -1
            self.dct_of_color.pop(self.lst_of_files[selected_file])
            self.lst_of_files.pop(selected_file)
            self.allfiles.takeItem(selected_file)

        except KeyError:
            pass
        except IndexError:
            error = QMessageBox.critical(self, 'ERROR', 'Нужен хотя бы один файл, чтобы его удалить')
        except AssertionError:
            error = QMessageBox.critical(self, 'ERROR', 'Выберите файл который хотите удалить')

    def work_with_db(self):
        """Открывает окно с БД в которой ведется лог логарифмирования и аппроксимирования графиков."""
        db_window = DBView()
        db_window.exec_()

    def table_with_info(self):
        try:
            file = self.lst_of_files[self.allfiles.currentRow()]
            table = TableView(file)
            assert evidence(file)  # проверяю корректен ли файл
            table.exec_()
        except IndexError:
            error = QMessageBox.critical(self, 'ERROR', 'Сначала выберите файл')
        except AssertionError:
            error = QMessageBox.critical(self, 'ERROR', 'некорректный файл')


class GraphView(QDialog):
    """класс создающий окно с графиком и кнопкой сохранить файл, важно создать класс, так как метод plot()
    не дает возможности размещения на нем каких-либо виджетов"""

    def __init__(self):
        super(GraphView, self).__init__()
        self.dct_of_color = {
        }
        self.setGeometry(550, 550, 550, 550)
        self.text = QLabel('введите название файла:', self)
        self.text.move(0, 510)
        self.name_file = QLineEdit(self)
        self.name_file.move(200, 510)
        self.save_graph_button = QPushButton('сохранить', self)  # кнопка сохраняющая график в пнг формате в базу данных
        self.save_graph_button.clicked.connect(self.save_graph)
        self.save_graph_button.move(410, 507)
        self.graphWidget = PlotWidget(self, background='w')
        self.graphWidget.resize(500, 500)
        self.graphWidget.addLegend(offset=(310, 22), brush=(mkBrush(128, 128, 128)))

    def draw(self, lst: list, x, y, color):
        """рисует график по названию файла: для легенды графика, - х и у для построения по ним графика"""
        self.graphWidget.plot(x, y, name=lst[lst.index('_') + 1:lst.index('.')], pen=color)

    def draw_2(self, lst: list, x, y, color, x1, y1, coef_a, coef_b, coef_p, size=5):
        """такой же функционал как у первого draw, но еще добавлятся x1 и y1 - прологированные точки,
        которые надо нарисовать вместе с аппроксимированном графиком и  вывести коэфф погрешности"""
        self.setGeometry(700, 730, 700, 730)
        table = QPlainTextEdit(self)
        table.resize(400, 120)
        table.setReadOnly(True)
        table.setPlainText(f'коэфф A = {coef_a} \nкоэфф B = {coef_b}'
                           f'\nкоэфф погрешности = {coef_p}')
        table.move(60, 550, )
        self.graphWidget.plot(x, y, name=lst[lst.index('_') + 1:lst.index('.')], pen=color)
        for i in range(len(x1)):
            self.graphWidget.plot([x1[i]], [y1[i]], symbol='o', symbolSize=size)

    def save_graph(self):
        """сохраняет нарисованный график в компьютер"""
        graph = exporters.ImageExporter(self.graphWidget.plotItem)
        graph.params.param('width').setValue(350, blockSignal=graph.widthChanged)
        graph.params.param('height').setValue(350, blockSignal=graph.heightChanged)
        try:
            assert len(self.name_file.text()) > 0
            assert self.name_file.text().endswith('.png')
            graph.export(self.name_file.text())
            save_ok = QMessageBox()
            save_ok.setIcon(QMessageBox.Information)
            save_ok.setWindowTitle('Сохранение файла')
            save_ok.setText('Файл успешно сохранен')
            save_ok.exec_()
        except AssertionError:
            error = QMessageBox.critical(self, 'ERROR', 'для того, чтобы файл можно было сохранить \n '
                                                        'нужно ввести его название и формат\n'
                                                        '(поддерживается только .png)')


class DBView(QDialog):
    """класс для создания окна, в котором пользователь сможет получать информацию из БД"""

    def __init__(self):
        super(DBView, self).__init__()
        self.setGeometry(800, 650, 800, 650)
        self.connection = sqlite3.connect("bia.sqlite")

        self.instruction = QLabel('Для поиска в БД заполните одну из строк и нажмите на кнопку "начать поиск".\n'
                                  'Данные ищутся по всем заполненным параметрам.\n'
                                  'Время в формате: часы:минуты. Например, 17:45', self)
        self.button_clear = QPushButton('сбросить фильтры', self)
        self.button_clear.clicked.connect(self.filter)
        self.button_clear.move(600, 60)
        self.label_for_year = QLabel('год:', self)
        self.label_for_year.move(0, 50)
        font = self.label_for_year.font()
        font.setPointSize(12)
        self.label_for_year.setFont(font)
        self.year = QLineEdit(self)
        self.year.move(300, 50)
        self.label_for_month = QLabel('месяц:', self)
        self.label_for_month.move(0, 90)
        self.month = QLineEdit(self)
        self.month.move(300, 90)
        self.label_for_month.setFont(font)
        self.label_for_time = QLabel('время:', self)
        self.label_for_time.setFont(font)
        self.label_for_time.move(0, 170)
        self.time = QLineEdit(self)
        self.time.move(300, 170)
        self.label_for_name = QLabel('название файла:', self)
        self.label_for_name.setFont(font)
        self.label_for_name.move(0, 200)
        self.label_for_day = QLabel('день:', self)
        self.label_for_day.setFont(font)
        self.label_for_day.move(0, 130)
        self.day = QLineEdit(self)
        self.found_not = QLabel('ПО ЗАПРОСУ НЕ БЫЛО \nНАЙДЕНО СОВПАДЕНИЙ', self)
        self.found_not.resize(300, 300)
        self.found_not.setStyleSheet("color: red;")
        self.found_not.move(500, 400)
        font.setPointSize(15)
        self.found_not.setFont(font)
        self.day.move(300, 130)
        self.name = QLineEdit(self)
        self.name.move(300, 200)
        self.tableWidget = QTableWidget(self)
        self.tableWidget.resize(500, 300)
        self.tableWidget.move(0, 300)
        self.do_table()
        self.search = QPushButton('начать поиск', self)
        self.search.move(600, 30)
        self.search.clicked.connect(self.sort)

    def do_table(self, query="SELECT * FROM graphs", words=''):
        """делает запрос в БД, получается оттуда данные и выводит их на экран"""
        try:
            res = self.connection.cursor().execute(query, words).fetchall()
            assert res
            self.found_not.hide()
            self.tableWidget.setColumnCount(6)
            self.tableWidget.setHorizontalHeaderLabels(['Название файла', 'Год', 'Месяц', 'День', 'Время', 'Тип'])
            self.tableWidget.setRowCount(0)
            for i, row in enumerate(res):
                self.tableWidget.setRowCount(
                    self.tableWidget.rowCount() + 1)
                for j, elem in enumerate(row):
                    item = QTableWidgetItem(str(elem))
                    item.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.tableWidget.setItem(
                        i, j, item)
            self.tableWidget.resizeColumnsToContents()
        except AssertionError:
            self.found_not.show()

    def sort(self):
        """проверяет какие параметры ввел пользователи и на их основе осуществляет фильтрацию БД(
        делает новый запрос (query) и передает его в do_table())"""
        try:
            year = self.year.text()
            month = self.month.text()
            day = self.day.text()
            time = self.time.text()
            name = self.name.text()
            if not (year or month or day or time or name):
                raise InquiryError
            elif year and not (month or day or time or name):
                query = f'SELECT * FROM graphs WHERE year=?'
                words = (year,)  # переменные которые буду подставлены вместо знаков вопрос при запросе
                self.do_table(query, words)
            elif month and not (year or day or time or name):
                if month.isalpha():
                    query = """SELECT * FROM graphs WHERE month=(SELECT number FROM months WHERE name=?)"""
                elif month.isdigit():
                    query = """SELECT * FROM graphs where month =?"""
                words = (month,)
                self.do_table(query, words)
            elif day and not (year or name or time or month):
                query = """SELECT * FROM graphs WHERE day=?"""
                words = (day,)
                self.do_table(query, words)
            elif time and not (year or month or day or name):
                query = """SELECT * FROM graphs WHERE time=?"""
                words = (time,)
                self.do_table(query, words)
            elif name and not (year or month or day or time):
                query = """SELECT * FROM graphs WHERE filename=?"""
                words = (name,)
                self.do_table(query, words)
            elif year and month and not (day or time or name):
                if month.isdigit():
                    query = f'SELECT * FROM graphs WHERE year=? AND month=?'
                    words = (year, month)
                elif month.isalpha():
                    query = """SELECT * FROM graphs WHERE month=(SELECT number FROM months WHERE name=?)
                    AND year=?"""
                    words = (month, year)
                self.do_table(query, words)
            elif year and day and not (month or time or name):
                query = """SELECT * FROM graphs WHERE year=? AND day=?"""
                words = (year, day)
                self.do_table(query, words)
            elif year and time and not (month or day or name):
                query = """SELECT * FROM graphs WHERE year=? AND time=?"""
                words = (year, time)
                self.do_table(query, words)
            elif year and name and not (time or month or day):
                query = """SELECT * FROM graphs WHERE year=?  AND filename=?"""
                words = (year, name)
                self.do_table(query, words)
            elif month and day and not (year or time or name):
                if month.isalpha():
                    query = """SELECT * FROM graphs WHERE month=(SELECT number FROM months WHERE name=?)
                               AND day=?"""
                elif month.isdigit():
                    query = """SELECT * FROM graphs where month =? AND day=?"""
                words = (month, day)
                self.do_table(query, words)
            elif month and time and not (year or day or name):
                if month.isalpha():
                    query = """SELECT * FROM graphs WHERE month=(SELECT number FROM months WHERE name=?)
                               AND time=?"""
                elif month.isdigit():
                    query = """SELECT * FROM graphs where month =? AND time=?"""
                words = (month, time)
                self.do_table(query, words)
            elif month and name and not (year or day or time):
                if month.isalpha():
                    query = """SELECT * FROM graphs WHERE month=(SELECT number FROM months WHERE name=?)
                               AND filename=?"""
                elif month.isdigit():
                    query = """SELECT * FROM graphs where month =? AND filename=?"""
                words = (month, name)
                self.do_table(query, words)
            elif day and time and not (year or month or name):
                query = """SELECT * FROM graphs WHERE day=? AND time=?"""
                words = (day, time)
                self.do_table(query, words)
            elif day and name and not (year or month or time):
                query = """SELECT * FROM graphs WHERE day=? AND filename=?"""
                words = (day, name)
                self.do_table(query, words)
            elif time and name and not (year or month or day):
                query = """SELECT * FROM graphs WHERE time=? AND filename=?"""
                words = (time, name)
                self.do_table(query, words)
            elif year and month and day and not (time or name):
                if month.isdigit():
                    query = f'SELECT * FROM graphs WHERE year=? AND month=? AND day=?'
                    words = (year, month, day)
                elif month.isalpha():
                    query = """SELECT * FROM graphs WHERE month=(SELECT number FROM months WHERE name=?)
                                   AND year=? AND day=?"""
                    words = (month, year, day)
                self.do_table(query, words)
            elif year and month and time and not (day or name):
                if month.isdigit():
                    query = 'SELECT * FROM graphs WHERE year=? AND month=? AND time=?'
                    words = (year, month, time)
                elif month.isalpha():
                    query = """SELECT * FROM graphs WHERE month=(SELECT number FROM months WHERE name=?)
                                                  AND year=? AND time=?"""
                    words = (month, year, time)
                self.do_table(query, words)
            elif year and day and time and not (month or name):
                query = """SELECT * FROM graphs WHERE year=? AND day=? AND time=?"""
                words = (year, day, time)
                self.do_table(query, words)
            elif year and time and name and not (month or day):
                query = """SELECT * FROM graphs WHERE year=? AND time=? AND filename=?"""
                words = (year, time, name)
                self.do_table(query, words)
            elif month and day and time and not (year or name):
                if month.isalpha():
                    query = """SELECT * FROM graphs WHERE month=(SELECT number FROM months WHERE name=?)
                                   AND day=? AND time=?"""
                elif month.isdigit():
                    query = """SELECT * FROM graphs where month =? AND day=? AND time=?"""
                words = (month, day, time)
                self.do_table(query, words)
            elif year and month and name and not (time or day):
                if month.isalpha():
                    query = """SELECT * FROM graphs WHERE month=(SELECT number FROM months WHERE name=?)
                                   AND year=? AND name=?"""
                elif month.isdigit():
                    query = """SELECT * FROM graphs where month =? AND year=? AND name=?"""
                words = (month, year, name)
                self.do_table(query, words)
            elif year and day and name and not (month or time):
                query = """SELECT * FROM graphs WHERE year=? AND day=? AND filename=?"""
                words = (year, day, name)
                self.do_table(query, words)
            elif month and day and name and not (year or time):
                if month.isalpha():
                    query = """SELECT * FROM graphs WHERE month=(SELECT number FROM months WHERE name=?)
                                                  AND day=? AND name=?"""
                elif month.isdigit():
                    query = """SELECT * FROM graphs where month =? AND day=? AND name=?"""
                words = (month, day, name)
                self.do_table(query, words)
            elif month and time and name and not (year or day):
                if month.isalpha():
                    query = """SELECT * FROM graphs WHERE month=(SELECT number FROM months WHERE name=?)
                                                  AND time=? AND name=?"""
                elif month.isdigit():
                    query = """SELECT * FROM graphs where month =? AND time=? AND name=?"""
                words = (month, time, name)
                self.do_table(query, words)
            elif day and time and name and not (month or year):
                query = """SELECT * FROM graphs WHERE day=? AND time=? AND filename=?"""
                words = (day, time, name)
                self.do_table(query, words)
            elif year and month and day and time and (not name):
                if month.isdigit():
                    query = 'SELECT * FROM graphs WHERE year=? AND month=? AND day=?' \
                            ' AND time=?'
                    self.do_table(query, words=(year, month, day, time))
                elif month.isalpha():
                    query = """SELECT * FROM graphs WHERE month=(SELECT number FROM months WHERE name=?)
                                   AND year=? AND day=? AND time=?"""
                    words = (month, year, day, time)
                    self.do_table(query, words)
            elif year and month and time and name and (not day):
                if month.isdigit():
                    query = 'SELECT * FROM graphs WHERE year=? AND month=? AND time=? AND filename=?'
                    words = (year, month, time, name)
                elif month.isalpha():
                    query = """SELECT * FROM graphs WHERE month=(SELECT number FROM months WHERE name=?)
                                                      AND year=? AND time=? AND name=?"""
                    words = (month, year, time, name)
                self.do_table(query, words)
            elif year and day and time and name and (not month):
                query = """SELECT * FROM graphs WHERE year=? AND day=? AND time=? AND filename=?"""
                words = (year, day, time, name)
                self.do_table(query, words)
            elif year and month and day and name and (not time):
                if month.isdigit():
                    query = 'SELECT * FROM graphs WHERE year=? AND month=? AND day=? AND filename=?'
                    words = (year, month, day, name)
                elif month.isalpha():
                    query = """SELECT * FROM graphs WHERE month=(SELECT number FROM months WHERE name=?)
                                                                     AND year=? AND day=? AND name=?"""
                    words = (month, year, day, name)
                self.do_table(query, words)
            elif month and day and time and name and (not year):
                if month.isalpha():
                    query = """SELECT * FROM graphs WHERE month=(SELECT number FROM months WHERE name=?)
                                                             AND day=? AND time=? AND name=?"""
                elif month.isdigit():
                    query = """SELECT * FROM graphs where month =? AND day=? AND time=? AND name=?"""
                words = (month, day, time, name)
                self.do_table(query, words)
            elif year and month and day and time and name:
                if month.isdigit():
                    query = 'SELECT * FROM graphs WHERE year=? AND month=? AND day=?' \
                            ' AND time=? AND filename=?'
                    words = (year, month, day, time, name)
                elif month.isalpha():
                    query = """SELECT * FROM graphs WHERE month=(SELECT number FROM months WHERE name=?)
                    AND year=? AND day=? AND time=? AND filename=? """
                    words = (month, year, day, time, name)
                self.do_table(query, words)
        except InquiryError:
            error = QMessageBox.critical(self, 'ERROR', 'хотя бы один параметр для фильтрации\n'
                                                        'должен быть введен')

    def filter(self):
        """показывает БД без фильтров"""
        self.month.clear()
        self.year.clear()
        self.day.clear()
        self.time.clear()
        self.name.clear()
        self.do_table()

    def closeEvent(self, event):
        if event:
            self.connection.close()


class TableView(QDialog):
    """выводит на экран данные о графике"""

    def __init__(self, filename):
        super(TableView, self).__init__()
        self.setGeometry(400, 400, 400, 400)
        self.table = QPlainTextEdit(self)
        self.table.move(0, 0)
        self.table.resize(400, 400)
        coef_A = approximation(filename)[2]
        assert coef_A  # если некорректный файл не заходит в setPlainText
        coef_B = approximation(filename)[3]
        coef_P = approximation(filename)[4]
        self.table.setPlainText(f'время жизни в миллисекундах: {1000 / coef_A}\n'
                                f'погрешность : {coef_P}\n'
                                f'коэффициент A: {coef_A}\n'
                                f'коэффициент B : {coef_B}')


if __name__ == "__main__":
    app = QApplication([])
    win = MainWindow()
    win.show()
    app.exec_()
