import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt


class Main(QWidget):

    def __init__(self):
        super().__init__()

        self.init()

    def init(self):
        grid = QGridLayout()
        grid.setSpacing(10)

        names = ['6-7 класс', '8 - 9 класс', '10 - 11 класс',
                 'Задачи низкого уровня сложности\n\nA | B = A + B - A & B',
                 'Задачи среднего уровня сложности\n\nУбывание/вострастание\nколичества найденных страниц',
                 'Задачи высокого уровня сложности\n\nЗадание №17 ЕГЭ',
                 'eiler-2.jpg', 'eiler-3.jpg', '17_EGЕ.png']

        positions = [(i, j) for i in range(3) for j in range(3)]

        for position, name in zip(positions, names):
            if position[0] == 0:
                button = QPushButton(name, self)
                grid.addWidget(button, *position)
                button.clicked.connect(self.tasks_window)
            elif position[0] == 1:
                label = QLabel(name)
                grid.addWidget(label, *position)
            else:
                label = QLabel(self)
                pixmap = QPixmap(name)
                smaller_pixmap = pixmap.scaled(256, 256, Qt.KeepAspectRatio, Qt.FastTransformation)
                label.setPixmap(smaller_pixmap)
                grid.addWidget(label, *position)

        self.setLayout(grid)

        self.resize(500, 300)
        self.center()
        self.setWindowTitle('Euler circles')
        self.show()

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def tasks_window(self):
        self.show()
        # number of task
        # text | picture
        # entry field


#class Tasks(Main):
#    def __init__(self):
#        super().__init__()
#
 #       self.init()
#
 #   def init(self):
#        self.resize(500, 300)
#        self.setWindowTitle('Euler circles')
#        self.show() */


if __name__ == '__main__':

    app = QApplication(sys.argv)

    ex = Main()

    sys.exit(app.exec_())
