import sys
import sqlite3
from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView, QDialog
from PyQt5.QtWidgets import QTableWidgetItem, QLCDNumber, QLabel, QWidget
from PyQt5.QtWidgets import QFileDialog, QLineEdit, QListView, QTextEdit
from PyQt5.QtWidgets import QDateEdit, QPushButton, QAction, QColorDialog, QSplashScreen
from PyQt5.QtGui import QPainter, QColor, QPixmap, QMovie
from random import randrange
from PyQt5.QtCore import Qt, QTimer

class GifSplashScreen(QSplashScreen):
    def __init__(self, *args, **kwargs):
        super(GifSplashScreen, self).__init__(*args, **kwargs)
        self.movie = QMovie('loading-1.gif')
        self.movie.frameChanged.connect(self.onFrameChanged)
        self.movie.start()

    def onFrameChanged(self, _):
        self.setPixmap(self.movie.currentPixmap())

    def finish(self, widget):
        self.movie.stop()
        super(GifSplashScreen, self).finish(widget)


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Myproject2.ui', self)
        self.setWindowTitle('Журнал заметок')
        self.pushButton.clicked.connect(self.run)
        self.pushButton_2.clicked.connect(self.close_application)
        self.pushButton_4.clicked.connect(self.story_check)
        self.pushButton_5.clicked.connect(self.files)
        self.pushButton_3.clicked.connect(self.new_text)
        self.pushButton_6.clicked.connect(self.black_color)
        self.pushButton_7.clicked.connect(self.game_play)
        self.pushButton_8.clicked.connect(self.information)
        # Обратите внимание: имя элемента такое же как в QTDesigner

    def information(self):
        self.inf = Information()
        self.inf.show()

    def run(self):
        if self.sender().text() == 'Продолжить':
            self.label_2.setText('Меню')
            self.label_3.setText('Если устали, то можете поиграть')
            self.pushButton_3.setText('Добавить заметку')
            self.pushButton_4.setText('Просмотр истории')
            self.pushButton_5.setText('Файлы')
            self.pushButton_6.setText('Настройки')
            self.pushButton_7.setText('Начать')


    def functions(self):
        if self.sender().text() == 'Добавить заметку':
            self.label_3.setText('Дата')
            self.label_4.setText('Описание')
            self.label_5.setText('Температура')

    def story_check(self):
        self.story = Story()
        self.story.show()

    def inc_click(self):
        self.checkbox3.setCheckState(0)

    def open_second_form(self):
        self.second_form = SecondForm(self, 'dvszdd')
        self.second_form.show()

    def close_application(self):
        self.close = CloseAplication(self, '           Для выхода из приложения нажмите на крестик')
        self.close.show()

    def new_text(self):
        self.new = NewText(self, '')
        self.new.show()

    def black_color(self):
        self.black = BlackColor(self, '')
        self.black.show()

    def game_play(self):
        self.game = SmallGame()
        self.game.show()

    def files(self):
        self.files = Files()
        self.files.show()


