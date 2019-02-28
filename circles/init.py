import sys
import logging
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QRect, pyqtSlot, QObject
from circles.db import *

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
        # Start
        logging.info('Start Welcome window')
        self.initUI()

    def initUI(self):
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(self.backgroundRad, self.backgroundGreen, self.backgroundBlue))
        self.setPalette(p)
        logging.info(f'Set backround rgb{self.backgroundRad, self.backgroundGreen, self.backgroundBlue}')

        self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.welcome_window()

        # TODO Редизайн приложения
        # TODO Сделать дизайн остальных окон
        # TODO написать функцию - главное меню

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

        for position, name in zip(positions, infoTxt):

            label = QLabel(name, self)
            label.setAlignment(Qt.AlignCenter)
            font = QFont()

            if position[0] == 0:
                font.setFamily("Montserrat Bold")
                font.setPointSize(24)
                font.setBold(True)
            elif position[0] == 1:
                font.setFamily("Montserrat Medium")
                font.setPointSize(18)
            else:
                label.setAlignment(Qt.AlignCenter)
                font.setFamily("Montserrat Medium")
                font.setPointSize(12)

            label.setFont(font)
            info.addWidget(label, *position)

        info.addLayout(buttons, 4, 0)
        grid.addWidget(photo, 0, 0)
        grid.addItem(info, 0, 1)

        self.setLayout(grid)

    @pyqtSlot()
    def welcome_button_click(self):
        sender = self.sender()
        logging.info(f"The '{sender.text()}' button was pressed")
        if sender.text() == 'Войти':
            self.close()
            self.login()
        elif sender.text() == 'Зарегистрироваться':
            self.close()
            self.sign_up()
        else:
            self.close()
            self.menu()

    def sign_up(self):
        super().__init__()

        logging.info('Sign up window started')
        self.init_sign()
        self.setWindowTitle('Sign in')
        self.show()

    def init_sign(self):
        self.setGeometry(450, 300, 500, 300)

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

        self.setLayout(layout)

    @pyqtSlot()
    def sign_up_button_click(self):
        sender = self.sender()
        logging.info(f"The '{sender.text()}' button was pressed")
        if sender.text() == 'Отмена':
            self.close()
            self.__init__()
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
                    self.on_error('Ваш адрес эектронной почты уже зарегистрирован')
                    self.emailRegistrationEdit.setStyleSheet("background-color: rgb(255, 50, 50)")
                    error_status = True
            except Exception as e:
                self.delete_items_of_layout(self.layout())
                errorMessage = QLabel('Извините, возникла какая-то ошибка\nНажмите назад, чтобы вернуться назад', self)
                errorMessage.setAlignment(Qt.AlignCenter)
                errorMessage.setFont(QFont("Montserrat Bold", 20))
                hbox = QHBoxLayout()
                btn = QPushButton('Назад', self)
                btn.clicked.connect(self.error_button)
                hbox.addWidget(btn)
                hbox.setAlignment(Qt.AlignLeft)
                self.layout().addWidget(errorMessage)
                self.layout().addChildLayout(hbox)
                logging.error('An error has occurred:' + str(e))

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
                self.close()
                self.menu()

            except Exception as e:
                self.delete_items_of_layout(self.layout())
                errorMessage = QLabel('Извините, возникла какая-то ошибка\nНажмите назад, чтобы вернуться назад', self)
                errorMessage.setAlignment(Qt.AlignCenter)
                errorMessage.setFont(QFont("Montserrat Bold", 20))
                hbox = QHBoxLayout()
                btn = QPushButton('Назад', self)
                btn.clicked.connect(self.error_button)
                hbox.addWidget(btn)
                hbox.setAlignment(Qt.AlignLeft)
                self.layout().addWidget(errorMessage)
                self.layout().addChildLayout(hbox)
                logging.error('An error has occurred' + str(e))

    @pyqtSlot()
    def error_button(self):
        self.close()
        self.__init__()

    def login(self):
        super().__init__()

        logging.info('Login window started')
        self.init_login()
        self.setWindowTitle('Login')
        self.show()

    def init_login(self):
        self.setGeometry(450, 300, 500, 300)
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

        self.setLayout(layout)

    @pyqtSlot()
    def login_button_click(self):
        sender = self.sender()
        logging.info(f"The '{sender.text()}' button was pressed")
        if sender.text() == 'Отмена':
            self.close()
            self.__init__()
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
                    self.close()
                    self.menu()
                else:
                    self.on_error('Неверный логин и/или пароль!')
                    self.passwordLoginEdit.clear()
                    return
            except Exception as e:
                self.delete_items_of_layout(self.layout())
                errorMessage = QLabel('Извините, возникла какая-то ошибка\nНажмите назад, чтобы вернуться назад', self)
                errorMessage.setAlignment(Qt.AlignCenter)
                errorMessage.setFont(QFont("Montserrat Bold", 20))
                hbox = QHBoxLayout()
                btn = QPushButton('Назад', self)
                btn.clicked.connect(self.error_button)
                hbox.addWidget(btn)
                self.layout().addWidget(errorMessage)
                self.layout().addChildLayout(hbox)
                logging.error('An error has occurred : ' + str(e))

    def menu(self):
        super().__init__()

        logging.info('Menu window started')
        self.init_menu()
        self.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))

        self.setWindowTitle('Menu')
        self.show()

    def init_menu(self):
        self.setGeometry(300, 200, 800, 500)
        if user_information['success']:
            info = user_information['payload']
            user_status = QLabel(f"Вход выполнен {info['name']} {info['surname']} / {info['email']}")

            user_status.mousePressEvent = self.closeEvent
        else:
            user_status = QLabel('Войти | Зарегистрироваться')
            user_status.mousePressEvent = self.closeEvent
        user_status.setFont(QFont('Montserrat Medium', 16))

        teacher_option = QLabel('Для решения варианта учителя,\nвведите номер варианта')
        create_option = QLabel('Вы можете создать свой вариант')
        auth_tests = QLabel('Или выберете нужный класс для\nтренеровки решения задач')

        teacher_option.setFont(QFont('Montserrat Medium', 16))
        create_option.setFont(QFont('Montserrat Medium', 16))
        auth_tests.setFont(QFont('Montserrat Medium', 16))

        self.teacher_option_edit = QLineEdit(self)
        create_option_button = QPushButton('Создать', self)
        create_option_button.setStyleSheet("background-color: rgb(223, 209, 21)")
        create_option_button.clicked.connect(self.create_teacher_option)
        topics_for_6_7_classes = QPushButton('6-7 класс', self)
        topics_for_8_9_classes = QPushButton('8-9 класс', self)
        topics_for_10_11_classes = QPushButton('10-11 класс', self)

        for item in [topics_for_6_7_classes, topics_for_8_9_classes, topics_for_10_11_classes]:
            item.setStyleSheet("background-color: rgb(223, 209, 21)")
            item.clicked.connect(self.topics_window)

        info = [
            [
                [user_status]
            ],
            [
                [teacher_option, self.teacher_option_edit],
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
                    vbox.addWidget(val)
                hbox.addLayout(vbox)

            if items[0][0] == user_status:
                hbox.setAlignment(Qt.AlignRight)
                self.adjustSize()

            layout.addLayout(hbox)

        self.setLayout(layout)

    def create_teacher_option(self):
        pass

    def topics_window(self):
        pass

    def closeEvent(self, event):
        sender = self.sender()
        if sender is not None:
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
            logging.info('Remove items in layout')
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    self.delete_items_of_layout(item.layout())

    def on_error(self, e):
        logging.error('An error has occurred ' + str(e))
        QMessageBox().critical(self, 'Внимание!', e)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    logging.info('Start app')
    ex = Main()

    sys.exit(app.exec_())
