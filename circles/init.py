import sys
import sip
from PIL import Image, ImageDraw, ImageFont
import logging
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, pyqtSlot, QEvent

from circles.utils.utils import *
from circles.db.db import *

logging.basicConfig(
    format='[%(filename)s:%(lineno)s - %(funcName)20s()]%(levelname)s:%(name)s:%(message)s',
    level=logging.INFO
)

user_information = {'success': False, 'payload': {}}


class Main(QWidget):

    def __init__(self):
        super().__init__()

        # Background RGB
        self.backgroundRad = 255
        self.backgroundGreen = 255  # 181
        self.backgroundBlue = 255  # 100
        # link clicked
        self.link_clicked = False
        # Start
        logging.info('Start Welcome window')
        self.initUI()

    def initUI(self):
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(self.backgroundRad, self.backgroundGreen, self.backgroundBlue))
        self.setPalette(p)
        logging.info(f'Set background rgb{self.backgroundRad, self.backgroundGreen, self.backgroundBlue}')

        self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.welcome_window()

        # TODO Redesign the app
        # TODO Create a design for other windows

        self.adjustSize()
        self.setGeometry(self.frameGeometry())
        self.move(150, 150)
        self.setWindowTitle('Euler circles')
        self.show()

    def welcome_window(self):
        grid = QGridLayout()
        grid.setSpacing(20)

        photo = QLabel(self)
        namePhoto = 'photo/MainWindowCircles.png'
        pixmap = QPixmap(namePhoto)
        pixmap2 = pixmap.scaled(550, 550, Qt.KeepAspectRatio)
        photo.setPixmap(pixmap2)
        logging.info(f"Add photo '{namePhoto}' in welcome window")

        buttons = QHBoxLayout()
        buttons.setSpacing(20)
        nameBattons = ['Зарегистрироваться', 'Войти', 'Пропустить']
        for name in nameBattons:
            btn = QPushButton(name, self)
            btn.setStyleSheet("background-color: rgb(223, 209, 21)")
            btn.clicked.connect(self.welcome_button_click)
            buttons.addWidget(btn, 0, Qt.AlignCenter)
        #buttons.setAlignment(Qt.AlignTop)

        info = QGridLayout()
        info.setSpacing(10)
        infoTxt = ['Здравствуй!',
                   'Это приложение содержит материал\nдля проверки ваших умений решать\nзадачи с применением кругов Эйлера',
                   'Войдите в свой аккаунт, или зарегистрируйте новый']

        positions = [(i, j) for i in range(3) for j in range(1)]

        fonts = [
            [QFontDatabase.addApplicationFont('fonts/Montserrat-Medium.ttf'), "Montserrat Medium"],
            [QFontDatabase.addApplicationFont('fonts/Montserrat-Bold.ttf'), "Montserrat Bold"]
        ]
        logging.info(f'Set fonts in app: {fonts}')
        #font, ok = QFontDialog.getFont()
        #if ok: print(font.toString())

        buttons_block = QVBoxLayout()
        buttons_block.setSpacing(10)

        for position, name in zip(positions, infoTxt):

            label = QLabel(name, self)
            label.setAlignment(Qt.AlignCenter)
            font = QFont()

            if position[0] == 0:
                font.setFamily("Montserrat Bold")
                font.setPointSize(24)
                font.setBold(True)
                label.setFont(font)
                info.addWidget(label, *position)
            elif position[0] == 1:
                font.setFamily("Montserrat Medium")
                font.setPointSize(18)
                label.setFont(font)
                info.addWidget(label, *position)
            else:
                label.setAlignment(Qt.AlignCenter)
                font.setFamily("Montserrat Medium")
                font.setPointSize(12)
                label.setFont(font)
                buttons_block.addWidget(label)

        buttons_block.addLayout(buttons)
        info.addLayout(buttons_block, 3, 0)
        grid.addWidget(photo, 0, 0)
        grid.addItem(info, 0, 1)

        if self.layout() is not None:
            self.delete_items_of_layout(self.layout())
            sip.delete(self.layout())

        logging.info('Set layout in welcome window')
        self.setLayout(grid)

    @pyqtSlot()
    def welcome_button_click(self):
        sender = self.sender()
        logging.info(f"The '{sender.text()}' button was pressed")
        if sender.text() == 'Войти':
            self.login()
        elif sender.text() == 'Зарегистрироваться':
            self.sign_up()
        else:
            self.menu()

    def sign_up(self):
        self.delete_items_of_layout(self.layout())
        sip.delete(self.layout())

        logging.info('Sign up window started')
        self.init_sign()
        self.adjustSize()
        self.setGeometry(450, 300, 500, 300)
        self.setWindowTitle('Sign in')
        self.show()

    def init_sign(self):
        titel = QLabel('Пожалуйста, введите свои данные:')
        name = QLabel('Имя')
        surname = QLabel('Фамилия')
        email = QLabel('Email')
        password = QLabel('Пароль( > 6 символов)')
        repeatPassword = QLabel('Повторите пароль')

        titel.setAlignment(Qt.AlignCenter)
        titel.setFont(QFont("Montserrat Bold", 18))
        name.setFont(QFont('Montserrat Medium'))
        surname.setFont(QFont('Montserrat Medium'))
        email.setFont(QFont('Montserrat Medium'))
        password.setFont(QFont('Montserrat Medium'))
        repeatPassword.setFont(QFont('Montserrat Medium'))

        self.nameRegistrationEdit = QLineEdit(self)
        self.surnameRegistrationEdit = QLineEdit(self)
        self.emailRegistrationEdit = QLineEdit(self)
        self.passwordRegistrationEdit = QLineEdit(self)
        self.passwordRegistrationEdit.setEchoMode(QLineEdit.Password)
        self.repeatPasswordRegistrationEdit = QLineEdit(self)
        self.repeatPasswordRegistrationEdit.setEchoMode(QLineEdit.Password)

        self.checkBox = QCheckBox('Даю согласие на обработку персональных данных', self)
        cancelButton = QPushButton('Отмена', self)
        continueButton = QPushButton('Продолжить', self)

        cancelButton.clicked.connect(self.sign_up_button_click)
        continueButton.clicked.connect(self.sign_up_button_click)

        info = [
            [titel],
            [name, self.nameRegistrationEdit],
            [surname, self.surnameRegistrationEdit],
            [email, self.emailRegistrationEdit],
            [password, self.passwordRegistrationEdit],
            [repeatPassword, self.repeatPasswordRegistrationEdit],
            [self.checkBox],
            [cancelButton, continueButton]
        ]

        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        for item in info:
            hbox = QHBoxLayout()
            hbox.setSpacing(20)
            for value in item:
                hbox.addWidget(value)
            layout.addLayout(hbox)

        logging.info('Set layout in sign up')
        self.setLayout(layout)

    @pyqtSlot()
    def sign_up_button_click(self):
        sender = self.sender()
        logging.info(f"The '{sender.text()}' button was pressed")
        if sender.text() == 'Отмена':
            self.initUI()
        else:
            logging.info('Data checking')
            alph = 'абвгдеёжзийклмнопрстуфхцчшщыьъэюя'
            error_status = False
            if self.nameRegistrationEdit.text() == '' or self.surnameRegistrationEdit.text() == '' or self.emailRegistrationEdit.text() == '':
                self.on_error('Пожалуйста, заполните все поля')
                return
            for letter in self.nameRegistrationEdit.text().lower():
                if letter not in alph:
                    self.on_error('Имя должно состоять только из букв Российского алфавита')
                    self.nameRegistrationEdit.setStyleSheet("background-color: rgb(255, 50, 50)")
                    error_status = True

            for letter in self.surnameRegistrationEdit.text().lower():
                if letter not in alph:
                    self.on_error('Фамилия должна состоять только из букв Российского алфавита')
                    self.surnameRegistrationEdit.setStyleSheet("background-color: rgb(255, 50, 50)")
                    error_status = True
            try:
                if is_registered_email(self.emailRegistrationEdit.text()):
                    self.on_error('Ваш адрес электронной почты уже зарегистрирован')
                    self.emailRegistrationEdit.setStyleSheet("background-color: rgb(255, 50, 50)")
                    error_status = True
            except Exception as e:
                self.on_exception(e)

            if '@' not in self.emailRegistrationEdit.text() or '.' not in self.emailRegistrationEdit.text():
                self.on_error('Пожалуйста, указывайте ваш действительный почтовый адрес')
                self.emailRegistrationEdit.setStyleSheet("background-color: rgb(255, 50, 50)")
                error_status = True

            if len(self.passwordRegistrationEdit.text()) < 6:
                self.on_error('Ваш пароль слишком короткий!')
                self.passwordRegistrationEdit.setStyleSheet("background-color: rgb(255, 50, 50)")
                error_status = True

            if self.passwordRegistrationEdit.text() != self.repeatPasswordRegistrationEdit.text():
                self.on_error('Пароли не совпадают!')
                self.repeatPasswordRegistrationEdit.setStyleSheet("background-color: rgb(255, 50, 50)")
                error_status = True

            if not self.checkBox.isChecked():
                self.on_error('Пожалуйста, примите соглашение на обработку персональных данных')
                return
            # If there was a error
            if error_status:
                self.passwordRegistrationEdit.clear()
                self.repeatPasswordRegistrationEdit.clear()
                return

            self.delete_items_of_layout(self.layout())

            try:
                waitMessage = QLabel('Пожалуйста, подождите немного, идёт загрузка данных', self)
                waitMessage.setAlignment(Qt.AlignCenter)
                waitMessage.setFont(QFont("Montserrat Bold", 20))
                self.layout().addWidget(waitMessage)
                logging.info('Set data in database')
                user_information['payload'] = add_user(name=self.nameRegistrationEdit.text(),
                                                       surname=self.surnameRegistrationEdit.text(),
                                                       email=self.emailRegistrationEdit.text(),
                                                       password=self.passwordRegistrationEdit.text())
                user_information['success'] = True
                self.menu()

            except Exception as e:
                self.on_exception(e)

    @pyqtSlot()
    def error_button(self):
        self.__init__()

    def login(self):
        self.delete_items_of_layout(self.layout())
        sip.delete(self.layout())

        logging.info('Login window started')
        self.init_login()
        self.adjustSize()
        self.setGeometry(450, 300, 500, 300)
        self.setWindowTitle('Login')
        self.show()

    def init_login(self):
        titel = QLabel('Введите свой email и пароль,\n чтобы войти в аккаунт')
        email = QLabel('Email')
        password = QLabel('Пароль')

        titel.setAlignment(Qt.AlignCenter)
        fontTitel = QFont("Montserrat Medium", 20)
        fontTitel.setBold(True)
        titel.setFont(fontTitel)
        email.setFont(QFont('Montserrat Medium'))
        password.setFont(QFont('Montserrat Medium'))

        self.emailLoginEdit = QLineEdit(self)
        self.passwordLoginEdit = QLineEdit(self)
        self.passwordLoginEdit.setEchoMode(QLineEdit.Password)

        cancelButton = QPushButton('Отмена', self)
        continueButton = QPushButton('Продолжить', self)

        cancelButton.clicked.connect(self.login_button_click)
        continueButton.clicked.connect(self.login_button_click)

        info = [
            [titel],
            [email, self.emailLoginEdit],
            [password, self.passwordLoginEdit],
            [cancelButton, continueButton]
        ]

        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        for item in info:
            hbox = QHBoxLayout()
            hbox.setSpacing(20)
            for value in item:
                hbox.addWidget(value)
            layout.addLayout(hbox)

        logging.info('Set layout in login')
        self.setLayout(layout)

    @pyqtSlot()
    def login_button_click(self):
        sender = self.sender()
        logging.info(f"The '{sender.text()}' button was pressed")
        if sender.text() == 'Отмена':
            self.initUI()
        else:
            if self.emailLoginEdit.text() == '' or self.passwordLoginEdit.text() == '':
                self.on_error('Все поля, должны быть заполнены!')
                return

            logging.info('Check user info')
            try:
                status = check_user(self.emailLoginEdit.text(), self.passwordLoginEdit.text())
                logging.info('Check status - ' + str(bool(status)))
                if status is not None:
                    user_information['success'] = True
                    user_information['payload'] = status
                    self.menu()
                else:
                    self.on_error('Неверный логин и/или пароль!')
                    self.passwordLoginEdit.clear()
                    return
            except Exception as e:
                self.on_exception(e)

    def menu(self):
        self.delete_items_of_layout(self.layout())
        sip.delete(self.layout())

        logging.info('Menu window started')
        self.init_menu()

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(self.backgroundRad, self.backgroundGreen, self.backgroundBlue))
        self.setPalette(p)
        logging.info(f'Set background rgb{self.backgroundRad, self.backgroundGreen, self.backgroundBlue}')

        self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.adjustSize()
        self.setGeometry(300, 200, 600, 300)
        self.setWindowTitle('Menu')
        self.show()

    def init_menu(self):
        user_status_seperator = QLabel(' | ')
        if user_information['success']:
            info = user_information['payload']
            user_status_sign = QLabel("Вход выполнен:")
            user_status_name = QLabel(info['name'] + ' ' + info['surname'])
            user_status_email = QLabel(info['email'])

            user_status_name.setStyleSheet("text-decoration: underline; color: blue;")
            user_status_email.setStyleSheet("text-decoration: underline; color: blue;")
            user_status_name.mousePressEvent = self.closeEvent
            user_status_email.mousePressEvent = self.closeEvent
            user_status = [user_status_sign, user_status_name, user_status_seperator, user_status_email]

        else:
            user_status_sign = QLabel('Зарегистрироваться')
            user_status_login = QLabel('Войти')
            user_status_sign.setStyleSheet("text-decoration: underline; color: blue;")
            user_status_login.setStyleSheet("text-decoration: underline; color: blue;")
            user_status_sign.mousePressEvent = self.mouse_press_event_sign_up
            user_status_login.mousePressEvent = self.mouse_press_event_login
            user_status = [user_status_sign, user_status_seperator, user_status_login]

        user_profile = QHBoxLayout()
        user_profile.setSpacing(10)
        user_profile.addStretch(1)
        for item in user_status:
            item.setFont(QFont('Montserrat Medium', 12))
            item.adjustSize()
            user_profile.addWidget(item)
        user_profile.sizeHint()


        teacher_option = QLabel('Для решения варианта учителя,\nвведите номер варианта')
        create_option = QLabel('Вы можете создать свой вариант')
        auth_tests = QLabel('Или выберете нужный класс для\nтренеровки решения задач')

        for item in [teacher_option, create_option, auth_tests]:
            item.setFont(QFont('Montserrat Medium', 16))
            item.setAlignment(Qt.AlignTop)
        create_option.setAlignment(Qt.AlignCenter)

        self.teacher_option_edit = QLineEdit(self)
        teacher_option_ok_button = QPushButton('ОК', self)
        teacher_option_ok_button.setStyleSheet("background-color: rgb(223, 209, 21)")
        teacher_option_ok_button.adjustSize()
        teacher_option_widgets = QHBoxLayout()
        teacher_option_widgets.addWidget(self.teacher_option_edit)
        teacher_option_widgets.addWidget(teacher_option_ok_button)

        create_option_button = QPushButton('Создать', self)
        create_option_button.setStyleSheet("background-color: rgb(223, 209, 21)")
        create_option_button.clicked.connect(self.create_teacher_option)
        topics_for_6_7_classes = QPushButton('6-7 класс', self)
        topics_for_8_9_classes = QPushButton('8-9 класс', self)
        topics_for_10_11_classes = QPushButton('10-11 класс', self)

        for item in [topics_for_6_7_classes, topics_for_8_9_classes, topics_for_10_11_classes]:
            item.setStyleSheet("background-color: rgb(223, 209, 21)")
            item.clicked.connect(self.topics_button_click)

        info = [
            [
                [user_profile]
            ],
            [
                [teacher_option, teacher_option_widgets],
                [auth_tests]
            ],
            [
                [create_option, create_option_button],
                [topics_for_6_7_classes, topics_for_8_9_classes, topics_for_10_11_classes]
            ]
        ]

        layout = QVBoxLayout(self)

        for items in info:
            hbox = QHBoxLayout()
            hbox.setSpacing(40)
            for item in items:
                vbox = QVBoxLayout()
                vbox.setSpacing(20)
                for val in item:
                    if val.isWidgetType():
                        vbox.addWidget(val)
                    else:
                        vbox.addLayout(val)
                hbox.addLayout(vbox)

            layout.addLayout(hbox)

        logging.info('Sey layout in menu')
        self.setLayout(layout)

    def mouse_press_event_sign_up(self, event):
        self.sign_up()

    def mouse_press_event_login(self, event):
        self.login()

    def create_teacher_option(self):
        pass

    def topics_button_click(self):
        sender = self.sender()
        logging.info(f"The '{sender.text()}' button was pressed")
        self.class_of_tasks = sender.text()
        self.topics_window()

    def topics_window(self):
        self.delete_items_of_layout(self.layout())
        sip.delete(self.layout())

        logging.info('Topics window started')
        self.init_topics()

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(self.backgroundRad, self.backgroundGreen, self.backgroundBlue))
        self.setPalette(p)
        logging.info(f'Set background rgb{self.backgroundRad, self.backgroundGreen, self.backgroundBlue}')

        self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.adjustSize()
        self.setGeometry(300, 200, 600, 300)
        self.setWindowTitle('Tests')
        self.show()

    def init_topics(self):
        self.number_of_task = 1
        self.right_tasks = 0
        self.already_been = []
        self.new_task()

    def new_task(self):
        self.user_can_ask_a_question = True

        grid = QGridLayout()

        titel = QLabel(f'Задача №{str(self.number_of_task)}')
        fontTitel = QFont("Montserrat Medium", 20)
        fontTitel.setBold(True)
        titel.setFont(fontTitel)
        titel.setAlignment(Qt.AlignCenter)

        if self.layout() is not None:
            procent_of_rigth = QLabel(f'Верно решёных - {str(self.right_tasks*100 // (self.number_of_task - 1))} %')
            procent_of_rigth.setFont(QFont("Montserrat Medium", 14))

        if self.class_of_tasks == '8-9 класс':
            task = Tests9Class(self.number_of_task, self.already_been)
            if task.return_task['success']:
                self.info = task.return_task['payload']
                logging.info('Task Info: ' +
                             str(self.info['options']) + ' ' +
                             str(self.info['question']) + ' ' +
                             str(self.info['answer']))

                text_task = self.get_text_task_8_9_class()

            self.answer_edit = QLineEdit()
            self.answer_edit.setPlaceholderText('Введите сюда ваш ответ (только число)')
        else:
            task = Tests10Class(number_of_task=self.number_of_task % 9, already_been=self.already_been)
            if task.return_task['success']:
                self.info = task.return_task['payload']
                logging.info('Task Info: ' +
                             str(self.info['request']) + ' ' +
                             str(self.info['find']) + ' ' +
                             str(self.info['question']) + ' ' +
                             str(self.info['answer']))

                text_task = self.get_text_task_10_11_class()

            self.answer_edit = QLineEdit()
            self.answer_edit.setPlaceholderText('Введите сюда ваш ответ (только число)')

        buttos = QHBoxLayout()
        buttos.setSpacing(10)
        buttos.addStretch(1)
        continue_button = QPushButton('Далее')
        continue_button.setStyleSheet("background-color: rgb(63, 137, 255)")
        if self.class_of_tasks == '8-9 класс':
            continue_button.clicked.connect(self.answer_task_10)
        else:
            continue_button.clicked.connect(self.answer_task_10)
        exit_button = QPushButton('Завершить')
        exit_button.setStyleSheet("background-color: rgb(244, 29, 29)")
        exit_button.clicked.connect(self.exit_button_click)
        buttos.addWidget(exit_button)
        buttos.addWidget(continue_button)

        grid.addWidget(titel, 0, 0)

        grid.addLayout(text_task, 1, 0)
        grid.addWidget(self.overlay_photo('new', None), 1, 1)
        grid.addWidget(self.answer_edit, 2, 0)
        grid.addLayout(buttos, 2, 1)

        if self.layout() is not None:
            grid.addWidget(procent_of_rigth, 0, 1)
            self.delete_items_of_layout(self.layout())
            sip.delete(self.layout())

        logging.info('Set layout in task')
        self.setLayout(grid)

    def get_text_task_8_9_class(self):
        text_task = QVBoxLayout()
        #text_task.addStretch(1)
        titel_request = QLabel('Запросы к поисковому серверу')
        titel_request.setFont(QFont('Montserrat Medium', 16))
        titel_request.setAlignment(Qt.AlignCenter)
        text_task.addWidget(titel_request)
        for letter, request in self.info['request'].items():
            request_text, request_number = request.split(';')
            line = QLabel(letter + ': ' + request_text)
            line.setFont(QFont('Montserrat Medium', 14))
            line.setFrameStyle(QFrame.Box)
            text_task.addWidget(line)

        text_question = self.info['question']
        question = QLabel(f"Напишите буквы в порядке {text_question}\nколичества страниц, найденых сервером.")
        question.setFont(QFont('Montserrat Medium', 14))
        question.setAlignment(Qt.AlignCenter)
        text_task.addWidget(question)

        return text_task

    def get_text_task_10_11_class(self):
        text_task = QGridLayout()
        titel_find = QLabel('Найдено страниц')
        titel_request = QLabel('Запрос')
        for item in [titel_request, titel_find]:
            item.setFont(QFont('Montserrat Medium', 14))
            item.setFrameStyle(QFrame.Box)
        text_task.addWidget(titel_request, 0, 0)
        text_task.addWidget(titel_find, 0, 1)
        row = 1
        for request, find in zip(self.info['request'], self.info['find']):
            position = 0
            for item in [QLabel(request), QLabel(str(find))]:
                item.setFont(QFont('Montserrat Medium', 14))
                item.setFrameStyle(QFrame.Box)
                text_task.addWidget(item, row, position)

                position += 1
            row += 1

        text_question, self.number_question = (self.info['question'].split(';'))
        question = QLabel(f"Найти: {text_question}")
        question.setFont(QFont('Montserrat Medium', 14))
        question.setAlignment(Qt.AlignCenter)
        text_task.addWidget(question, row, 0)

        return text_task

    def answer_task_10(self):
        if self.answer_edit.text() == '':
            self.on_error('Введите ответ на задачу!')
            return

        grid = QGridLayout()

        try:
            if int(self.answer_edit.text()) == self.info['answer']:
                logging.info('Right answer')
                titel = QLabel('Верный ответ!')
                titel.setStyleSheet("color: green")
                self.right_tasks += 1
            else:
                logging.info('Wrong answer')
                titel = QLabel('Неправильный ответ!')
                titel.setStyleSheet("color: red")
            fontTitel = QFont("Montserrat Medium", 20)
            fontTitel.setBold(True)
            titel.setFont(fontTitel)
            titel.setAlignment(Qt.AlignCenter)
        except ValueError:
            self.on_error('В ответе должно содержаться одно число -\nколичество страниц найденых по запросу')
            return

        decision_status = QVBoxLayout()
        decision_status.setSpacing(1)
        decision_status.addStretch(1)
        procent_of_right = self.right_tasks*100 // self.number_of_task
        procent = QLabel(f'Верно решёных - {str(procent_of_right)} %')
        procent.setFont(QFont("Montserrat Medium", 14))
        result = QLabel('Оптимальный результат - более 90 %')
        result.setFont(QFont("Montserrat Medium", 14))
        if procent_of_right >= 90:
            result.setStyleSheet("color: green")
        else:
            result.setStyleSheet("color: red")
        decision_status.addWidget(procent)
        decision_status.addWidget(result)

        explanation = ''
        number_of_letter = 0
        text_explanation = self.info['explanation']
        while number_of_letter + 40 <= len(text_explanation) - 1:
            row_long = 40
            while text_explanation[number_of_letter + row_long] != ' ':
                row_long -= 1
            if number_of_letter < 0:
                explanation += text_explanation[0:number_of_letter + row_long] + '\n'
            else:
                explanation += text_explanation[number_of_letter:number_of_letter + row_long] + '\n'
            number_of_letter += row_long + 1
        try:
            explanation += self.info['explanation'][number_of_letter:]
        except IndexError:
            pass
        exp = QLabel(explanation)
        exp.setFont(QFont("Montserrat Medium", 14))

        question_of_task = QLabel('Возник вопрос по заданию? Задайте его нам')
        question_of_task.setFont(QFont("Montserrat Medium", 12))
        question_of_task.setStyleSheet("text-decoration: underline; color: blue;")
        question_of_task.mousePressEvent = self.question_button_click

        buttons = QHBoxLayout()
        buttons.setSpacing(10)
        buttons.addStretch(1)
        continue_button = QPushButton('Продолжить')
        continue_button.setStyleSheet("background-color: rgb(63, 137, 255)")
        continue_button.clicked.connect(self.new_task)
        exit_button = QPushButton('Завершить')
        exit_button.setStyleSheet("background-color: rgb(244, 29, 29)")
        exit_button.clicked.connect(self.exit_button_click)
        buttons.addWidget(exit_button)
        buttons.addWidget(continue_button)

        grid.addWidget(titel, 0, 0)
        grid.addLayout(decision_status, 0, 1)
        grid.addWidget(exp, 1, 0)
        grid.addWidget(self.overlay_photo('answer', self.number_question), 1, 1)
        grid.addWidget(question_of_task, 2, 0)
        grid.addLayout(buttons, 2, 1)

        if self.layout() is not None:
            self.delete_items_of_layout(self.layout())
            sip.delete(self.layout())

        logging.info('Set layout in answer')
        self.setLayout(grid)

        self.number_of_task += 1

    def exit_button_click(self):
        logging.info('Exit button click')
        reply = QMessageBox.question(self, 'Message',
                                     "Вы уверены, что хотите завершить тестирование?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            logging.info('User answer - YES')
            logging.info('Return to menu')
            self.menu()
        else:
            logging.info('User answer - NO')

    def question_button_click(self, event):
        if self.user_can_ask_a_question:
            self.link_clicked = True
            self.close()

            super().__init__()

            self.setAutoFillBackground(True)
            p = self.palette()
            p.setColor(self.backgroundRole(), QColor(self.backgroundRad, self.backgroundGreen, self.backgroundBlue))
            self.setPalette(p)
            logging.info(f'Set background rgb{self.backgroundRad, self.backgroundGreen, self.backgroundBlue}')

            titel = QLabel('Введите ваш вопрос по задаче в это поле')
            fontTitel = QFont("Montserrat Medium", 20)
            fontTitel.setBold(True)
            titel.setFont(fontTitel)
            titel.setAlignment(Qt.AlignCenter)

            self.question_edit = QTextEdit()
            self.question_edit.setPlaceholderText('Введите сюда ваш вопрос')

            buttons = QHBoxLayout()
            buttons.addStretch(5)
            buttons.addSpacing(10)
            cancel_button = QPushButton('Отмена')
            continue_button = QPushButton('Продолжить')
            cancel_button.setStyleSheet("background-color: rgb(223, 209, 21)")
            continue_button.setStyleSheet("background-color: rgb(223, 209, 21)")
            cancel_button.clicked.connect(self.continue_question_button_click)
            continue_button.clicked.connect(self.continue_question_button_click)
            buttons.addWidget(cancel_button)
            buttons.addWidget(continue_button)

            content = QVBoxLayout(self)
            content.addSpacing(10)
            content.addWidget(titel)
            content.addWidget(self.question_edit)
            content.addLayout(buttons)

            self.setLayout(content)

            self.adjustSize()
            self.setGeometry(self.frameGeometry())
            self.move(150, 150)
            self.setWindowTitle('Ask a question')
            self.show()
        else:
            self.on_error('Вы не можете задавать более\n1 вопроса по задаче')

    def continue_question_button_click(self):
        sender = self.sender()
        if sender.text() == 'Отмена':
            self.answer_task()
            return

        if self.question_edit.toPlainText() != '':
            try:
                add_user_question_for_task(user_information['payload']['email'],
                                           self.question_edit.toPlainText(),
                                           self.class_of_tasks,
                                           self.number_of_task)
            except KeyError:
                self.on_error('Вопрос могут задавать только\n зарегестрированные пользователи')
                return
        else:
            self.on_error('Пожалуйста, введите вопрос')
            return

        self.user_can_ask_a_question = False
        titel = QLabel("Спсибо за ваш вопрос!\nВ скором времени мы вам ответим.", self)
        fontTitel = QFont("Montserrat Medium", 20)
        fontTitel.setBold(True)
        titel.setFont(fontTitel)
        titel.setAlignment(Qt.AlignCenter)

        btn = QPushButton('Вернуться')
        btn.setStyleSheet("background-color: rgb(223, 209, 21)")
        btn.clicked.connect(self.answer_task)

        self.delete_items_of_layout(self.layout())
        sip.delete(self.layout())
        box = QVBoxLayout()
        box.addWidget(titel)
        box.addWidget(btn)

        self.setLayout(box)

    def overlay_photo(self, status_task, overlay):

        if self.number_of_task % 9 != 1 or self.class_of_tasks != '10-11 класс':
            if self.class_of_tasks == '10-11 класс':
                names = [self.info['request'][i] for i in range(3)]
            else:
                names = self.info['options']
        else:
            names = self.info['request'][0].split('|')

        if status_task == 'new':
            img = Image.open('photo/taskCircles/all.png')
            if len(self.already_been) < 12:
                self.already_been += [names]
            else:
                self.already_been = []
        else:
            if overlay == 'all':
                img = Image.open('photo/taskCircles/all.png')
            else:
                img = Image.open('photo/taskCircles/all_grey.png').convert("RGBA")
                for number_photo in overlay:
                    sector = Image.open(f'photo/taskCircles/{number_photo}.png').convert("RGBA")
                    img.paste(sector, None, sector)

        draw = ImageDraw.Draw(img)
        draw.text((65, 120), names[0], fill=(0, 0, 0), font=ImageFont.truetype("fonts/Montserrat-Medium.ttf", 16))
        draw.text((250, 120), names[1], fill=(0, 0, 0), font=ImageFont.truetype("fonts/Montserrat-Medium.ttf", 16))
        draw.text((150, 270), names[2], fill=(0, 0, 0), font=ImageFont.truetype("fonts/Montserrat-Medium.ttf", 16))

        namePhoto = 'photo/taskCircles/newTask.png'
        img.save(namePhoto)

        photo = QLabel()
        pixmap = QPixmap(namePhoto)
        pixmap2 = pixmap.scaled(390, 390, Qt.KeepAspectRatio)
        photo.setPixmap(pixmap2)
        logging.info(f"Add photo '{namePhoto}' in answer window")

        return photo

    def closeEvent(self, event):
        sender = self.sender()

        if sender is not None or self.link_clicked:
            self.link_clicked = False
            event.accept()
            return

        logging.info('Close event')
        reply = QMessageBox.question(self, 'Message',
                                     "Вы уверены, что хотите выйти?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            logging.info('User answer - YES')
            logging.info('Close app')
            event.accept()
        else:
            logging.info('User answer - NO')
            event.ignore()

    def delete_items_of_layout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    self.delete_items_of_layout(item.layout())

    def on_exception(self, e):
        self.delete_items_of_layout(self.layout())
        if check_network_connection():
            error_message = QLabel('Извините, возникла какая-то ошибка\n'
                                   'Нажмите назад, чтобы вернуться назад', self)
        else:
            error_message = QLabel('Пожалуйста, проверьте ваше Интернет соединение\n'
                                   'Нажмите назад, чтобы вернуться назад', self)
        error_message.setAlignment(Qt.AlignCenter)
        error_message.setFont(QFont("Montserrat Bold", 20))
        hbox = QHBoxLayout()
        btn = QPushButton('Назад', self)
        btn.clicked.connect(self.error_button)
        hbox.addWidget(btn)
        self.layout().addWidget(error_message)
        self.layout().addChildLayout(hbox)
        logging.error('An error has occurred : ' + str(e))

    def on_error(self, e):
        logging.error('An error has occurred ' + str(e))
        QMessageBox().critical(self, 'Внимание!', e)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    logging.info('Start app')
    ex = Main()

    sys.exit(app.exec_())
