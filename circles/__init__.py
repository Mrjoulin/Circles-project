import sys
import sip
import random
import smtplib as smtp
from PIL import Image, ImageDraw, ImageFont
import logging
from functools import partial
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
NUMBER_OF_TASKS_9_CLASS = 15
NUMBER_OF_TASKS_10_CLASS = 9

EULERO_EMAIL = 'eulerocircles@gmail.com'
EULERO_PASSWORD = 'xsw2zaq1'


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
        if self.layout() is not None:
            sip.delete(self.layout())


        logging.info('Sign up window started')
        self.init_sign()
        self.adjustSize()
        self.setGeometry(450, 300, 500, 300)
        self.setWindowTitle('Sign in')
        self.show()

    def init_sign(self):
        title = QLabel('Пожалуйста, введите свои данные:')
        name = QLabel('Имя')
        surname = QLabel('Фамилия')
        patronymic = QLabel('Отчество')
        email = QLabel('Email')
        password = QLabel('Пароль( > 6 символов)')
        repeatPassword = QLabel('Повторите пароль')

        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Montserrat Bold", 18))
        name.setFont(QFont('Montserrat Medium'))
        surname.setFont(QFont('Montserrat Medium'))
        patronymic.setFont(QFont("Montserrat Medium"))
        email.setFont(QFont('Montserrat Medium'))
        password.setFont(QFont('Montserrat Medium'))
        repeatPassword.setFont(QFont('Montserrat Medium'))

        self.nameRegistrationEdit = QLineEdit(self)
        self.surnameRegistrationEdit = QLineEdit(self)
        self.patronymicRegistrationEdit = QLineEdit(self)
        self.patronymicRegistrationEdit.setPlaceholderText('Не обязательное поле')
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
            [title],
            [name, self.nameRegistrationEdit],
            [surname, self.surnameRegistrationEdit],
            [patronymic, self.patronymicRegistrationEdit],
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
            if self.nameRegistrationEdit.text() == '' or self.surnameRegistrationEdit.text() == '' \
                    or self.emailRegistrationEdit.text() == '':
                self.on_error('Пожалуйста, заполните все поля')
                return
            for letter in self.nameRegistrationEdit.text().lower():
                if letter not in alph or letter.isdigit():
                    self.on_error('Имя должно состоять только из букв русского алфавита')
                    self.nameRegistrationEdit.setStyleSheet("background-color: rgb(255, 50, 50)")
                    error_status = True

            for letter in self.surnameRegistrationEdit.text().lower():
                if letter not in alph or letter.isdigit():
                    self.on_error('Фамилия должна состоять только из букв русского алфавита')
                    self.surnameRegistrationEdit.setStyleSheet("background-color: rgb(255, 50, 50)")
                    error_status = True
            for letter in self.patronymicRegistrationEdit.text().lower():
                if letter not in alph or letter.isdigit():
                    self.on_error('Отчество должно состоять только из букв русского алфавита')
                    self.patronymicRegistrationEdit.setStyleSheet("background-color: rgb(255, 50, 50)")
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
                                                       patronymic=self.patronymicRegistrationEdit.text(),
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
        if self.layout() is not None:
            sip.delete(self.layout())

        logging.info('Login window started')
        self.init_login()
        self.adjustSize()
        self.setGeometry(450, 300, 500, 300)
        self.setWindowTitle('Login')
        self.show()

    def init_login(self):
        title = QLabel('Введите свой email и пароль,\n чтобы войти в аккаунт')
        email = QLabel('Email')
        password = QLabel('Пароль')

        title.setAlignment(Qt.AlignCenter)
        fontTitle = QFont("Montserrat Medium", 20)
        fontTitle.setBold(True)
        title.setFont(fontTitle)
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
            [title],
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
        if self.layout() is not None:
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
            user_status_name = QLabel(info['surname'] + ' ' + info['name'] + ' ' + info['patronymic'])
            user_status_email = QLabel(info['email'])

            user_status_name.setStyleSheet("text-decoration: underline; color: blue;")
            user_status_email.setStyleSheet("text-decoration: underline; color: blue;")
            user_status_name.mousePressEvent = self.user_exit
            user_status_email.mousePressEvent = self.user_exit
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
        auth_tests = QLabel('Или выберете нужный класс для\nтренировки решения задач')

        for item in [teacher_option, create_option, auth_tests]:
            item.setFont(QFont('Montserrat Medium', 16))
            item.setAlignment(Qt.AlignTop)
        create_option.setAlignment(Qt.AlignCenter)

        self.teacher_option_edit = QLineEdit(self)
        teacher_option_ok_button = QPushButton('ОК', self)
        teacher_option_ok_button.setStyleSheet("background-color: rgb(223, 209, 21)")
        teacher_option_ok_button.clicked.connect(self.get_teacher_option_button_click)
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
            item.clicked.connect(self.task_button_click)

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

    def user_exit(self, event):
        logging.info('User exit question')
        reply = QMessageBox.question(self, 'Message',
                                     "Вы уверены, что хотите выйти из аккаунта?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            logging.info('User answer - YES')
            logging.info('User exit')
            user_information['success'] = False
            user_information['payload'] = {}
            self.menu()
        else:
            logging.info('User answer - NO')

    def mouse_press_event_sign_up(self, event):
        self.sign_up()

    def mouse_press_event_login(self, event):
        self.login()

    def get_teacher_option_button_click(self):
        if not user_information['success']:
            self.on_error('Для испольования данной функции\nВы должны быть зарегестрированны')
            return
        try:
            options = get_teacher_option(self.teacher_option_edit.text())
        except Exception as e:
            self.on_exception(e)
            return

        if options == []:
            self.on_error('Введённого вами варианта не существует!')
        else:
            self.options = options
            self.get_stack_teacher_tasks()

    def get_stack_teacher_tasks(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)

        title = QLabel('По вашему запросу найдены \nследующие варианты:')
        fontTitle = QFont("Montserrat Medium", 20)
        fontTitle.setBold(True)
        title.setFont(fontTitle)
        title.setAlignment(Qt.AlignCenter)

        options = QVBoxLayout()
        options.setSpacing(5)
        number_line_cnt = 1
        for option in self.options:
            line = QHBoxLayout()
            line.setSpacing(10)

            number_line = QLabel(str(number_line_cnt) + '.')
            number_line.setFont(QFont("Montserrat Medium", 14))

            line_option = QHBoxLayout()
            line_option.setSpacing(10)

            line_text = QLabel(option['topic'][:30])
            line_text.setFont(QFont("Montserrat Medium", 14))
            line_text.setStyleSheet('color: grey')
            if self.teacher_option_edit.text().lower() == option['topic'].lower():
                line_number = QLabel(f"Вариант №{str(option['number_option'])}")
                line_number.setFont(QFont("Montserrat Medium", 14))
                line_text.setStyleSheet('background-color: yellow')
                line_option.addWidget(line_number)
            elif self.teacher_option_edit.text().isdigit():
                line_number = QHBoxLayout()
                line_number.addStretch(1)
                line_number_text = QLabel(f'Вариант №')
                line_number_text.setFont(QFont("Montserrat Medium", 14))
                line_number_int = QLabel(str(option['number_option']))
                line_number_int.setFont(QFont("Montserrat Medium", 14))
                line_number_int.setStyleSheet('background-color: yellow')
                line_number.addWidget(line_number_text)
                line_number.addWidget(line_number_int)
                line_option.addLayout(line_number)
            elif self.teacher_option_edit.text().lower() == option['email_teacher'].lower():
                line_number = QLabel(option['email_teacher'])
                line_number.setFont(QFont("Montserrat Medium", 14))
                line_number.setStyleSheet('background-color: yellow')
                line_option.addWidget(line_number)
            else:
                line_number = QHBoxLayout()
                line_number.addStretch(1)
                for item in option['name_teacher'].split():
                    line_number_text = QLabel(item)
                    line_number_text.setFont(QFont("Montserrat Medium", 14))
                    if item.lower() in self.teacher_option_edit.text().lower().split():
                        line_number_text.setStyleSheet('background-color: yellow')
                    line_number.addWidget(line_number_text)
                line_option.addLayout(line_number)

            line_option.addWidget(line_text)

            view_button = QPushButton('Просмотр')
            view_button.setStyleSheet("background-color: rgb(223, 209, 21)")
            view_button.clicked.connect(partial(self.get_teacher_option_view_button_click, number_line_cnt - 1))

            line.addWidget(number_line)
            line.addLayout(line_option)
            line.addWidget(view_button)

            options.addLayout(line)
            number_line_cnt += 1

        last_line = QHBoxLayout()
        last_line.setSpacing(10)
        button_left_box = QHBoxLayout()
        button_left = QPushButton('Назад')
        button_left.setStyleSheet("background-color: rgb(244, 29, 29)")
        button_left.clicked.connect(self.menu)
        button_left_box.addWidget(button_left)
        button_left_box.setAlignment(Qt.AlignLeft)
        text_right_box = QHBoxLayout()
        text_right = QLabel('Нажмите "Просмотр" для решения варианта')
        text_right.setFont(QFont("Montserrat Medium", 14))
        text_right.setStyleSheet('color: grey')
        text_right_box.addWidget(text_right)
        text_right_box.setAlignment(Qt.AlignRight)
        last_line.addLayout(button_left_box)
        last_line.addLayout(text_right_box)

        layout.addWidget(title)
        layout.addLayout(options)
        layout.addLayout(last_line)

        self.delete_items_of_layout(self.layout())
        if self.layout() is not None:
            sip.delete(self.layout())

        logging.info('Add layout in stack teachers options window')
        self.setLayout(layout)

    def send_email_teacher_option(self):
        sender = self.sender().text()
        if sender == 'Сохранить':
            msg = 'Спасибо за ваш новый вариант на Eulero!\n\nИнформация о варианте:\n' \
                  'Тема варианта: {topic}\n' \
                  'Количество кругов Эйлера: {number_of_circles}\n' \
                  '    Процент правильных ответов для отценки 5: {to_5}\n' \
                  '    Процент правильных ответов для отценки 4: {to_4}\n' \
                  '    Процент правильных ответов для отценки 5: {to_3}\n' \
                  'Показывать оценку по завершению: {mark}\n' \
                  'Номер варианта: {number}\n'.format(
                   topic=self.topic_edit.text(), number_of_circles=self.number_of_circles_combo.currentText(),
                   to_5=self.procent_of_right_for_5.text(), to_4=self.procent_of_right_for_4.text(),
                   to_3=self.procent_of_right_for_3.text(), mark='Да' if self.check_box_mark.isChecked() else 'Нет',
                   number=str(self.random_number)
                   )
            from_email = user_information['payload']['email']
        else:
            msg = 'Информация о прохождении вашего варианта на Eulero!\n\nИнформация о варианте:\n' \
                  'Тема варианта: {topic}\n' \
                  '    Процент правильных ответов для отценки 5: {to_5}%\n' \
                  '    Процент правильных ответов для отценки 4: {to_4}%\n' \
                  '    Процент правильных ответов для отценки 5: {to_3}%\n' \
                  'Показывать оценку по завершению: {mark}\n' \
                  'Номер варианта: {number}'.format(
                   topic=self.option['topic'],
                   to_5=self.option['procent_to_5'], to_4=self.option['procent_to_4'],
                   to_3=self.option['procent_to_3'], mark='Да' if self.option['show_mark'] else 'Нет',
                   number=str(self.option['number_option'])
                   )
            msg += '\n\nИнформация о проходившем пользователе:\n' \
                   '{availabilitypatronymic}: {name}\n' \
                   'email: {user_email}\n' \
                   '{option_passed}\n' \
                   'Вариант был найден {what_find}по номеру варианта'.format(
                    availabilitypatronymic='ФИО' if user_information['payload']['patronymic'] != '' else 'Фамилия, Имя',
                    name=f"{user_information['payload']['surname']} {user_information['payload']['name']} "
                         f"{user_information['payload']['patronymic']}",
                    user_email=user_information['payload']['email'],
                    option_passed='Процент верно решённых заданий: {percent}'.format(
                        percent=str(self.right_tasks * 100 // len(self.option['tasks']))
                    ) if sender == 'Продолжить' else '       Внимание!\nВариант не был пройден пользователем до конца!',
                    what_find='' if str(self.option['number_option']) == self.teacher_option_edit.text() else 'не '
                    )
            from_email = self.option['email_teacher']

        logging.info(f'Send message from: {from_email}, Message:\n{msg}\n')

        server = smtp.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(EULERO_EMAIL, EULERO_PASSWORD)
        server.sendmail(EULERO_EMAIL, from_email, f'From: {EULERO_EMAIL}\nTo: {from_email}\nSubject: '
                                                  f'Уведомление от Eulero!\n\n{msg}'.encode('utf-8'))
        server.quit()
        self.menu()

    def get_teacher_option_view_button_click(self, number_line):
        self.option = self.options[number_line]
        self.get_teacher_option()

    def get_teacher_option(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)

        title = QLabel(f'Решить вариант №{str(self.option["number_option"])}')
        fontTitle = QFont("Montserrat Medium", 20)
        fontTitle.setBold(True)
        title.setFont(fontTitle)
        title.setAlignment(Qt.AlignCenter)

        topic = QLabel(f'Тема: {self.option["topic"]}')
        topic.setFont(QFont("Montserrat Bold", 18))
        topic.setAlignment(Qt.AlignCenter)

        name_teacher = QLabel(f'Учитель: {self.option["name_teacher"]}')
        name_teacher.setFont(QFont("Montserrat Medium", 16))
        name_teacher.setAlignment(Qt.AlignCenter)

        if self.option['show_mark']:
            procents = QVBoxLayout()
            procents.addStretch(1)
            procents.addSpacing(5)
            procent_titel = QLabel("Процент верных ответов:")
            procent_titel.setFont(QFont("Montserrat Medium", 14))
            procent_titel.setAlignment(Qt.AlignCenter)
            procents.addWidget(procent_titel)
            for i in range(5, 2, -1):
                procent_text = f"procent_to_{str(i)}"
                procent = QLabel(f'На оценку {str(i)} - {self.option[procent_text]}%')
                procent.setFont(QFont("Montserrat Medium", 14))
                procent.setAlignment(Qt.AlignCenter)
                procents.addWidget(procent)

        buttons = QHBoxLayout()
        buttons.setSpacing(10)
        buttons.addStretch(1)
        cancelButton = QPushButton('Отмена', self)
        continueButton = QPushButton('Приступить', self)
        cancelButton.setStyleSheet("background-color: rgb(223, 209, 21)")
        continueButton.setStyleSheet("background-color: rgb(223, 209, 21)")
        cancelButton.clicked.connect(self.get_stack_teacher_tasks)
        continueButton.clicked.connect(self.get_teacher_tasks)
        buttons.addWidget(cancelButton)
        buttons.addWidget(continueButton)

        layout.addWidget(title)
        layout.addWidget(topic)
        layout.addWidget(name_teacher)
        if self.option['show_mark']:
            layout.addLayout(procents)
        layout.addLayout(buttons)

        self.delete_items_of_layout(self.layout())
        if self.layout() is not None:
            sip.delete(self.layout())

        logging.info('Add layout in get teacher option window')
        self.setLayout(layout)

        self.is_teacher_option_passed = False
        self.number_of_task = 0
        self.right_tasks = 0
        self.right_tasks_numbers = []
        self.already_been = []

    def get_teacher_tasks(self):
        self.class_of_tasks = 'teacher task'
        self.answer_photo = 'all'
        if len(self.option['tasks']) > self.number_of_task:
            self.task = self.option['tasks'][self.number_of_task]
            self.new_task()
        else:
            self.is_teacher_option_passed = True
            self.get_teacher_option_final_window()

    def get_teacher_option_final_window(self):
        self.delete_items_of_layout(self.layout())
        if self.layout() is not None:
            sip.delete(self.layout())

        layout = QVBoxLayout()
        layout.setSpacing(10)

        title = QLabel(f'Итоги решения варианта №{self.option["number_option"]}')
        fontTitle = QFont("Montserrat Medium", 20)
        fontTitle.setBold(True)
        title.setFont(fontTitle)
        title.setAlignment(Qt.AlignCenter)

        topic = QLabel(f'Тема: {self.option["topic"]}')
        topic.setFont(QFont("Montserrat Bold", 18))
        topic.setAlignment(Qt.AlignCenter)

        name_teacher = QLabel(f'Учитель: {self.option["name_teacher"]}')
        name_teacher.setFont(QFont("Montserrat Medium", 16))
        name_teacher.setAlignment(Qt.AlignCenter)

        stack_tasks = QVBoxLayout()
        stack_tasks.setSpacing(10)

        for task in self.option['tasks']:
            line = QHBoxLayout()
            line.setSpacing(10)
            line_content = QHBoxLayout()
            line_content.setSpacing(0)
            if task['8-9 class']['table 8-9 class']:
                class_of_table = '8-9 class'
            elif task['10-11 class']['table 10-11 class']:
                class_of_table = '10-11 class'
            else:
                class_of_table = 'other'

            number_of_task = task[class_of_table]['payload']['number of task']
            line_content_number = QLabel(f"Задание №{number_of_task}")
            line_content_number.setFont(QFont("Montserrat Medium", 14))
            if task[class_of_table]['payload']['text task'][:30] == task[class_of_table]['payload']['text task']:
                line_content_text = QLabel('  ' + task[class_of_table]['payload']['text task'])
            else:
                line_content_text = QLabel('  ' + task[class_of_table]['payload']['text task'][:27] + '...')
            line_content_text.setFont(QFont("Montserrat Medium", 14))

            if number_of_task in self.right_tasks_numbers:
                line_content_number.setStyleSheet('background-color: rgb(118, 206, 103)')
                line_content_text.setStyleSheet('color: rgb(61, 61, 61); background-color: rgb(118, 206, 103)')
            else:
                line_content_number.setStyleSheet('background-color: rgb(237, 73, 73)')
                line_content_text.setStyleSheet('color: rgb(61, 61, 61); background-color: rgb(237, 73, 73)')

            line_content.addWidget(line_content_number)
            line_content.addWidget(line_content_text)

            line_view_button = QPushButton('Просмотр')
            line_view_button.setStyleSheet("background-color: rgb(223, 209, 21)")
            line_view_button.clicked.connect(partial(self.get_teacher_task_final_view, number_of_task - 1))

            line.addLayout(line_content)
            line.addWidget(line_view_button)

            stack_tasks.addLayout(line)

        procent_mark = QHBoxLayout()
        procent_mark.setSpacing(10)
        procent_of_right = self.right_tasks * 100 // len(self.option['tasks'])
        if self.option['show_mark']:
            procent = QLabel("Ваша оценка: ")
            procent.setFont(QFont("Montserrat Medium", 16))
            mark = QLabel('2')
            for mark_number in range(3, 6):
                if procent_of_right >= int(self.option[f'procent_to_{mark_number}']):
                    mark = QLabel(str(mark_number))
            mark.setFont(QFont("Montserrat Medium", 24))
        else:
            procent = QLabel("Процент ваших правильных ответов:")
            procent.setFont(QFont("Montserrat Medium", 14))
            mark = QLabel(str(procent_of_right))
            mark.setFont(QFont("Montserrat Medium", 24))

        mark.setStyleSheet('color: rgb(244, 29, 29)')
        procent_mark.addWidget(procent)
        procent_mark.addWidget(mark)

        last_line = QHBoxLayout()
        last_line.setSpacing(10)
        self.class_of_tasks = 'teacher window'
        question_of_task = QLabel('У Вас возник вопрос? Задайте его нам')
        question_of_task.setFont(QFont("Montserrat Medium", 12))
        question_of_task.setStyleSheet("text-decoration: underline; color: blue;")
        question_of_task.mousePressEvent = self.question_button_click
        button_box = QHBoxLayout()
        continue_button = QPushButton('Продолжить')
        continue_button.setStyleSheet("background-color: rgb(223, 209, 21)")
        continue_button.clicked.connect(self.send_email_teacher_option)
        button_box.addWidget(continue_button)
        button_box.setAlignment(Qt.AlignRight)
        last_line.addWidget(question_of_task)
        last_line.addLayout(button_box)

        layout.addWidget(title)
        layout.addWidget(topic)
        layout.addWidget(name_teacher)
        layout.addLayout(stack_tasks)
        layout.addLayout(procent_mark)
        layout.addLayout(last_line)

        logging.info('Set layout in get teacher option final window')
        self.setLayout(layout)
        self.adjustSize()

    def get_teacher_task_final_view(self, number_task):
        self.task = self.option['tasks'][number_task]
        self.class_of_tasks = 'final preview task'
        self.new_task()

    def create_teacher_option(self):
        if not user_information['success']:
            self.on_error('Для испольования данной функции\nВы должны быть зарегестрированны')
            return
        self.delete_items_of_layout(self.layout())
        if self.layout() is not None:
            sip.delete(self.layout())

        logging.info('Teacher option window started')
        self.init_teacher_option()

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(self.backgroundRad, self.backgroundGreen, self.backgroundBlue))
        self.setPalette(p)
        logging.info(f'Set background rgb{self.backgroundRad, self.backgroundGreen, self.backgroundBlue}')

        self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.adjustSize()
        self.setGeometry(300, 200, 600, 300)
        self.setWindowTitle('Teacher Option')
        self.show()

    def init_teacher_option(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        title = QLabel('Создать вариант')
        fontTitle = QFont("Montserrat Medium", 20)
        fontTitle.setBold(True)
        title.setFont(fontTitle)
        title.setAlignment(Qt.AlignCenter)

        topic_box = QHBoxLayout()
        topic_box.setSpacing(10)
        topic = QLabel('Тема: ')
        topic.setFont(QFont("Montserrat Medium", 16))
        self.topic_edit = QLineEdit()
        self.topic_edit.setPlaceholderText('Введите сюда тему варианта')
        topic_box.addWidget(topic)
        topic_box.addWidget(self.topic_edit)

        class_of_task = QHBoxLayout()
        class_of_task_text = QLabel('Задания, ориентируемые на')
        class_of_task_text.setFont(QFont("Montserrat Medium", 14))
        self.class_of_task_combo = QComboBox()
        self.class_of_task_combo.addItems(['5 класс', '6 класс', '7 класс', '8 класс',
                                           '9 класс', '10 класс', '11 класс', 'любой класс'])
        class_of_task.addWidget(class_of_task_text)
        class_of_task.addWidget(self.class_of_task_combo)

        number_of_circles = QHBoxLayout()
        number_of_circles_text = QLabel('Количество кругов Эйлера:')
        number_of_circles_text.setFont(QFont("Montserrat Medium", 14))
        self.number_of_circles_combo = QComboBox()
        self.number_of_circles_combo.addItems(['3 окружности', '4 окружности'])
        number_of_circles.addWidget(number_of_circles_text)
        number_of_circles.addWidget(self.number_of_circles_combo)

        procent = QVBoxLayout()
        procent.setSpacing(5)
        procent.addStretch(1)
        procent_of_right_in_tasks = QLabel('Процент правильных ответов для оценки:')
        procent_of_right_in_tasks.setFont(QFont("Montserrat Medium", 14))
        procent.addWidget(procent_of_right_in_tasks)

        procents_for_mark = {'5': '90', '4': '75', '3': '50'}

        self.procent_of_right_for_5 = QLineEdit()
        self.procent_of_right_for_4 = QLineEdit()
        self.procent_of_right_for_3 = QLineEdit()

        for mark, procents in procents_for_mark.items():
            line = QHBoxLayout()
            line.addStretch(1)

            text_line = QLabel(f'% - "{mark}"')
            text_line.setFont(QFont("Montserrat Medium", 14))

            default = QLabel(f'(по умолчанию {procents}%)')
            default.setFont(QFont("Montserrat Medium", 14))
            default.setStyleSheet("color: grey")

            if mark == '5':
                line.addWidget(self.procent_of_right_for_5)
            elif mark == '4':
                line.addWidget(self.procent_of_right_for_4)
            else:
                line.addWidget(self.procent_of_right_for_3)
            line.addWidget(text_line)
            line.addWidget(default)
            line.setAlignment(Qt.AlignLeft)
            procent.addLayout(line)

        self.check_box_mark = QCheckBox('Показывать оценку по окончанию прохождения теста', self)
        self.check_box_mark.setChecked(True)
        procent.addWidget(self.check_box_mark)

        number_of_tasks = QHBoxLayout()
        number_of_tasks.addStretch(1)
        number_of_tasks_text = QLabel("Количество задач: ")
        number_of_tasks_text.setFont(QFont("Montserrat Medium", 14))
        number_of_tasks_text_default = QLabel('(можно оставить незаполненным)')
        number_of_tasks_text_default.setFont(QFont("Montserrat Medium", 12))
        number_of_tasks_text_default.setStyleSheet('color: grey;')
        self.number_of_tasks_edit = QLineEdit()
        number_of_tasks.addWidget(number_of_tasks_text)
        number_of_tasks.addWidget(self.number_of_tasks_edit)
        number_of_tasks.addWidget(number_of_tasks_text_default)

        buttons = QHBoxLayout()
        buttons.setSpacing(10)
        buttons.addStretch(1)
        cancelButton = QPushButton('Отмена', self)
        continueButton = QPushButton('Приступить', self)
        cancelButton.setStyleSheet("background-color: rgb(223, 209, 21)")
        continueButton.setStyleSheet("background-color: rgb(223, 209, 21)")
        cancelButton.clicked.connect(self.menu)
        continueButton.clicked.connect(self.teacher_option_button_click)
        buttons.addWidget(cancelButton)
        buttons.addWidget(continueButton)

        layout.addWidget(title)
        layout.addLayout(topic_box)
        layout.addLayout(class_of_task)
        layout.addLayout(number_of_circles)
        layout.addLayout(procent)
        layout.addLayout(number_of_tasks)
        layout.addLayout(buttons)

        layout.setAlignment(Qt.AlignLeft)
        logging.info('Set layout in teacher option')
        self.setLayout(layout)
        self.teacher_tasks = []
        self.teacher_tasks_appended = False

    def teacher_option_button_click(self):
        if self.topic_edit.text() == '':
            self.on_error('Введите тему варианта!')
            return

        if self.procent_of_right_for_5.text().isdigit():
            if float(self.procent_of_right_for_5.text()) > 100.0 or float(self.procent_of_right_for_5.text()) < 1.0:
                self.procent_of_right_for_5.setText('90')
        else:
            self.procent_of_right_for_5.setText('90')

        if self.procent_of_right_for_4.text().isdigit():
            if float(self.procent_of_right_for_4.text()) > float(self.procent_of_right_for_5.text()) or\
                    float(self.procent_of_right_for_4.text()) < 1.0:
                if 75.0 < float(self.procent_of_right_for_5.text()):
                    self.procent_of_right_for_4.setText('75')
                else:
                    self.procent_of_right_for_4.setText(str(float(self.procent_of_right_for_5.text()) / 2))
        else:
            self.procent_of_right_for_4.setText('75')

        if self.procent_of_right_for_3.text().isdigit():
            if float(self.procent_of_right_for_3.text()) > float(self.procent_of_right_for_4.text()) or\
                    float(self.procent_of_right_for_3.text()) < 1.0:
                if 75.0 < float(self.procent_of_right_for_4.text()):
                    self.procent_of_right_for_3.setText('50')
                else:
                    self.procent_of_right_for_3.setText(str(float(self.procent_of_right_for_4.text()) / 2))
        else:
            self.procent_of_right_for_3.setText('50')

        if self.number_of_tasks_edit.text().isdigit():
            if int(self.number_of_tasks_edit.text()) > 20 or int(self.number_of_tasks_edit.text()) < 1:
                self.number_of_tasks_edit.setText('20')
        else:
            self.number_of_tasks_edit.setText('20')

        combo_text = self.class_of_task_combo.currentText()
        self.number_of_task = 0
        self.before_teacher_option_task_usual()

    def before_teacher_option_task_usual(self):
        sender = self.sender().text()
        self.table_9 = False if sender != 'Таблица 8-9 класс' else True
        self.table_10 = False if sender != 'Таблица 10-11 класс' else True
        self.no_table = False if self.table_9 or self.table_10 else True

        self.teacher_option_task_usual()

    def teacher_option_task_usual(self):
        sender = self.sender().text()
        self.class_of_tasks = 'preview task'

        if int(self.number_of_tasks_edit.text()) <= self.number_of_task:
            self.teacher_tasks.append(self.task)
            self.teacher_option_final_window()
            return

        if sender != 'Назад' and sender != 'Таблица 8-9 класс' and sender != 'Таблица 10-11 класс' and \
                sender != 'Текстовое поле':
            if sender != 'Добавить задачу':
                self.teacher_tasks_appended = not self.teacher_tasks_appended
                if not self.teacher_tasks_appended:
                    self.teacher_tasks.append(self.task)
                    self.teacher_tasks_appended = True
            self.number_of_task += 1

        layout = QVBoxLayout()
        layout.setSpacing(10)

        title = QLabel(f'Задача №{str(self.number_of_task)}')
        fontTitle = QFont("Montserrat Medium", 20)
        fontTitle.setBold(True)
        title.setFont(fontTitle)
        title.setAlignment(Qt.AlignCenter)

        info_block = QHBoxLayout()
        info_block.addStretch(1)
        info_text = QLabel('обязательное поле')
        info_star = QLabel('*')
        info_star.setFont(QFont("Montserrat Medium", 14))
        info_star.setStyleSheet("color: red")
        info_text.setFont(QFont("Montserrat Medium", 14))
        info_block.addWidget(info_star)
        info_block.addWidget(info_text)

        task = QVBoxLayout()
        task.addStretch(1)
        text_task = QHBoxLayout()
        text_task.addStretch(1)
        text_task_without_star = QLabel('{text} задачи:'.format(text='Текст' if self.no_table else 'Таблица'))
        text_task_without_star.setFont(QFont("Montserrat Medium", 14))
        info_star = QLabel('*')
        info_star.setFont(QFont("Montserrat Medium", 14))
        info_star.setStyleSheet("color: red")
        text_task.addWidget(info_star)
        text_task.addWidget(text_task_without_star)
        text_task.setAlignment(Qt.AlignLeft)
        if self.table_9:
            table = QVBoxLayout()
            table.setSpacing(5)
            letters = ['А', 'Б', 'В',  'Г']
            if sender == 'Назад':
                text = [i.text() for i in self.table_tasks]
                number = [i.text() for i in self.table_circles_numbers]
            else:
                text = ['', '', '', '']
                number = ['', '', '', '']
            self.table_tasks = []
            self.table_circles_numbers = []
            for letter in range(len(letters)):
                line = QHBoxLayout()
                line.setSpacing(5)
                line_text = QLabel(letters[letter])
                line_text.setFont(QFont('Montserrat Medium', 14))
                line_edit = QLineEdit()
                line_edit.setPlaceholderText('Запрос')
                line_edit.setText(text[letter])
                self.table_tasks.append(line_edit)
                line_sectors_edit = QLineEdit()
                line_sectors_edit.setPlaceholderText('Сектора кругов Эйлера')
                line_sectors_edit.setText(number[letter])
                self.table_circles_numbers.append(line_sectors_edit)
                line.addWidget(line_text)
                line.addWidget(line_edit)
                line.addWidget(line_sectors_edit)
                table.addLayout(line)

            text_question = QHBoxLayout()
            text_question.setSpacing(5)
            text_question.addStretch(1)
            question = QLabel(f"Расположить буквы в порядке ")
            question.setFont(QFont('Montserrat Medium', 14))

            index = self.question_combo.findText(self.question_combo.currentText(), Qt.MatchFixedString) \
                if sender == 'Назад' else 0

            self.question_combo = QComboBox()
            self.question_combo.addItems(['возрастания', 'убывания'])
            self.question_combo.setCurrentIndex(index)

            text_question.addWidget(question)
            text_question.addWidget(self.question_combo)
            table.addLayout(text_question)
            table.addLayout(table)

        elif self.table_10:
            table = QGridLayout()
            request = QLabel("Запрос")
            request.setFont(QFont('Montserrat Medium', 14))
            find = QLabel('Найдено страниц')
            find.setFont(QFont('Montserrat Medium', 14))
            table.addWidget(request, 0, 0)
            table.addWidget(find, 0, 1)
            if sender == 'Назад':
                text = [i.text() for i in self.table_tasks]
                number = [i.text() for i in self.table_circles_numbers]
            else:
                text = ['', '', '', '', '', '']
                number = ['', '', '', '', '', '']
            self.table_tasks = []
            self.table_circles_numbers = []
            for i in range(6):
                line_edit = QLineEdit()
                line_edit.setPlaceholderText('Запрос')
                line_edit.setText(text[i])
                self.table_tasks.append(line_edit)
                line_sectors_edit = QLineEdit()
                line_sectors_edit.setPlaceholderText('Найдено страниц')
                line_sectors_edit.setText(number[i])
                self.table_circles_numbers.append(line_sectors_edit)
                table.addWidget(line_edit, i + 1, 0)
                table.addWidget(line_sectors_edit, i + 1, 1)

            question = QLabel('Найти: ')
            question.setFont(QFont('Montserrat Medium', 14))
            self.question_text_edit = QLineEdit()
            self.question_text_edit.setPlaceholderText('Вопрос')
            table.addWidget(question, 7, 0)
            table.addWidget(self.question_text_edit, 7, 1)
        else:
            if sender == 'Назад':
                text = self.text_task.toPlainText()
            else:
                text = ''
            self.text_task = QTextEdit()
            self.text_task.setPlaceholderText('Введите текст задачи сюда')
            self.text_task.setText(text)

        buttons_table = QHBoxLayout()
        buttons_table.setSpacing(50)
        button_9_class = QPushButton('Текстовое поле' if self.table_9 else 'Таблица 8-9 класс')
        button_9_class.setStyleSheet("background-color: rgb(223, 209, 21)")
        button_9_class.clicked.connect(self.before_teacher_option_task_usual)
        button_10_class = QPushButton('Текстовое поле' if self.table_10 else 'Таблица 10-11 класс')
        button_10_class.setStyleSheet("background-color: rgb(223, 209, 21)")
        button_10_class.clicked.connect(self.before_teacher_option_task_usual)
        buttons_table.addWidget(button_9_class)
        buttons_table.addWidget(button_10_class)
        task.addLayout(text_task)
        if self.no_table:
            task.addWidget(self.text_task)
        else:
            task.addLayout(table)
        task.addLayout(buttons_table)

        photo = QLabel(self)
        if self.number_of_circles_combo.currentText() == '3 окружности':
            namePhoto = 'photo/threeCircles.png'
        else:
            namePhoto = 'photo/fourCircles.png'
        pixmap = QPixmap(namePhoto)
        pixmap2 = pixmap.scaled(300, 300, Qt.KeepAspectRatio)
        photo.setPixmap(pixmap2)
        logging.info(f"Add photo '{namePhoto}' in teacher options window")

        names_box = QVBoxLayout()
        names_box.addStretch(1)
        names_box.setSpacing(5)

        names_title = QLabel('Введите названия множеств:')
        names_title.setFont(QFont("Montserrat Medium", 14))
        names_perms = QHBoxLayout()
        names_perms.setSpacing(10)
        names_perms.addStretch(1)
        names_text = ['1: ', '2: ', '3: ']
        if self.number_of_circles_combo.currentText() == '4 окружности':
            names_text.append('4: ')

        if sender == 'Назад':
            text = [i.text() for i in self.names_edits]
        else:
            text = ['', '', '', '']
        self.names_edits = []
        for label in range(len(names_text)):
            self.name_edit = QLineEdit()
            self.name_edit.setPlaceholderText(f'"{str(label + 1)}" по умолчанию')
            self.name_edit.setText(text[label])
            text_perm = QLabel(names_text[label])
            text_perm.setFont(QFont("Montserrat Medium", 14))
            names_perms.addWidget(text_perm)
            names_perms.addWidget(self.name_edit)
            self.names_edits.append(self.name_edit)
        names_box.addWidget(names_title)
        names_box.addLayout(names_perms)

        answer = QHBoxLayout()
        answer.setSpacing(5)
        answer_text = QLabel('Ответ:')
        answer_text.setFont(QFont("Montserrat Medium", 14))
        if sender == 'Назад':
            text = self.answer_edit.text()
        else:
            text = ''
        self.answer_edit = QLineEdit()
        self.answer_edit.setPlaceholderText('Введите сюда ответ')
        self.answer_edit.setText(text)

        info_star = QLabel('*')
        info_star.setFont(QFont("Montserrat Medium", 14))
        info_star.setStyleSheet("color: red")
        answer.addWidget(info_star)
        answer.addWidget(answer_text)
        answer.addWidget(self.answer_edit)

        if not self.table_9:
            answer_picture = QLabel('Сектора кругов Эйлера:')
            answer_picture.setFont(QFont("Montserrat Medium", 14))
            if sender == 'Назад':
                text = self.answer_picture_edit.text()
            else:
                text = ''
            self.answer_picture_edit = QLineEdit()
            self.answer_picture_edit.setPlaceholderText('ТОЛЬКО номера секторов')
            self.answer_picture_edit.setText(text)

            answer.addWidget(answer_picture)
            answer.addWidget(self.answer_picture_edit)

        explanation = QVBoxLayout()
        explanation.setSpacing(5)
        explanation.addStretch(1)
        explanation_text = QHBoxLayout()
        explanation_text.addStretch(1)
        explanation_text_without_star = QLabel('Объяснение задачи:')
        explanation_text_without_star.setFont(QFont("Montserrat Medium", 14))
        info_star = QLabel('*')
        info_star.setFont(QFont("Montserrat Medium", 14))
        info_star.setStyleSheet("color: red")
        explanation_text.addWidget(info_star)
        explanation_text.addWidget(explanation_text_without_star)
        if self.table_9:
            if sender == 'Назад':
                check = self.auth_explanation_check_box.isChecked()
            else:
                check = False
            self.auth_explanation_check_box = QCheckBox('Автоматическое объяснение')
            self.auth_explanation_check_box.setChecked(check)
            explanation_text.addWidget(self.auth_explanation_check_box)

        if sender == 'Назад':
            text = self.explanation_edit.toPlainText()
        else:
            text = ''
        self.explanation_edit = QTextEdit()
        self.explanation_edit.setPlaceholderText('Введите сюда объяснение задачи')
        self.explanation_edit.setText(text)
        explanation.addLayout(explanation_text)
        explanation.addWidget(self.explanation_edit)

        buttons = QHBoxLayout()
        buttons.setSpacing(10)
        buttons.addStretch(1)
        continue_button = QPushButton('Предпросмотр')
        continue_button.setStyleSheet("background-color: rgb(63, 137, 255)")
        continue_button.clicked.connect(self.teacher_option_task_button_click)
        exit_button = QPushButton('Завершить')
        exit_button.setStyleSheet("background-color: rgb(244, 29, 29)")
        exit_button.clicked.connect(self.exit_button_click)
        buttons.addWidget(exit_button)
        buttons.addWidget(continue_button)

        titel_box = QHBoxLayout()
        titel_box.addWidget(title)
        titel_box.addLayout(info_block)

        task_box = QHBoxLayout()
        task_box.addLayout(task)
        task_box.addWidget(photo)

        layout.addLayout(titel_box)
        layout.addLayout(task_box)
        layout.addLayout(names_box)
        layout.addLayout(answer)
        layout.addLayout(explanation)
        layout.addLayout(buttons)

        if self.layout() is not None:
            self.delete_items_of_layout(self.layout())
            sip.delete(self.layout())

        logging.info('Set layout in task')
        self.setLayout(layout)

        self.adjustSize()
        self.setGeometry(300, 150, 750, 300)
        self.setWindowTitle('Teacher Task')
        self.show()

    def teacher_option_task_button_click(self):
        logging.info(str(self.table_9) + str(self.table_10) + str(self.no_table))
        if self.no_table:
            if self.text_task.toPlainText() == '':
                self.on_error('Введите текст задачи!')
                return
        if self.answer_edit .text() == '':
            self.on_error('Введите ответ на задачу!')
            return
        if self.no_table or self.table_10 or (self.table_9 and not self.auth_explanation_check_box.isChecked()):
            if self.explanation_edit.toPlainText() == '':
                self.on_error('Введите объяснение задачи!')
                return

        names_perms = []
        for name in range(len(self.names_edits)):
            if self.names_edits[name].text() != '':
                names_perms.append(self.names_edits[name].text())
            else:
                names_perms.append(str(name + 1))

        payload_9_class = {}
        payload_10_class = {}
        payload_other = {}

        if self.table_9:
            for i in range(4):
                if self.table_tasks[i].text() == '':
                    self.on_error('Заполните все поля запроса!')
                    return
                for number in self.table_circles_numbers[i].text():
                    if not number.isdigit() or int(number) < 1 \
                           or int(number) > 7:
                        self.table_circles_numbers[i].setText('')

            payload_9_class = {
                'number of task': self.number_of_task,
                'text task': f'А: {self.table_tasks[0].text()} Б: {self.table_tasks[1].text()} '
                             f'В: {self.table_tasks[2].text()} Г: {self.table_tasks[3].text()}',
                'request': {
                    'А': f'{self.table_tasks[0].text()};{self.table_circles_numbers[0].text()}',
                    'Б': f'{self.table_tasks[1].text()};{self.table_circles_numbers[1].text()}',
                    'В': f'{self.table_tasks[2].text()};{self.table_circles_numbers[2].text()}',
                    'Г': f'{self.table_tasks[3].text()};{self.table_circles_numbers[3].text()}'
                },
                'options': names_perms,
                'question': self.question_combo.currentText(),
                'answer': self.answer_edit.text(),
                'sectors circles': None,
                'auth explanation': self.auth_explanation_check_box.isChecked(),
                'explanation': self.explanation_edit.toPlainText()
            }
        elif self.table_10:
            requests = []
            finds = []

            if self.question_text_edit.text() == '':
                self.on_error('Введите то, что нужно найти')
                return

            for i in range(6):
                if self.table_tasks[i].text() != '':
                    requests.append(self.table_tasks[i].text())
                    if self.table_circles_numbers[1].text() != '':
                        finds.append(self.table_circles_numbers[i].text())
                    else:
                        self.on_error('Введите количество найденных страниц для запроса')
                        return

            if len(requests) < 3:
                self.on_error('Введите больше запросов')
                return

            text_task = ''
            for request, find in zip(requests, finds):
                text_task += request + ' ' + find + '; '

            payload_10_class = {
                'number of task': self.number_of_task,
                'text task': f'А: {self.table_tasks[0].text()} Б: {self.table_tasks[1].text()} '
                             f'В: {self.table_tasks[2].text()} Г: {self.table_tasks[3].text()}',
                'request': requests,
                'find': finds,
                'options': names_perms,
                'question': f'{self.question_text_edit.text()};{self.answer_picture_edit.text()}',
                'answer': self.answer_edit.text(),
                'sectors circles': None,
                'explanation': self.explanation_edit.toPlainText()
            }
        else:
            number_answer = ''
            for numeral in self.answer_picture_edit.text():
                try:
                    if int(numeral) < 1 or int(numeral) > 7:
                        number_answer = ''
                        break
                    else:
                        number_answer += str(numeral)
                except ValueError:
                    number_answer = ''

            payload_other = {
                'number of task': self.number_of_task,
                'text task': self.text_task.toPlainText(),
                'options': names_perms,
                'answer': self.answer_edit.text(),
                'sectors circles': number_answer,
                'explanation': self.explanation_edit.toPlainText()
            }

        self.task = {
            '8-9 class': {'table 8-9 class': self.table_9, 'payload': payload_9_class},
            '10-11 class': {'table 10-11 class': self.table_10, 'payload': payload_10_class},
            'other': {'no table': self.no_table, 'payload': payload_other}
        }

        self.setWindowTitle('Preview')
        self.new_task()

    def teacher_option_final_window(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)

        title = QLabel(self.topic_edit.text())
        fontTitle = QFont("Montserrat Medium", 20)
        fontTitle.setBold(True)
        title.setFont(fontTitle)
        title.setAlignment(Qt.AlignCenter)

        stack_task = QVBoxLayout()
        stack_task.setSpacing(5)
        stack_task.addStretch(1)
        stack_task_text = QLabel('Добавленные задачи:')
        stack_task_text.setFont(QFont("Montserrat Medium", 18))
        stack_task_text.setAlignment(Qt.AlignCenter)
        stack_task.addWidget(stack_task_text)
        logging.info(self.teacher_tasks)
        for item in self.teacher_tasks:
            line = QHBoxLayout()
            line.setSpacing(10)
            frame = QFrame()
            frame.setFrameShape(QFrame.Box)
            task = QHBoxLayout()
            task.addSpacing(5)
            if item['8-9 class']['table 8-9 class']:
                table = '8-9 class'
            elif item['10-11 class']['table 10-11 class']:
                table = '10-11 class'
            else:
                table = 'other'

            task_number = QLabel(f'Задание №{item[table]["payload"]["number of task"]}')
            task_number.setFont(QFont("Montserrat Medium", 14))
            if len(item[table]["payload"]['text task']) > 40:
                task_text = QLabel(item[table]["payload"]['text task'][:40] + '...')
            else:
                task_text = QLabel(item[table]["payload"]['text task'])
            task_text.setFont(QFont("Montserrat Medium", 14))
            task_text.setStyleSheet('color: grey')
            task.addWidget(task_number)
            task.addWidget(task_text)
            remove_button = QPushButton('Удалить')
            remove_button.setStyleSheet("background-color: rgb(244, 29, 29)")
            remove_button.clicked.connect(partial(self.delete_teacher_task, item[table]["payload"]["number of task"]))
            line.addLayout(task)
            line.addWidget(remove_button)
            line.setAlignment(Qt.AlignCenter)
            stack_task.addLayout(line)

        if len(self.teacher_tasks) < 20:
            button_box = QHBoxLayout()
            self.number_of_tasks_edit.setText(str(int(self.number_of_tasks_edit.text()) + 1))
            add_button = QPushButton('Добавить задачу')
            add_button.setStyleSheet("background-color: rgb(223, 209, 21)")
            add_button.clicked.connect(self.teacher_option_task_usual)
            button_box.addWidget(add_button)
            button_box.setAlignment(Qt.AlignCenter)

        number_of_option = QHBoxLayout()
        number_of_option.setSpacing(10)
        self.random_number = random.randint(100000, 999999)
        number_of_option_text = QLabel(f'Номер варианта - {str(self.random_number)}')
        number_of_option_text.setFont(QFont("Montserrat Medium", 14))
        number_of_option_info = QLabel('(сохраните его для дальнейшего доступа)')
        number_of_option_info.setFont(QFont("Montserrat Medium", 14))
        number_of_option_info.setStyleSheet('color: grey')
        number_of_option.addWidget(number_of_option_text)
        number_of_option.addWidget(number_of_option_info)
        number_of_option.setAlignment(Qt.AlignCenter)

        open_access = QHBoxLayout()
        open_access.addSpacing(5)
        self.open_access = QCheckBox('Открытый оступ')
        self.open_access.setChecked(True)
        open_access_text = QLabel('(кроме № варианта, ещё по теме, вашему email и ФИО)')
        open_access_text.setFont(QFont("Montserrat Medium", 13))
        open_access_text.setStyleSheet('color: grey')
        open_access.addWidget(self.open_access)
        open_access.addWidget(open_access_text)
        open_access.setAlignment(Qt.AlignCenter)

        buttons = QHBoxLayout()
        buttons.setSpacing(10)
        button_left_box = QHBoxLayout()
        button_left = QPushButton('Не сохранять')
        button_left.setStyleSheet("background-color: rgb(244, 29, 29)")
        button_left.clicked.connect(self.not_save_teacher_option)
        button_left_box.addWidget(button_left)
        button_left_box.setAlignment(Qt.AlignLeft)
        button_right_box = QHBoxLayout()
        button_right = QPushButton('Сохранить')
        button_right.setStyleSheet('background-color: rgb(140, 255, 0)')
        button_right.clicked.connect(self.save_teacher_option)
        button_right_box.addWidget(button_right)
        button_right_box.setAlignment(Qt.AlignRight)
        buttons.addLayout(button_left_box)
        buttons.addLayout(button_right_box)

        layout.addWidget(title)
        layout.addLayout(stack_task)
        if len(self.teacher_tasks) < 20:
            layout.addLayout(button_box)
        layout.addLayout(number_of_option)
        layout.addLayout(open_access)
        layout.addLayout(buttons)

        self.delete_items_of_layout(self.layout())
        if self.layout() is not None:
            sip.delete(self.layout())

        logging.info('Add layout in teacher option final window')
        self.setLayout(layout)
        self.adjustSize()

    def save_teacher_option(self):
        try:
            status = add_teacher_option(
                number_option=self.random_number,
                open_access=self.open_access.isChecked(),
                name_teacher=user_information['payload']['name'] + ' ' + user_information['payload']['surname'] + ' ' +
                             user_information['payload']['patronymic'],
                email_teacher=user_information['payload']['email'],
                topic=self.topic_edit.text(),
                number_of_circles=self.number_of_circles_combo.currentText(),
                procent_to_5=self.procent_of_right_for_5.text(),
                procent_to_4=self.procent_of_right_for_4.text(),
                procent_to_3=self.procent_of_right_for_3.text(),
                show_mark=self.check_box_mark.isChecked(),
                tasks=self.teacher_tasks
            )
            if status:
                QMessageBox.information(self, 'Спасибо', 'Ваш вариант успешно добавлен!\nПроверьте свою почту для\n'
                                                         'получения информации о варианте')
                self.send_email_teacher_option()
        except Exception as e:
            self.on_exception(e)

    def not_save_teacher_option(self):
        logging.info('Close event')
        reply = QMessageBox.question(self, 'Message',
                                     "Вы уверены, что не будете созранять ваш вариант?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            logging.info('User answer - YES')
            logging.info('Close app')
            self.menu()
        else:
            logging.info('User answer - NO')

    def delete_teacher_task(self, number_of_task):
        for item in self.teacher_tasks:
            if item['8-9 class']['table 8-9 class']:
                table = '8-9 class'
            elif item['10-11 class']['table 10-11 class']:
                table = '10-11 class'
            else:
                table = 'other'

            if int(item[table]['payload']['number of task']) == int(number_of_task):
                self.teacher_tasks.remove(item)
                break
        for number in range(number_of_task - 1, len(self.teacher_tasks)):
            if self.teacher_tasks[number]['8-9 class']['table 8-9 class']:
                table = '8-9 class'
            elif self.teacher_tasks[number]['10-11 class']['table 10-11 class']:
                table = '10-11 class'
            else:
                table = 'other'
            self.teacher_tasks[number][table]['payload']['number of task'] -= 1
        self.number_of_task -= 1
        self.teacher_option_final_window()

    def task_button_click(self):
        sender = self.sender()
        logging.info(f"The '{sender.text()}' button was pressed")
        self.class_of_tasks = sender.text()
        self.task_window()

    def task_window(self):
        self.delete_items_of_layout(self.layout())
        if self.layout() is not None:
            sip.delete(self.layout())

        logging.info('Topics window started')
        self.init_task()

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

    def init_task(self):
        self.number_of_task = 0
        self.right_tasks = 0
        self.right_tasks_numbers = []
        self.already_been = []
        self.new_task()

    def new_task(self):
        sender = self.sender().text()
        self.user_can_ask_a_question = True
        if sender != 'Окно задачи' and sender != 'Предпросмотр':
            self.number_of_task += 1
        self.is_new_task = True

        grid = QGridLayout()
        if self.class_of_tasks == 'preview task':
            title = QLabel('Окно задачи')
        else:
            title = QLabel(f'Задача №{str(self.number_of_task)}')
        fontTitle = QFont("Montserrat Medium", 20)
        fontTitle.setBold(True)
        title.setFont(fontTitle)
        title.setAlignment(Qt.AlignCenter)

        if self.class_of_tasks != 'preview task' and self.number_of_task != 1:
            procent_of_rigth = QLabel(f'Верно решёных - {str(self.right_tasks * 100 // (self.number_of_task - 1))} %')
            procent_of_rigth.setFont(QFont("Montserrat Medium", 14))
            grid.addWidget(procent_of_rigth, 0, 1)

        if self.class_of_tasks == 'preview task' or self.class_of_tasks == 'final preview task' or \
                self.class_of_tasks == 'teacher task':
            if self.task['8-9 class']['table 8-9 class']:
                self.info = self.task['8-9 class']['payload']
                logging.info('Task Info: ' + str(self.info))
                self.requests = {}
                self.answer_photo = 'all'
                text_task = self.get_text_task_8_9_class()

            elif self.task['10-11 class']['table 10-11 class']:
                logging.info('10-11 class')
                self.info = self.task['10-11 class']['payload']
                logging.info('Task Info: ' + str(self.info))
                text_task = self.get_text_task_10_11_class()
            else:
                logging.info('other')
                self.info = self.task['other']['payload']
                logging.info('Task Info: ' + str(self.info))
                text_task_body_split = ''
                number_of_letter = 0
                spliter = self.info['text task']
                while number_of_letter + 40 <= len(spliter) - 1:
                    row_long = 40
                    while spliter[number_of_letter + row_long] != ' ':
                        row_long -= 1
                        if row_long <= 0:
                            break
                    if number_of_letter < 0:
                        text_task_body_split += spliter[0:number_of_letter + row_long] + '\n'
                    else:
                        text_task_body_split += spliter[number_of_letter:number_of_letter + row_long] + '\n'
                    number_of_letter += row_long + 1
                try:
                    text_task_body_split += self.info['text task'][number_of_letter:]
                except IndexError:
                    pass
                text_task = QLabel(text_task_body_split)
                text_task.setFont(QFont("Montserrat Medium", 14))
            if self.class_of_tasks == 'teacher task':
                self.answer_edit = QLineEdit()
                self.answer_edit.setPlaceholderText('Введите сюда ваш ответ')
        elif self.class_of_tasks == '6-7 класс':
            QMessageBox.information(self, 'Внимание', 'Данная функция находится на стадии разработки.\n'
                                                      'Приносим извинения за неудобства.')
            self.menu()
            return
        elif self.class_of_tasks == '8-9 класс':
            task = Tests9Class(number_of_task=self.number_of_task % NUMBER_OF_TASKS_9_CLASS,
                               already_been=self.already_been)
            if task.return_task['success']:
                self.info = task.return_task['payload']
                logging.info('Task Info: ' +
                             str(self.info['options']) + ' ' +
                             str(self.info['question']) + ' ' +
                             str(self.info['answer']))

                self.requests = {}
                self.answer_photo = 'all'
                text_task = self.get_text_task_8_9_class()

            self.answer_edit = QLineEdit()
            self.answer_edit.setPlaceholderText('Введите сюда ваш ответ (только число)')
        else:
            task = Tests10Class(number_of_task=self.number_of_task % NUMBER_OF_TASKS_10_CLASS,
                                already_been=self.already_been)
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

        buttons_right = QHBoxLayout()
        buttons_right.setSpacing(10)
        buttons_right.addStretch(1)
        continue_button = QPushButton('Далее')
        continue_button.setStyleSheet("background-color: rgb(63, 137, 255)")
        exit_button = QPushButton('Завершить')
        exit_button.setStyleSheet("background-color: rgb(244, 29, 29)")
        if self.class_of_tasks == 'preview task':
            continue_button.clicked.connect(self.before_teacher_option_task_usual)
            exit_button.clicked.connect(self.before_exit_button_click)
        elif self.class_of_tasks == 'final preview task':
            continue_button.clicked.connect(self.answer_task)
            exit_button.clicked.connect(self.get_teacher_option_final_window)
        else:
            continue_button.clicked.connect(self.answer_task)
            exit_button.clicked.connect(self.exit_button_click)
        buttons_right.addWidget(exit_button)
        buttons_right.addWidget(continue_button)
        if self.class_of_tasks == 'preview task':
            buttons_left = QHBoxLayout()
            buttons_left.setSpacing(60)
            forward_button = QPushButton('Назад')
            forward_button.setStyleSheet("background-color: rgb(223, 209, 21)")
            forward_button.clicked.connect(self.teacher_option_task_usual)
            answer_button = QPushButton('Окно ответа')
            answer_button.setStyleSheet("background-color: rgb(223, 209, 21)")
            answer_button.clicked.connect(self.answer_task)
            buttons_left.addWidget(forward_button)
            buttons_left.addWidget(answer_button)

        grid.addWidget(title, 0, 0)

        if self.class_of_tasks == 'preview task' or self.class_of_tasks == 'final preview task' \
                or self.class_of_tasks == 'teacher task':
            if self.task['other']['no table']:
                grid.addWidget(text_task, 1, 0)
            else:
                grid.addLayout(text_task, 1, 0)
            if self.class_of_tasks == 'preview task':
                grid.addLayout(buttons_left, 2, 0)
            elif self.class_of_tasks != 'final preview task':
                grid.addWidget(self.answer_edit, 2, 0)
        else:
            grid.addLayout(text_task, 1, 0)
            grid.addWidget(self.answer_edit, 2, 0)
        grid.addWidget(self.overlay_photo('new', None), 1, 1)
        grid.addLayout(buttons_right, 2, 1)

        if self.layout() is not None:
            self.delete_items_of_layout(self.layout())
            sip.delete(self.layout())

        logging.info('Set layout in task')
        self.setLayout(grid)

    def get_text_task_8_9_class(self):
        text_task = QVBoxLayout()
        #text_task.addStretch(1)
        title_request = QLabel('Запросы к поисковому серверу')
        title_request.setFont(QFont('Montserrat Medium', 16))
        title_request.setAlignment(Qt.AlignCenter)
        text_task.addWidget(title_request)
        for letter, request in self.info['request'].items():
            request_text, request_number = request.split(';')
            self.requests[request_text] = request_number
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
        title_find = QLabel('Найдено страниц')
        title_request = QLabel('Запрос')
        for item in [title_request, title_find]:
            item.setFont(QFont('Montserrat Medium', 14))
            item.setFrameStyle(QFrame.Box)
        text_task.addWidget(title_request, 0, 0)
        text_task.addWidget(title_find, 0, 1)
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

    def answer_task(self):
        if self.class_of_tasks == '8-9 класс' or \
                ((self.class_of_tasks == 'preview task' or self.class_of_tasks == 'final preview task'
                  or self.class_of_tasks == 'teacher task') and
                 self.task['8-9 class']['table 8-9 class']):
            self.answer_task_9()
        else:
            self.answer_task_10()

    def answer_task_9(self):
        if self.class_of_tasks == '8-9 класс' or self.class_of_tasks == 'teacher task':
            if len(self.answer_edit.text()) < 4:
                self.on_error('В ответе должна содержаться соответствующая\nвопросу последовательность букв!')
                return

            if self.answer_edit.text().upper() == self.info['answer'].upper():
                logging.info('Right answer')
                title = QLabel('Верный ответ!')
                title.setStyleSheet("color: green")
                if self.is_new_task:
                    self.right_tasks += 1
            else:
                logging.info('Wrong answer')
                title = QLabel('Неправильный ответ!')
                title.setStyleSheet("color: red")
            self.is_new_task = False
            fontTitle = QFont("Montserrat Medium", 20)
            fontTitle.setBold(True)
            title.setFont(fontTitle)
            title.setAlignment(Qt.AlignCenter)

            decision_status = QVBoxLayout()
            decision_status.setSpacing(1)
            decision_status.addStretch(1)
            procent_of_right = self.right_tasks * 100 // self.number_of_task
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
        else:
            title = QLabel('Окно ответа')
            fontTitle = QFont("Montserrat Medium", 20)
            fontTitle.setBold(True)
            title.setFont(fontTitle)
            title.setAlignment(Qt.AlignCenter)

        grid = QGridLayout()

        explanation_block = QVBoxLayout()
        explanation_block.setSpacing(10)
        if (self.class_of_tasks == 'preview task' or self.class_of_tasks == 'final preview task') \
                and not self.info['auth explanation']:
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
            explanation_block.addWidget(exp)
        else:
            explanation = QLabel(f'Давайте рассмотрим области кругов Эйлера,\n' +
                                 f'которые покрывает каждый поисковый запрос\n' +
                                 f'и расположим их в порядке {self.info["question"]}:')
            explanation.setFont(QFont("Montserrat Medium", 14))
            explanation.setAlignment(Qt.AlignCenter)
            explanation_block.addWidget(explanation)

            explanation_grid = QGridLayout()

            row = 0
            for letter in self.info['answer']:
                let = QLabel(letter + ': ')
                let.setFont(QFont("Montserrat Medium", 14))
                let.setAlignment(Qt.AlignCenter)
                text_bnt = self.info['request'][letter].split(';')[0].split('&')
                text_bnt_with_union = text_bnt[0]
                for union_number in range(1, len(text_bnt)):
                    text_bnt_with_union += '&&' + text_bnt[union_number]
                btn = QPushButton(text_bnt_with_union)
                btn.setStyleSheet("color: blue; font: 14pt Montserrat-Medium")
                btn.clicked.connect(self.explanation_button_click)
                explanation_grid.addWidget(let, row, 0)
                explanation_grid.addWidget(btn, row, 1, 1, 5)
                row += 1
            explanation_block.addLayout(explanation_grid)

            end = QLabel(f'Получив в ответе - {self.info["answer"]}')
            end.setFont(QFont("Montserrat Medium", 14))
            end.setAlignment(Qt.AlignCenter)
            explanation_block.addWidget(end)

        if self.class_of_tasks != 'preview task' and self.class_of_tasks != 'final preview task':
            question_of_task = QLabel('Возник вопрос по заданию? Задайте его нам')
            question_of_task.setFont(QFont("Montserrat Medium", 12))
            question_of_task.setStyleSheet("text-decoration: underline; color: blue;")
            question_of_task.mousePressEvent = self.question_button_click

        buttons_right = QHBoxLayout()
        buttons_right.setSpacing(10)
        buttons_right.addStretch(1)
        continue_button = QPushButton('Продолжить')
        continue_button.setStyleSheet("background-color: rgb(63, 137, 255)")
        exit_button = QPushButton('Завершить')
        exit_button.setStyleSheet("background-color: rgb(244, 29, 29)")
        if self.class_of_tasks == 'preview task':
            continue_button.clicked.connect(self.before_teacher_option_task_usual)
            exit_button.clicked.connect(self.exit_button_click)
        elif self.class_of_tasks == 'final preview task':
            continue_button.clicked.connect(self.get_teacher_option_final_window)
            exit_button.clicked.connect(self.get_teacher_option_final_window)
        else:
            if self.class_of_tasks == 'teacher task':
                continue_button.clicked.connect(self.get_teacher_tasks)
            else:
                continue_button.clicked.connect(self.new_task)
            exit_button.clicked.connect(self.exit_button_click)
        buttons_right.addWidget(exit_button)
        buttons_right.addWidget(continue_button)
        if self.class_of_tasks == 'preview task':
            buttons_left = QHBoxLayout()
            buttons_left.setSpacing(60)
            forward_button = QPushButton('Назад')
            forward_button.setStyleSheet("background-color: rgb(223, 209, 21)")
            forward_button.clicked.connect(self.teacher_option_task_usual)
            answer_button = QPushButton('Окно задачи')
            answer_button.setStyleSheet("background-color: rgb(223, 209, 21)")
            answer_button.clicked.connect(self.new_task)
            buttons_left.addWidget(forward_button)
            buttons_left.addWidget(answer_button)

        grid.addWidget(title, 0, 0)
        grid.addLayout(explanation_block, 1, 0)
        grid.addLayout(buttons_right, 2, 1)
        grid.addWidget(self.overlay_photo('answer', self.answer_photo), 1, 1)
        if self.class_of_tasks != 'preview task' and self.class_of_tasks != 'final preview task':
            grid.addLayout(decision_status, 0, 1)
            grid.addWidget(question_of_task, 2, 0)
        elif self.class_of_tasks != 'final preview window':
            grid.addLayout(buttons_left, 2, 0)

        if self.layout() is not None:
            self.delete_items_of_layout(self.layout())
            sip.delete(self.layout())

        logging.info('Set layout in answer')
        self.setLayout(grid)

    def answer_task_10(self):
        if self.answer_edit.text() == '':
            self.on_error('Введите ответ на задачу!')
            return

        grid = QGridLayout()
        if self.class_of_tasks != 'preview task':
            try:
                if self.answer_edit.text() == str(self.info['answer']):
                    logging.info('Right answer')
                    title = QLabel('Верный ответ!')
                    title.setStyleSheet("color: green")
                    if self.is_new_task:
                        self.right_tasks += 1
                        self.right_tasks_numbers.append(self.number_of_task)
                else:
                    logging.info('Wrong answer')
                    title = QLabel('Неправильный ответ!')
                    title.setStyleSheet("color: red")
                self.is_new_task = False
                fontTitle = QFont("Montserrat Medium", 20)
                fontTitle.setBold(True)
                title.setFont(fontTitle)
                title.setAlignment(Qt.AlignCenter)
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
        else:
            title = QLabel('Окно ответа')
            fontTitle = QFont("Montserrat Medium", 20)
            fontTitle.setBold(True)
            title.setFont(fontTitle)
            title.setAlignment(Qt.AlignCenter)

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

        if self.class_of_tasks != 'preview task':
            question_of_task = QLabel('Возник вопрос по заданию? Задайте его нам')
            question_of_task.setFont(QFont("Montserrat Medium", 12))
            question_of_task.setStyleSheet("text-decoration: underline; color: blue;")
            question_of_task.mousePressEvent = self.question_button_click

        buttons_right = QHBoxLayout()
        buttons_right.setSpacing(10)
        buttons_right.addStretch(1)
        continue_button = QPushButton('Продолжить')
        continue_button.setStyleSheet("background-color: rgb(63, 137, 255)")
        exit_button = QPushButton('Завершить')
        exit_button.setStyleSheet("background-color: rgb(244, 29, 29)")
        if self.class_of_tasks == 'preview task':
            continue_button.clicked.connect(self.before_teacher_option_task_usual)
            exit_button.clicked.connect(self.exit_button_click)
        elif self.class_of_tasks == 'final preview task':
            continue_button.clicked.connect(self.get_teacher_option_final_window)
            exit_button.clicked.connect(self.get_teacher_option_final_window)
        else:
            if self.class_of_tasks == 'teacher task':
                continue_button.clicked.connect(self.get_teacher_tasks)
            else:
                continue_button.clicked.connect(self.new_task)
            exit_button.clicked.connect(self.exit_button_click)
        buttons_right.addWidget(exit_button)
        buttons_right.addWidget(continue_button)
        if self.class_of_tasks == 'preview task':
            buttons_left = QHBoxLayout()
            buttons_left.setSpacing(60)
            forward_button = QPushButton('Назад')
            forward_button.setStyleSheet("background-color: rgb(223, 209, 21)")
            forward_button.clicked.connect(self.teacher_option_task_usual)
            answer_button = QPushButton('Окно задачи')
            answer_button.setStyleSheet("background-color: rgb(223, 209, 21)")
            answer_button.clicked.connect(self.new_task)
            buttons_left.addWidget(forward_button)
            buttons_left.addWidget(answer_button)

        grid.addWidget(title, 0, 0)
        grid.addWidget(exp, 1, 0)
        grid.addLayout(buttons_right, 2, 1)
        if self.class_of_tasks != 'preview task':
            if self.class_of_tasks == 'teacher task':
                if self.task['10-11 class']['table 10-11 class']:
                    grid.addWidget(self.overlay_photo('answer', self.number_question), 1, 1)
                else:
                    grid.addWidget(self.overlay_photo('answer', self.info['sectors circles']), 1, 1)
            else:
                grid.addWidget(self.overlay_photo('answer', self.number_question), 1, 1)

            if self.class_of_tasks != 'final preview task':
                grid.addLayout(decision_status, 0, 1)
                grid.addWidget(question_of_task, 2, 0)
        else:
            if self.task['10-11 class']['table 10-11 class']:
                grid.addWidget(self.overlay_photo('answer', self.number_question), 1, 1)
            else:
                grid.addWidget(self.overlay_photo('answer', self.info['sectors circles']), 1, 1)
            grid.addLayout(buttons_left, 2, 0)

        if self.layout() is not None:
            self.delete_items_of_layout(self.layout())
            sip.delete(self.layout())

        logging.info('Set layout in answer')
        self.setLayout(grid)

    def explanation_button_click(self):
        sender = self.sender().text().split('&')
        request_text = sender[0]
        for i in range(1, len(sender)):
            if sender[i] != '':
                request_text += '&' + sender[i]
        self.answer_photo = self.requests[str(request_text)]
        self.answer_task_9()

    def before_exit_button_click(self):
        self.teacher_tasks_appended = False
        self.exit_button_click()

    def exit_button_click(self):
        logging.info('Exit button click')
        if self.class_of_tasks == 'preview task':
            text = 'создание варианта'
        else:
            text = 'тестирование'
        reply = QMessageBox.question(self, 'Message',
                                     f"Вы уверены, что хотите завершить {text}?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            logging.info('User answer - YES')
            if self.class_of_tasks == 'preview task':
                if not self.teacher_tasks_appended:
                    try:
                        self.teacher_tasks.append(self.task)
                        self.teacher_tasks_appended = True
                    except Exception as e:
                        logging.error(e)
                else:
                    self.number_of_task -= 1

                logging.info('Run to teacher option final window')
                self.teacher_option_final_window()
            elif self.class_of_tasks == 'teacher task':
                logging.info('Run to sending email teacher option')
                self.send_email_teacher_option()
            else:
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

            title = QLabel('Введите ваш вопрос в это поле')
            fontTitle = QFont("Montserrat Medium", 20)
            fontTitle.setBold(True)
            title.setFont(fontTitle)
            title.setAlignment(Qt.AlignCenter)

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
            content.addWidget(title)
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
            if self.class_of_tasks == 'teacher window':
                self.get_teacher_option_final_window()
            else:
                self.answer_task()
            return

        if self.question_edit.toPlainText() != '':
            if user_information['success']:
                add_user_question_for_task(user_information['payload']['email'],
                                           self.question_edit.toPlainText(),
                                           self.class_of_tasks,
                                           self.number_of_task)
            else:
                self.on_error('Вопрос могут задавать только\n зарегестрированные пользователи')
                return
        else:
            self.on_error('Пожалуйста, введите вопрос')
            return

        self.user_can_ask_a_question = False
        title = QLabel("Спсибо за ваш вопрос!\nВ скором времени мы вам ответим.", self)
        fontTitle = QFont("Montserrat Medium", 20)
        fontTitle.setBold(True)
        title.setFont(fontTitle)
        title.setAlignment(Qt.AlignCenter)

        btn = QPushButton('Вернуться')
        btn.setStyleSheet("background-color: rgb(223, 209, 21)")
        if self.class_of_tasks == 'teacher window':
            btn.clicked.connect(self.get_teacher_option_final_window)
        else:
            btn.clicked.connect(self.answer_task)

        self.delete_items_of_layout(self.layout())
        if self.layout() is not None:
            sip.delete(self.layout())
        box = QVBoxLayout()
        box.addWidget(title)
        box.addWidget(btn)

        self.setLayout(box)

    def overlay_photo(self, status_task, overlay):
        if self.number_of_task % NUMBER_OF_TASKS_9_CLASS != 1 or self.class_of_tasks != '10-11 класс':
            if self.class_of_tasks == '10-11 класс':
                names = [self.info['request'][i] for i in range(3)]
            else:
                names = self.info['options']
        else:
            names = self.info['request'][0].split('|')

        if status_task == 'new':
            img = Image.open('photo/taskCircles/all.png')
            if self.class_of_tasks != 'preview task' and len(self.already_been) < 12:
                self.already_been += [names]
            else:
                self.already_been = []
        else:
            if overlay == 'all' or overlay == '':
                img = Image.open('photo/taskCircles/all.png')
            elif overlay == 'four_all':
                img = Image.open('photo/taskCircles/four_all.png')
            elif overlay == 'four_center':
                img = Image.open('photo/taskCircles/four_all_grey.png')
                sector = Image.open(f'photo/taskCircles/four_center.png').convert("RGBA")
                img.paste(sector, None, sector)
            else:
                img = Image.open('photo/taskCircles/all_grey.png').convert("RGBA")
                for number_photo in overlay:
                    sector = Image.open(f'photo/taskCircles/{number_photo}.png').convert("RGBA")
                    img.paste(sector, None, sector)

        draw = ImageDraw.Draw(img)
        draw.text((65, 120), names[0], fill=(0, 0, 0),
                  font=ImageFont.truetype("fonts/Montserrat-Medium.ttf", 16))
        draw.text((250, 120), names[1], fill=(0, 0, 0),
                  font=ImageFont.truetype("fonts/Montserrat-Medium.ttf", 16))
        if overlay == 'four_all' or overlay == 'four_center':
            draw.text((65, 270), names[2], fill=(0, 0, 0),
                      font=ImageFont.truetype("fonts/Montserrat-Medium.ttf", 16))
            draw.text((250, 270), names[3], fill=(0, 0, 0),
                      font=ImageFont.truetype("fonts/Montserrat-Medium.ttf", 16))
        else:
            draw.text((150, 270), names[2], fill=(0, 0, 0),
                      font=ImageFont.truetype("fonts/Montserrat-Medium.ttf", 16))

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