class Information(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(710, 260, 630, 500)
        self.setWindowTitle('Информация')

        ## Изображение
        self.pixmap = QPixmap('Яндекс картинка2.jpg')
        # Если картинки нет, то QPixmap будет пустым,
        # а исключения не будет
        self.im = QLabel(self)
        self.im.move(0, -50)
        self.im.resize(800, 600)
        # Отображаем содержимое QPixmap в объекте QLabel
        self.im.setPixmap(self.pixmap)

    def close_all(self):
        self.close()


class Files(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("Myproject2_filewidget.ui", self)
        self.addButton.clicked.connect(self.new_base)
        self.findButton_2.clicked.connect(self.story_check_2)

    def new_base(self):
        self.con = sqlite3.connect("films_db (2).sqlite")
        try:
            id_new = self.id_input_2.text()
            file_name = self.file_input.text()
            if id_new == '' or file_name == '':
                self.error()
            else:
                cur = self.con.cursor()
                cur.execute('''INSERT INTO files(id, files_name) VALUES(?, ?)''', (id_new, file_name)).fetchall()
        except Exception:
            self.not_find()
        self.con.commit()

    def story_check_2(self):
        self.story_2 = StoryFiles()
        self.story_2.show()

    def error(self):
        self.error = Error()
        self.error.show()

    def not_find(self):
        self.not_find = NotFind()
        self.not_find.show()


class StoryFiles(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("delete.ui", self)
        self.con = sqlite3.connect("films_db (2).sqlite")
        self.find_Button.clicked.connect(self.update_files)
        self.tableWidget.itemChanged.connect(self.elem_changed_files)
        self.save_Button.clicked.connect(self.save_files)
        self.allstory_Button.clicked.connect(self.all_story)
        self.dictation = {}
        self.name = None

    def all_story(self):
        self.story_4 = AllStory_2()
        self.story_4.show()

    def update_files(self):
        cur = self.con.cursor()
        # Получили результат запроса, который ввели в текстовое поле
        result = cur.execute("SELECT * FROM files WHERE id=?",
                             (id := self.id_input.text(),)).fetchall()
        # Заполнили размеры таблицы
        self.tableWidget.setRowCount(len(result))
        # Если запись не нашлась, то не будем ничего делать
        if not result:
            self.statusBar().showMessage('Не найдено')
            return
        else:
            self.statusBar().showMessage(f"Нашлась запись с id = {id}")
        self.tableWidget.setColumnCount(len(result[0]))
        self.name = [description[0] for description in cur.description]
        # Заполнили таблицу полученными элементами
        for i, elem in enumerate(result):
            for j, values in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(values)))
        self.dictation = {}

    def elem_changed_files(self, elem):
        # Если значение в ячейке было изменено,
        # то в словарь записывается пара: название поля, новое значение
        self.dictation[self.name[elem.column()]] = elem.text()

    def save_files(self):
        if self.dictation:
            cur = self.con.cursor()
            new = "UPDATE files SET\n"
            new += ", ".join([f"{key}='{self.dictation.get(key)}'"
                              for key in self.dictation.keys()])
            new += "WHERE id = ?"
            print(new)
            cur.execute(new, (self.id_input.text(),))
            self.con.commit()
            self.dictation.clear()


class AllStory_2(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("Myproject2_allstorywidget.ui", self)
        self.find2_Button.clicked.connect(self.update)
        self.dictation = {}
        self.name = None
        self.close_story_btn.clicked.connect(self.close_window)
        self.delete_btn.clicked.connect(self.confirm)

    def confirm(self):
        self.conf = Confirm_2()
        self.conf.show()

    def update(self):
        con = sqlite3.connect("films_db (2).sqlite")
        cur = con.cursor()
        self.tableWidget.verticalScrollBar()
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(['Номер', 'Файл'])
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        count = cur.execute("SELECT * FROM files").fetchall()
        self.tableWidget.setRowCount(len(count))
        flag = 0
        for i in count:
            item_id = QTableWidgetItem(str(i[0]))
            self.tableWidget.setItem(flag, 0, item_id)
            item_time = QTableWidgetItem(str(i[1]))
            self.tableWidget.setItem(flag, 1, item_time)
            flag += 1
        flag = 0
        con.close()

    def close_window(self):
        self.close()

    def delete_1(self):
        self.tableWidget.clear()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(['Номер', 'Файл'])


class AllStory(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("Myproject2_allstorywidget.ui", self)
        self.find2_Button.clicked.connect(self.update)
        self.dictation = {}
        self.name = None
        self.close_story_btn.clicked.connect(self.close_window)
        self.delete_btn.clicked.connect(self.confirm)

    def confirm(self):
        self.conf = Confirm()
        self.conf.show()

    def update(self):
        con = sqlite3.connect("films_db (2).sqlite")
        cur = con.cursor()
        self.tableWidget.verticalScrollBar()
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(['Номер', 'Дата', 'Температура', 'Описание'])
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        count = cur.execute("SELECT * FROM films").fetchall()
        self.tableWidget.setRowCount(len(count))
        flag = 0
        for i in count:
            item_id = QTableWidgetItem(str(i[0]))
            self.tableWidget.setItem(flag, 0, item_id)
            item_time = QTableWidgetItem(str(i[1]))
            self.tableWidget.setItem(flag, 1, item_time)
            item_file = QTableWidgetItem(str(i[2]))
            self.tableWidget.setItem(flag, 2, item_file)
            item_action = QTableWidgetItem(str(i[3]))
            self.tableWidget.setItem(flag, 3, item_action)
            flag += 1
        flag = 0
        con.close()

    def close_window(self):
        self.close()

    def delete_1(self):
        self.tableWidget.clear()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(['Номер', 'Дата', 'Температура', 'Описание'])


class Confirm_2(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("Myproject2_deletewidget.ui", self)
        self.yes_Button.clicked.connect(self.delete)
        self.no_Button.clicked.connect(self.back)

    def delete(self):
        con = sqlite3.connect("films_db (2).sqlite")
        cur = con.cursor()
        cur.execute("""DELETE from files""").fetchall()
        con.commit()
        con.close()

    def back(self):
        self.close()


class Confirm(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("Myproject2_deletewidget.ui", self)
        self.yes_Button.clicked.connect(self.delete)
        self.no_Button.clicked.connect(self.back)

    def delete(self):
        con = sqlite3.connect("films_db (2).sqlite")
        cur = con.cursor()
        cur.execute("""DELETE from films""").fetchall()
        con.commit()
        con.close()

    def back(self):
        self.close()


class Story(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("delete.ui", self)
        self.con = sqlite3.connect("films_db (2).sqlite")
        self.find_Button.clicked.connect(self.update)
        self.tableWidget.itemChanged.connect(self.elem_changed)
        self.save_Button.clicked.connect(self.save)
        self.allstory_Button.clicked.connect(self.all_story)
        self.dictation = {}
        self.name = None

    def all_story(self):
        self.story_3 = AllStory()
        self.story_3.show()

    def update(self):
        cur = self.con.cursor()
        # Получили результат запроса, который ввели в текстовое поле
        result = cur.execute("SELECT * FROM films WHERE id=?",
                             (id := self.id_input.text(),)).fetchall()
        # Заполнили размеры таблицы
        self.tableWidget.setRowCount(len(result))
        # Если запись не нашлась, то не будем ничего делать
        if not result:
            self.statusBar().showMessage('Не найдено')
            return
        else:
            self.statusBar().showMessage(f"Нашлась запись с id = {id}")
        self.tableWidget.setColumnCount(len(result[0]))
        self.name = [description[0] for description in cur.description]
        # Заполнили таблицу полученными элементами
        for i, elem in enumerate(result):
            for j, values in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(values)))
        self.dictation = {}

    def elem_changed(self, elem):
        # Если значение в ячейке было изменено,
        # то в словарь записывается пара: название поля, новое значение
        self.dictation[self.name[elem.column()]] = elem.text()

    def save(self):
        if self.dictation:
            cur = self.con.cursor()
            other = "UPDATE films SET\n"
            other += ", ".join([f"{key}='{self.dictation.get(key)}'"
                              for key in self.dictation.keys()])
            other += "WHERE id = ?"
            print(other)
            cur.execute(other, (self.id_input.text(),))
            self.con.commit()
            self.dictation.clear()



class SecondForm(QWidget):
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)

    def initUI(self, args):
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('Вторая форма')
        self.lbl = QLabel(args[-1], self)
        self.lbl.adjustSize()



class CloseAplication(QWidget):
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)

    def initUI(self, args):
        self.setGeometry(710, 260, 500, 500)
        self.setWindowTitle('   Подтверждение выхода')
        self.lbl = QLabel(args[-1], self)
        self.lbl.adjustSize()



class NewText(QWidget):
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)

    def initUI(self, args):
        self.setGeometry(710, 260, 500, 500)
        self.setWindowTitle(' ')
        self.lbl = QLabel(args[-1], self)
        self.lbl.adjustSize()

        self.data_input = QDateEdit(self)
        self.data_input.move(10, 100)
        self.data_input.resize(90, 30)

        self.temperature_input = QLineEdit(self)
        self.temperature_input.move(10, 180)
        self.temperature_input.resize(90, 30)

        self.information_input = QTextEdit(self)
        self.information_input.move(120, 100)
        self.information_input.resize(350, 210)

        self.id_input = QLineEdit(self)
        self.id_input.move(10, 280)
        self.id_input.resize(90, 30)

        self.label_id = QLabel(self)
        self.label_id.setText("Номер")
        self.label_id.move(10, 240)
        self.label_id.resize(150, 30)

        self.label_data = QLabel(self)
        self.label_data.setText("Дата")
        self.label_data.move(10, 60)
        self.label_data.resize(150, 30)

        self.label_temperature = QLabel(self)
        self.label_temperature.setText("Температура")
        self.label_temperature.move(10, 145)
        self.label_temperature.resize(150, 30)

        self.label_information = QLabel(self)
        self.label_information.setText("Описание")
        self.label_information.move(130, 60)
        self.label_information.resize(150, 30)

        self.btn = QPushButton('Добавить', self)
        self.btn.resize(120, 50)
        self.btn.move(350, 320)
        self.btn.clicked.connect(self.base)

        self.btn_saveoncomp = QPushButton('Сохранить', self)
        self.btn_saveoncomp.resize(120, 50)
        self.btn_saveoncomp.move(350, 400)
        self.btn_saveoncomp.clicked.connect(self.save_file)


        self.btn_calc = QPushButton('Калькулятор', self)
        self.btn_calc.resize(100, 80)
        self.btn_calc.move(10, 320)
        self.btn_calc.clicked.connect(self.calc)

    def save_file(self):
        name = QFileDialog.getSaveFileName(self)[0]
        try:
            f = open(name, 'w')
            text = self.information_input.toPlainText()
            f.write(text)
            f.close()
        except FileNotFoundError:
            print('Файл не найден')

    def calc(self):
        self.calcul = Calcul()
        self.calcul.show()

    def base(self):
        self.con = sqlite3.connect("films_db (2).sqlite")
        try:
            id = self.id_input.text()
            text = self.information_input.toPlainText()
            data = self.data_input.text()
            temperatura = self.temperature_input.text()
            if id == '' or text == '' or data == '' or temperatura == '':
                self.error()
            else:
                cur = self.con.cursor()
                cur.execute('''INSERT INTO films(id, date, temperature, description) VALUES(?, ?, ?, ?)''', (id, data, temperatura, text)).fetchall()
        except Exception:
            self.not_find()
        self.con.commit()

    def error(self):
        self.error = Error()
        self.error.show()

    def not_find(self):
        self.not_find = NotFind()
        self.not_find.show()


class NotFind(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(710, 260, 500, 500)
        self.setWindowTitle('Ошибка')

        self.label_error = QLabel('Заметка с таким номером уже существует', self)
        self.label_error.move(112, 150)
        self.label_error.resize(400, 120)



class NewTextColor(QWidget):
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)

    def initUI(self, args):
        self.setGeometry(710, 260, 500, 500)
        self.setWindowTitle('Другая тема')
        self.lbl_color = QLabel(args[-1], self)
        self.lbl_color.adjustSize()

        self.window_2_color = QListView(self)
        self.window_2_color.move(500, 500)
        self.window_2_color.resize(0, 0)

        self.data_input_color = QDateEdit(self)
        self.data_input_color.move(10, 100)
        self.data_input_color.resize(90, 30)

        self.temperature_input_color = QLineEdit(self)
        self.temperature_input_color.move(10, 180)
        self.temperature_input_color.resize(90, 30)

        self.information_input_color = QTextEdit(self)
        self.information_input_color.move(120, 100)
        self.information_input_color.resize(350, 210)

        self.id_input_color = QLineEdit(self)
        self.id_input_color.move(10, 280)
        self.id_input_color.resize(90, 30)

        self.label_id_color = QLabel(self)
        self.label_id_color.setText("Номер")
        self.label_id_color.move(10, 240)
        self.label_id_color.resize(150, 30)

        self.label_data_color = QLabel(self)
        self.label_data_color.setText("Дата")
        self.label_data_color.move(10, 60)
        self.label_data_color.resize(150, 30)

        self.label_temperature_color = QLabel(self)
        self.label_temperature_color.setText("Температура")
        self.label_temperature_color.move(10, 145)
        self.label_temperature_color.resize(150, 30)

        self.label_information_color = QLabel(self)
        self.label_information_color.setText("Описание")
        self.label_information_color.move(130, 60)
        self.label_information_color.resize(150, 30)

        self.btn_color = QPushButton('Добавить', self)
        self.btn_color.resize(120, 50)
        self.btn_color.move(350, 320)
        self.btn_color.clicked.connect(self.base_color_0)

        self.btn_calc_1 = QPushButton('Калькулятор', self)
        self.btn_calc_1.resize(100, 80)
        self.btn_calc_1.move(10, 320)
        self.btn_calc_1.clicked.connect(self.calc_2)

        self.btn_saveoncomp_color = QPushButton('Сохранить', self)
        self.btn_saveoncomp_color.resize(120, 50)
        self.btn_saveoncomp_color.move(350, 400)
        self.btn_saveoncomp_color.clicked.connect(self.save_file)

    def save_file(self):
        name = QFileDialog.getSaveFileName(self)[0]
        try:
            f = open(name, 'w')
            text = self.information_input_color.toPlainText()
            f.write(text)
            f.close()
        except FileNotFoundError:
            print('Файл не найден')

    def base_color_0(self):
        print(self.temperature_input_color.text())
        if not self.id_input_color.text().isdigit():
            self.error()
        else:
            self.base_color()

    def base_color(self):
        self.con = sqlite3.connect("films_db (2).sqlite")
        try:
            id_2 = self.id_input_color.text()
            text = self.information_input_color.toPlainText()
            data = self.data_input_color.text()
            temperatura = self.temperature_input_color.text()
            if id_2 == '' or text == '' or data == '' or temperatura == '':
                self.error()
            else:
                cur = self.con.cursor()
                cur.execute('''INSERT INTO films(id, date, temperature, description) VALUES(?, ?, ?, ?)''',
                           (id_2, data, temperatura, text))
        except Exception:
            self.not_find_2()
        self.con.commit()

    def error(self):
        self.error_1 = Error()
        self.error_1.show()

    def not_find_2(self):
        self.not_find = NotFind()
        self.not_find.show()

    def calc_2(self):
        self.calcul_2 = Calcul()
        self.calcul_2.show()

class Error(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("Myproject2_errorwidget.ui", self)


class BlackColor(QWidget):
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)

    def initUI(self, args):
        self.setGeometry(710, 260, 500, 500)
        self.setWindowTitle('Другая тема')
        self.lbl2 = QLabel(args[-1], self)
        self.lbl2.adjustSize()

        self.window_2 = QListView(self)
        self.window_2.move(500, 500)
        self.window_2.resize(0, 0)

        self.label_hello = QLabel(self)
        self.label_hello.setText("                Приветствуем вас в нашем приложении!")
        self.label_hello.move(0, 0)
        self.label_hello.resize(500, 30)


        self.btn2 = QPushButton('Продолжить', self)
        self.btn2.resize(400, 30)
        self.btn2.move(0, 30)

        self.btn3 = QPushButton('Отмена', self)
        self.btn3.resize(100, 30)
        self.btn3.move(400, 30) # подключить все кнопки

        self.btn4 = QPushButton('Дабавить заметку', self)
        self.btn4.resize(166, 40)
        self.btn4.move(0, 120)  # подключить все кнопки

        self.btn5 = QPushButton('Просмотр истории', self)
        self.btn5.resize(166, 40)
        self.btn5.move(164, 120)  # подключить все кнопки

        self.btn6 = QPushButton('Файлы', self)
        self.btn6.resize(170, 40)
        self.btn6.move(330, 120)  # подключить все кнопки

        self.btn_color_2 = QPushButton(self)
        self.btn_color_2.resize(500, 340)
        self.btn_color_2.move(0, 160)

        self.btn_color_1 = QPushButton(self)
        self.btn_color_1.resize(500, 60)
        self.btn_color_1.move(0, 60)

        self.btn7 = QPushButton('Мини-игры', self)
        self.btn7.resize(221, 31)
        self.btn7.move(10, 360)

        self.btn8 = QPushButton('Информация', self)
        self.btn8.resize(481, 31)
        self.btn8.move(10, 390)

        self.btn2.clicked.connect(self.run_2)
        self.btn3.clicked.connect(self.close_application_2)
        self.btn4.clicked.connect(self.new_text_2)
        self.btn5.clicked.connect(self.story_check)
        self.btn6.clicked.connect(self.story_check_2)
        self.btn7.clicked.connect(self.game_play2)
        self.btn8.clicked.connect(self.information2)
        global color
        color = QColorDialog.getColor()
        if color.isValid():
            self.btn_color_1.setStyleSheet(
                "background-color: {}".format(color.name()))
            self.btn_color_2.setStyleSheet(
                "background-color: {}".format(color.name()))
            self.label_hello.setStyleSheet(
                "background-color: {}".format(color.name()))
            self.window_2.setStyleSheet(
                "background-color: {}".format(color.name()))

    def information2(self):
        self.inf2 = Information()
        self.inf2.show()

    def game_play2(self):
        self.game2 = SmallGame()
        self.game2.show()

    def run_2(self):
        pass

    def close_application_2(self):
        self.close_2 = CloseAplication_color(self, '')
        self.close_2.show()

    def new_text_2(self):
        self.new2 = NewTextColor(self, '')
        self.new2.show()

    def story_check(self):
        self.story_color = Story()
        self.story_color.show()

    def story_check_2(self):
        self.story_2_color = Files()
        self.story_2_color.show()



class CloseAplication_color(QWidget):
    def __init__(self, *args):
        super().__init__()
        self.initUI(args)

    def initUI(self, args):
        self.setGeometry(710, 260, 500, 500)
        self.setWindowTitle('   Подтверждение выхода')
        self.lbl = QLabel(args[-1], self)
        self.lbl.adjustSize()

        self.label_exit = QLabel(self)
        self.label_exit.setText("                Для выхода из приложения нажмите на крестик")
        self.label_exit.move(0, 0)
        self.label_exit.resize(500, 30)

        self.btn_exit_pass = QPushButton('', self)
        self.btn_exit_pass.resize(500, 470)
        self.btn_exit_pass.move(0, 30)
        if color.isValid():
            self.btn_exit_pass.setStyleSheet(
                "background-color: {}".format(color.name()))
            self.label_exit.setStyleSheet(
                "background-color: {}".format(color.name()))



class SmallGame(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setMouseTracking(True)
        self.coords = []
        self.qp = QPainter()
        self.flag = False
        self.status = None

        self.btn_other = QPushButton('Другая игра', self)
        self.btn_other.resize(500, 60)
        self.btn_other.move(0, 0)
        self.btn_other.clicked.connect(self.other_game)


    def initUI(self):
        self.setGeometry(710, 260, 500, 500)
        self.setWindowTitle('Маленькая игра')

    def other_game(self):
        self.game_2 = SecondGame()
        self.game_2.show()

    def paintEvent(self, event):
        if self.flag:
            self.qp = QPainter()
            self.qp.begin(self)
            self.qp.setBrush(QColor(randrange(0, 255), randrange(0, 255), randrange(0, 255)))
            self.draw()
            self.qp.end()

    def draw(self):
        if self.status == 1:
            a = randrange(100)
            self.qp.drawEllipse(*self.coords, a, a)
        elif self.status == 2:
            b = randrange(100)
            self.qp.drawRect(*self.coords, b, b)
        elif self.status == 3:
            c = randrange(100)
            self.qp.drawTriangle(*self.coords, c, c)

    def mousePressEvent(self, event):
        self.coords = [event.x(), event.y()]
        if (event.button() == Qt.LeftButton):
            self.status = 1
        elif (event.button() == Qt.RightButton):
            self.status = 2
        self.new_draw()

    def keyPressEvent(self, event):
        self.coords = [event.x(), event.y()]
        if event.key() == Qt.Key_Space:
            self.status = 3
        self.new_draw()

    def new_draw(self):
        self.flag = True
        self.update()


class SecondGame(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(710, 260, 500, 500)
        self.setWindowTitle('Координаты')

        self.coords = QLabel(self)
        self.coords.setText("Координаты: None, None")
        self.coords.move(30, 30)

    def mouseMoveEvent(self, event):
        self.coords.setText(f"Координаты: {event.x()}, {event.y()}")


class Calcul(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(210, 370, 500, 200)
        self.setWindowTitle('Миникалькулятор')

        self.label_cal = QLabel(self)
        self.label_cal.setText("Первое число(целое):")
        self.label_cal.move(20, 15)

        self.label_cal = QLabel(self)
        self.label_cal.setText("Второе число(целое):")
        self.label_cal.move(20, 95)

        self.btn_cal = QPushButton('->', self)
        self.btn_cal.move(190, 70)
        self.btn_cal.clicked.connect(self.go)

        self.first_input_cal = QLineEdit(self)
        self.first_input_cal.move(20, 40)

        self.second_input_cal = QLineEdit(self)
        self.second_input_cal.move(20, 120)

        self.summ_lbl_cal = QLabel(self)
        self.summ_lbl_cal.setText("Сумма:")
        self.summ_lbl_cal.move(300, 20)

        self.summ_cal = QLCDNumber(self)
        self.summ_cal.move(410, 20)

        self.ras_lbl_cal = QLabel(self)
        self.ras_lbl_cal.setText("Разность:")
        self.ras_lbl_cal.move(300, 50)

        self.ras_cal = QLCDNumber(self)
        self.ras_cal.move(410, 50)

        self.chas_lbl_cal = QLabel(self)
        self.chas_lbl_cal.setText("Частное:")
        self.chas_lbl_cal.move(300, 110)

        self.chas_cal = QLCDNumber(self)
        self.chas_cal.move(410, 110)

        self.prois_lbl_cal = QLabel(self)
        self.prois_lbl_cal.setText("Произведение:")
        self.prois_lbl_cal.move(300, 80)

        self.prois_cal = QLCDNumber(self)
        self.prois_cal.move(410, 80)

    def go(self):
        a, b = list(map(int, [self.first_input_cal.text(), self.second_input_cal.text()]))
        self.summ_cal.display(a + b)
        self.ras_cal.display(a - b)
        if b != 0:
            self.chas_cal.display(a / b)
        else:
            self.chas_cal.display("Error")
        self.prois_cal.display(a * b)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    splash = GifSplashScreen()
    splash.show()

    def createWindow():
        app.w = MyWidget()
        QTimer.singleShot(1500, lambda: (
            app.w.show(),
            splash.finish(app.w))
                          )
    QTimer.singleShot(1500, createWindow)
    sys.exit(app.exec_())