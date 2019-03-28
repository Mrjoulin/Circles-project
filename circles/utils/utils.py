import logging
import requests
import random
from PyQt5.QtWidgets import *
from circles.__init__ import *


def check_network_connection():
    try:
        _ = requests.get('http://216.58.192.142', timeout=5)
        connection = True
    except requests.ConnectionError:
        connection = False
    logging.info(f'Check internet connection - {str(connection)}')
    return connection


names = [
    ['Австралия', 'Утконос', 'Коала', 'Животное'],
    ['Смартфон', 'Платформа', 'Дисплей', 'Память'],
    ['Гаджеты', 'Часы', 'Док-станция', 'Наушники'],
    ['Валюта', 'Кредит', 'Рынок', 'Акции'],
    ['Модель', 'Технология', 'Патент', 'Разработчик'],
    ['Грибы', 'Рыжики', 'Фото', 'Опята'],
    ['Человек', 'Первобытный', 'Археология', 'Кости'],
    ['Суфле', 'Корзина', 'Эклер', 'Пирожное'],
    ['Стольник', 'Рында', 'Парус', 'Корабль'],
    ['Кот', 'Дом', 'Гепард', 'Вода'],
    ['Сканер', 'Принтер', 'Модем', 'Роутер'],
    ['Автомобиль', 'Мотоцикл', 'Велосипед', 'Ролики'],
    ['Клуб', 'Эмблема', 'Футбол', 'Сборная'],
    ['Страна', 'Герб', 'Флаг', 'Гимн'],
    ['Рецепт', 'Салат', 'Курица', 'Овощи'],
    ['Работа', 'Физика', 'Формула', 'Электричество'],
    ['История', 'Россия', 'Реформы', 'Империя'],
    ['Кристалл', 'Форма', 'Решетка', 'Структура'],
    ['Загрязнения', 'Экология', 'Реки', 'Проблемы'],
    ['Техника', 'Журнал', 'Каталог', 'Компьютеры'],
    ['Погода', 'Осадки', 'Прогноз', 'Солнце'],
    ['Портрет', 'Повесть', 'Гоголь', 'Рассказ'],
    ['Орёл', 'Созвездие', 'Легенда', 'Зевс'],
    ['Лего', 'Игра', 'История', 'Дети'],
    ['Мечта', 'Выбор', 'Желание', 'Действие'],
    ['Крот', 'Осязание', 'Еда', 'Земля'],
    ['Рысь', 'Добыча', 'Ареал', 'Лев']
]


class Tests9Class(QWidget):
    def __init__(self, number_of_task, already_been):
        QWidget.__init__(self)
        self.questions = ['', 'возрастания', 'убывания']

        random_name = names[random.randint(0, len(names) - 1)]
        while random_name in already_been:
            random_name = names[random.randint(0, len(names) - 1)]
        tests = [
            self.task_one(random_name),
            self.task_two(random_name),
            self.task_three(random_name),
            self.task_four(random_name),
            self.task_five(random_name),
            self.task_six(random_name),
            self.task_seven(random_name),
            self.task_eight(random_name),
            self.task_nine(random_name),
            self.task_ten(random_name),
            self.task_eleven(random_name),
            self.task_twelve(random_name),
            self.task_thirteen(random_name),
            self.task_fourteen(random_name),
            self.task_fifteen(random_name)
        ]
        try:
            logging.info(f'Search by parameters:{random_name[0]}, {random_name[1]}, {random_name[2]}, {random_name[3]}')
            self.return_task = {'success': True, 'payload': tests[number_of_task - 1]}
            # return statements:
            # 'options': names in task
            # 'request': {requests}
            # 'question': question to find
            # 'answer': answer to question
            # 'explanation': explanation of task
            # TODO create txt file to write a names and with connection of network - get updates
        except Exception as e:
            logging.error('Error: ' + str(e))
            self.return_task = {'success': False, 'payload': {}}

    def task_one(self, parms):
        index = random.choice([-1, 1])
        return {
            'options': [parms[0], parms[1], parms[2]],
            'request': {
                'А': f'{parms[0]}|{parms[1]};124567',
                'Б': f'{parms[2]}&{parms[1]};67',
                'В': f'{parms[0]};1456',
                'Г': f'{parms[2]}|{parms[1]}|{parms[0]};all'
            },
            'question': self.questions[index],
            'answer': 'БВАГ'[::index]
        }

    def task_two(self, parms):
        index = random.choice([-1, 1])
        return {
            'options': [parms[0], parms[1], parms[2]],
            'request': {
                'А': f'{parms[0]}|{parms[1]};124567',
                'Б': f'{parms[0]}|{parms[2]}|{parms[1]};all',
                'В': f'{parms[2]}&{parms[1]}&{parms[0]};6',
                'Г': f'{parms[1]}&{parms[2]};67'
            },
            'question': self.questions[index],
            'answer': 'ВГАБ'[::index]
        }

    def task_three(self, parms):
        index = random.choice([-1, 1])
        return {
            'options': [parms[0], parms[1], parms[2]],
            'request': {
                'А': f'{parms[0]}&{parms[1]};46',
                'Б': f'{parms[0]};1456',
                'В': f'{parms[0]}&{parms[1]}&{parms[2]};6',
                'Г': f'{parms[0]}|{parms[2]};134567'
            },
            'question': self.questions[index],
            'answer': 'ВАБГ'[::index]
        }

    def task_four(self, parms):
        index = random.choice([-1, 1])
        return {
            'options': [parms[0], parms[1], parms[2], parms[3]],
            'request': {
                'А': f'{parms[0]}|{parms[1]};124567',
                'Б': f'{parms[0]}&{parms[1]};46',
                'В': f'{parms[0]}|{parms[1]}|{parms[2]}|{parms[3]};four_all',
                'Г': f'{parms[0]}|{parms[1]}|{parms[2]};all'
            },
            'question': self.questions[index],
            'answer': 'БАГВ'[::index]
        }

    def task_five(self, parms):
        index = random.choice([-1, 1])
        return {
            'options': [parms[0], parms[1], parms[2], parms[3]],
            'request': {
                'А': f'{parms[0]}&{parms[1]}&{parms[2]};6',
                'Б': f'{parms[0]}&{parms[1]};46',
                'В': f'{parms[0]}|{parms[2]};134567',
                'Г': f'{parms[2]}&{parms[3]}&{parms[0]}&{parms[1]};four_center'
            },
            'question': self.questions[index],
            'answer': 'ГАБВ'[::index]
        }

    def task_six(self, parms):
        index = random.choice([-1, 1])
        return {
            'options': [parms[0], parms[1], parms[2], parms[3]],
            'request': {
                'А': f'{parms[0]}&{parms[1]}&{parms[2]}&{parms[3]};four_center',
                'Б': f'{parms[1]}|{parms[2]}|{parms[0]};all',
                'В': f'{parms[1]}|{parms[0]};124567',
                'Г': f'{parms[1]}&{parms[2]};67'
            },
            'question': self.questions[index],
            'answer': 'АГВБ'[::index]
        }

    def task_seven(self, parms):
        index = random.choice([-1, 1])
        return {
            'options': [parms[0], parms[1], parms[2]],
            'request': {
                'А': f'{parms[0]}|{parms[1]};124567',
                'Б': f'{parms[2]}&{parms[1]};67',
                'В': f'{parms[0]};1456',
                'Г': f'{parms[2]}|{parms[1]}|{parms[0]};all'
            },
            'question': self.questions[index],
            'answer': 'БВАГ'[::index]
        }

    def task_eight(self, parms):
        index = random.choice([-1, 1])
        return {
            'options': [parms[0], parms[1], parms[2]],
            'request': {
                'А': f'{parms[0]}&{parms[1]};46',
                'Б': f'{parms[0]}|{parms[2]};134567',
                'В': f'{parms[0]}&{parms[1]}&{parms[2]};6',
                'Г': f'({parms[0]}|{parms[2]})&{parms[1]};467'
            },
            'question': self.questions[index],
            'answer': 'ВАГБ'[::index]
        }

    def task_nine(self, parms):
        index = random.choice([-1, 1])
        return {
            'options': [parms[0], parms[1], parms[2]],
            'request': {
                'А': f'{parms[0]}&{parms[1]};46',
                'Б': f'{parms[0]}|{parms[2]};134567',
                'В': f'({parms[0]}|{parms[2]})&{parms[1]};467',
                'Г': f'{parms[0]}|{parms[1]}|{parms[2]};all'
            },
            'question': self.questions[index],
            'answer': 'АВБГ'[::index]
        }

    def task_ten(self, parms):
        index = random.choice([-1, 1])
        return {
            'options': [parms[0], parms[1], parms[2]],
            'request': {
                'А': f'{parms[0]}&{parms[1]};46',
                'Б': f'({parms[0]}|{parms[2]})&{parms[1]};467',
                'В': f'{parms[0]}&{parms[1]}&{parms[2]};6',
                'Г': f'{parms[0]}|{parms[2]}|{parms[1]};all'
            },
            'question': self.questions[index],
            'answer': 'ВАБГ'[::index]
        }

    def task_eleven(self, parms):
        index = random.choice([-1, 1])
        return {
            'options': [parms[0], parms[1], parms[2], parms[3]],
            'request': {
                'А': f'({parms[0]}|{parms[1]})&{parms[2]};567',
                'Б': f'{parms[0]}&{parms[1]}&{parms[2]}&{parms[3]};four_center',
                'В': f'{parms[0]}&{parms[2]};56',
                'Г': f'{parms[0]}|{parms[1]}|{parms[2]};all'
            },
            'question': self.questions[index],
            'answer': 'ВАБГ'[::index]
        }

    def task_twelve(self, parms):
        index = random.choice([-1, 1])
        return {
            'options': [parms[0], parms[1], parms[2]],
            'request': {
                'А': f'{parms[0]}|{parms[1]};124567',
                'Б': f'{parms[0]}&{parms[2]};56',
                'В': f'{parms[0]}&{parms[1]}&{parms[2]};6',
                'Г': f'({parms[0]}&{parms[2]})|{parms[1]};24567'
            },
            'question': self.questions[index],
            'answer': 'ВБГА'[::index]
        }

    def task_thirteen(self, parms):
        index = random.choice([-1, 1])
        return {
            'options': [parms[0], parms[1], parms[2]],
            'request': {
                'А': f'{parms[0]}&{parms[1]};46',
                'Б': f'({parms[0]}&{parms[1]})|{parms[2]};34567',
                'В': f'{parms[0]}|{parms[1]}|{parms[2]};all',
                'Г': f'{parms[0]}|{parms[2]};134567'
            },
            'question': self.questions[index],
            'answer': 'АБГВ'[::index]
        }

    def task_fourteen(self, parms):
        index = random.choice([-1, 1])
        return {
            'options': [parms[0], parms[1], parms[2]],
            'request': {
                'А': f'{parms[0]}&{parms[1]}&{parms[2]};6',
                'Б': f'{parms[0]}|{parms[1]}|{parms[2]};all',
                'В': f'({parms[0]}&{parms[1]})|{parms[2]};34567',
                'Г': f'{parms[0]}&{parms[1]};46'
            },
            'question': self.questions[index],
            'answer': 'АГВБ'[::index]
        }

    def task_fifteen(self, parms):
        index = random.choice([-1, 1])
        return {
            'options': [parms[0], parms[1], parms[2]],
            'request': {
                'А': f'({parms[2]}&{parms[1]})|{parms[0]};14567',
                'Б': f'{parms[0]}&{parms[1]}&{parms[2]};6',
                'В': f'{parms[0]}|{parms[1]}|{parms[2]};all',
                'Г': f'{parms[1]}|{parms[2]};234567'
            },
            'question': self.questions[index],
            'answer': 'БАГВ'[::index]
        }


class Tests10Class(QWidget):
    def __init__(self, number_of_task, already_been):
        QWidget.__init__(self)

        random_name = names[random.randint(0, len(names) - 1)]
        while random_name in already_been:
            random_name = names[random.randint(0, len(names) - 1)]
        tests = [
            self.task_one(random_name),
            self.task_two(random_name),
            self.task_three(random_name),
            self.task_four(random_name),
            self.task_five(random_name),
            self.task_six(random_name),
            self.task_seven(random_name),
            self.task_eight(random_name),
            self.task_nine(random_name)
        ]
        try:
            logging.info(f'Search by parameters: {random_name[0]}, {random_name[1]}, {random_name[2]}')
            self.return_task = {'success': True, 'payload': tests[number_of_task - 1]}
            # return statements:
            # 'request': requests of task
            # 'find': [number of pages on request]
            # 'question': question to find
            # 'answer': answer to question
            # 'explanation': explanation of task
        except Exception as e:
            logging.error('Error: ' + str(e))
            self.return_task = {'success': False, 'payload': {}}

    def task_one(self, parms):
        parm_one = parms[0]
        parm_two = parms[1]
        parm_three = parms[2]

        # parm_one|parm_two|parm_three
        find_one = random.randint(700, 1100)
        # parm_three&(parm_one|parm_two)
        find_two = random.randint(50, 600)
        # parm_two|parm_one
        find_three = random.randint(50, 600)
        while find_two >= find_three:
            find_two = random.randint(50, 600)

        answer = find_one - find_three + find_two
        explanation = f'Зная, что {parm_one}|{parm_two}|{parm_three} это {str(find_one)}, то есть все 3 окружности, ' \
                      f'тогда, если мы вычтем из него {parm_two}|{parm_one}, то получим {str(find_one - find_three)}.' \
                      f' Это будет {parm_three} - {parm_three}&({parm_one}|{parm_two}). ' \
                      f'Подставив, получим что множество {parm_three} равно {str(answer)}'

        return {
            'request': [
                f'{parm_one}|{parm_two}|{parm_three}',
                f'{parm_three}&({parm_one}|{parm_two})',
                f'{parm_two}|{parm_one}'
            ],
            'find': [find_one, find_two, find_three],
            'question': f'{parm_three};3567',
            'answer': answer,
            'explanation': explanation
        }

    def task_two(self, parms):
        parm_one = parms[0]
        parm_two = parms[1]
        parm_three = parms[2]

        # parm_one
        find_one = random.randint(200, 800)
        # parm_two
        find_two = random.randint(200, 800)
        # parm_three
        find_three = random.randint(200, 800)
        # parm_one&parm_three
        find_four = random.randint(1, 150)
        # parm_one&parm_two
        find_five = random.randint(1, 150)
        # parm_three&parm_two
        find_six = random.randint(1, 150)

        logical_find = [find_four, find_five, find_six]
        logical_find[random.randint(0, 2)] = 0

        answer = (find_one + find_two + find_three) - (find_four + find_five + find_six)

        if find_four == 0:
            text_find = f'{parm_one}&{parm_three}'
        elif find_five == 0:
            text_find = f'{parm_one}&{parm_two}'
        else:
            text_find = f'{parm_three}&{parm_two}'

        explanation = f'Так как {text_find} равен 0, то можно сказать, что эти 2 окружности вовсе не пересекаются.' \
                      f'Значит, чтобы найти {parm_one}|{parm_two}|{parm_three}, нужно сложить {parm_one} с {parm_two}' \
                      f' и с {parm_three}, а после вычесть их пересечения. Получив в ответе {str(answer)}'

        return {
            'request': [
                parm_one,
                parm_two,
                parm_three,
                f'{parm_one}&{parm_three}',
                f'{parm_one}&{parm_two}',
                f'{parm_three}&{parm_two}'
            ],
            'find': [find_one, find_two, find_three, find_four, find_five, find_six],
            'question': f'{parm_one}|{parm_two}|{parm_three};all',
            'answer': answer,
            'explanation': explanation
        }

    def task_three(self, parms):
        parm_one = parms[0]
        parm_two = parms[1]
        parm_three = parms[2]

        # parm_one
        find_one = random.randint(200, 500)
        # parm_two
        find_two = random.randint(200, 500)
        # parm_three
        find_three = random.randint(200, 500)
        # parm_one|parm_three
        find_four = find_one + find_three - random.randint(50, 150)
        # parm_one|parm_two
        find_five = find_one + find_two - random.randint(50, 150)
        # parm_three|parm_two
        find_six = find_two + find_three - random.randint(50, 150)

        logical_find = [find_four, find_five, find_six]
        sum_find = logical_find[random.randint(0, 2)]
        if sum_find == find_four:
            find_four = find_one + find_three
            text_find = f'{parm_one}|{parm_three}'
            text_question = f'({text_find})&{parm_two}'
            number_question = '467'
        elif sum_find == find_five:
            find_five = find_one + find_two
            text_find = f'{parm_one}|{parm_two}'
            text_question = f'({text_find})&{parm_three}'
            number_question = '567'
        else:
            find_six = find_two + find_three
            text_find = f'{parm_three}|{parm_two}'
            text_question = f'({text_find})&{parm_one}'
            number_question = '456'
        answer = 2*(find_one + find_two + find_three) - find_four - find_five - find_six

        explanation = f'Зная {text_find} и численное значение каждой оркужности, можно найти их пересечение и ' \
                      f'в итоге получив 0, можно сказать, что эти 2 окружности вовсе не пересекаются. ' \
                      f'Значит, чтобы найти {text_question}, нужно сложить попарно пересекающиеся окружности ' \
                      f'и вычисть объединения этих окружностей. Получив в ответе {str(answer)}'

        return {
            'request': [
                parm_one,
                parm_two,
                parm_three,
                f'{parm_one}|{parm_three}',
                f'{parm_one}|{parm_two}',
                f'{parm_three}|{parm_two}'
            ],
            'find': [find_one, find_two, find_three, find_four, find_five, find_six],
            'question': f'{text_question};{number_question}',
            'answer': answer,
            'explanation': explanation
        }

    def task_four(self, parms):
        parm_one = parms[0]
        parm_two = parms[1]
        parm_three = parms[2]

        # parm_one
        find_one = random.randint(200, 500)
        # parm_two
        find_two = random.randint(200, 500)
        # parm_three
        find_three = random.randint(200, 500)
        # parm_three|parm_one
        find_four = find_one + find_three - random.randint(50, 150)
        # parm_two&(parm_three&parm_one)
        find_five = random.randint(1, 150)
        # parm_one|parm_two
        find_six = find_one + find_two - random.randint(50, 150)

        answer = (find_one + find_two - find_six) + (find_two + find_three - find_four) - find_five

        explanation = f'Зная {parm_three}|{parm_one} и {parm_one}|{parm_two}, а также численное значение каждой ' \
                      f'оркужности, можно найти их пересечения. Они будут равны соответственно ' \
                      f'{find_one + find_two - find_six} и {find_two + find_three - find_four}. Значит, чтобы найти ' \
                      f'{parm_one}&({parm_three}|{parm_two}), нужно сложить эти пересечения и вычесть пересечени всех' \
                      f' окружностей, то есть {parm_two}&({parm_three}&{parm_one}). Получив в ответе {str(answer)}'

        return {
            'request': [
                parm_one,
                parm_two,
                parm_three,
                f'{parm_three}|{parm_one}',
                f'{parm_two}&({parm_three}&{parm_one})',
                f'{parm_one}|{parm_two}'
            ],
            'find': [find_one, find_two, find_three, find_four, find_five, find_six],
            'question': f'{parm_one}&({parm_three}|{parm_two});456',
            'answer': answer,
            'explanation': explanation
        }

    def task_five(self, parms):
        parm_one = parms[0]
        parm_two = parms[1]
        parm_three = parms[2]

        # parm_one
        find_one = random.randint(200, 500)
        # parm_two
        find_two = random.randint(200, 500)
        # parm_three
        find_three = random.randint(200, 500)
        # parm_three|parm_one
        find_four = find_one + find_three - random.randint(50, 150)
        # parm_two&(parm_three|parm_one)
        find_five = random.randint(100, 200)
        # parm_three&(parm_one|parm_two)
        find_six = random.randint(100, 200)

        answer = (find_one + find_two) - (find_five - (find_six - (find_one + find_three - find_four)))

        explanation = f'Зная {parm_three}|{parm_one} и численное значение каждой оркужности, можно найти их ' \
                      f'пересечения и это будет {find_one + find_three - find_four}. Далее найдём {parm_two}&' \
                      f'{parm_one}: {parm_two}&({parm_three}|{parm_one}) - ({parm_three}&({parm_one}|{parm_two}) - ' \
                      f'{parm_three}&{parm_one}. Значит, чтобы найти {parm_one}|{parm_two}' \
                      f' - нужно вычесть пересечение этих кругой из из суммы. Получив в ответе {str(answer)}'

        return {
            'request': [
                parm_one,
                parm_two,
                parm_three,
                f'{parm_three}|{parm_one}',
                f'{parm_two}&({parm_three}|{parm_one})',
                f'{parm_three}&({parm_one}|{parm_two})'
            ],
            'find': [find_one, find_two, find_three, find_four, find_five, find_six],
            'question': f'{parm_one}|{parm_two};124567',
            'answer': answer,
            'explanation': explanation
        }

    def task_six(self, parms):
        parm_one = parms[0]
        parm_two = parms[1]
        parm_three = parms[2]

        # parm_one
        find_one = random.randint(200, 500)
        # parm_two
        find_two = random.randint(200, 500)
        # Фото
        find_three = random.randint(200, 500)
        # parm_two|parm_three
        find_four = find_two + find_three - random.randint(50, 150)
        # parm_one&parm_three
        find_five = random.randint(100, 150)
        # (parm_two|parm_three)&parm_one
        find_six = find_five + random.randint(1, 50)

        answer = (find_six - find_five) + (find_two + find_three - find_four)

        explanation = f'Зная ({parm_two}|{parm_three})&{parm_one} и {parm_one}&{parm_three}, можно найти их разницу ' \
                      f'и это будет {find_six - find_five}. Далее найдём {parm_two}&{parm_three}, вычев из суммы ' \
                      f'{parm_two} и {parm_three} их объединение, получив {find_two + find_three - find_four}. Далее,' \
                      f' чтобы получить ({parm_one}|{parm_three})&{parm_two} - просто сложим {parm_two}&{parm_three}' \
                      f' и разницу, полученную в начале. Получив в ответе {str(answer)}'

        return {
            'request': [
                parm_one,
                parm_two,
                parm_three,
                f'{parm_two}|{parm_three}',
                f'{parm_one}&{parm_three}',
                f'({parm_two}|{parm_three})&{parm_one}'
            ],
            'find': [find_one, find_two, find_three, find_four, find_five, find_six],
            'question': f'({parm_one}|{parm_three})&{parm_two};467',
            'answer': answer,
            'explanation': explanation
        }

    def task_seven(self, parms):
        parm_one = parms[0]
        parm_two = parms[1]
        parm_three = parms[2]

        # parm_one
        find_one = random.randint(400, 800)
        # parm_two
        find_two = random.randint(400, 800)
        # parm_three
        find_three = random.randint(400, 800)
        # Рандомный 0 в пересечении или сумма в объединение
        random_zero = random.randint(0, 2)
        text_question = ''
        # parm_one|parm_three
        if random_zero == 0:
            # 0 - так как при дальнейшем решении понадобятся пересечения и для упрощения кода легче взять его
            find_four = 0
            text_find = f'{parm_one}|{parm_three}'
            text_question = f'({parm_one}|{parm_three})&{parm_two}'
            number_question = '467'
        else:
            find_four = find_one + find_three - random.randint(50, 300)
        # parm_one&parm_two
        if random_zero == 1:
            find_five = 0
            text_find = f'{parm_one}&{parm_two}'
            text_question = f'({parm_one}|{parm_two})&{parm_three}'
            number_question = '567'
        else:
            find_five = random.randint(100, 300)
        # parm_three&parm_two
        if random_zero == 2:
            find_six = 0
            text_find = f'{parm_three}&{parm_two}'
            text_question = f'({parm_three}|{parm_two})&{parm_one}'
            number_question = '456'
        else:
            find_six = random.randint(100, 300)

        answer = find_four + find_five + find_six

        if random_zero == 0:
            cliche_intro = f'Так как {text_find} равен сумме двух его состовляющих окружностей'
            cliche_decision = 'сложить остальные 2 пересечения'
        else:
            cliche_intro = f'Зная, что {text_find} равен 0'
            cliche_decision = f'найти {parm_one}&{parm_three}: Человек + Археология - Человек|Археология, а после ' \
                              f'сложить с оставшимся пересечением'

        explanation = f'{cliche_intro}, то можно сказать, что эти 2 окружности вовсе не пересекаются.' \
                      f'Значит, чтобы найти {text_question}, нужно {cliche_decision}. ' \
                      f'Получив в ответе {str(answer)}'
        return {
            'request': [
                parm_one,
                parm_two,
                parm_three,
                f'{parm_one}|{parm_three}',
                f'{parm_one}&{parm_two}',
                f'{parm_three}&{parm_two}'
            ],
            'find': [find_one, find_two, find_three, find_four, find_five, find_six],
            'question': f'{text_question};{number_question}',
            'answer': answer,
            'explanation': explanation
        }

    def task_eight(self, parms):
        parm_one = parms[0]
        parm_two = parms[1]
        parm_three = parms[2]

        # parm_one
        find_one = random.randint(400, 800)
        # parm_two
        find_two = random.randint(400, 800)
        # parm_three
        find_three = random.randint(400, 800)
        # parm_one&parm_two
        find_four = random.randint(50, 300)
        # parm_one&parm_three
        find_five = random.randint(50, 300)
        # parm_two&parm_three
        find_six = random.randint(50, 300)

        logical_find = [find_four, find_five, find_six]
        logical_find[random.randint(0, 2)] = 0

        answer = (find_one + find_two + find_three) - (find_four + find_five + find_six)

        if find_four == 0:
            text_find = f'{parm_one}&{parm_two}'
        elif find_five == 0:
            text_find = f'{parm_one}&{parm_three}'
        else:
            text_find = f'{parm_two}&{parm_three}'

        explanation = f'Так как {text_find} равен 0, то можно сказать, что эти 2 окружности вовсе не пересекаются.' \
                      f'Значит, чтобы найти {parm_one}|{parm_two}|{parm_three}, нужно сложить {parm_one} с {parm_two}' \
                      f' и с {parm_three}, а после вычесть их пересечения. Получив в ответе {str(answer)}'

        return {
            'request': [
                parm_one,
                parm_two,
                parm_three,
                f'{parm_one}&{parm_two}',
                f'{parm_one}&{parm_three}',
                f'{parm_two} & {parm_three}'
            ],
            'find': [find_one, find_two, find_three, find_four, find_five, find_six],
            'question': f'{parm_one}|{parm_two}|{parm_three};1234567',
            'answer': answer,
            'explanation': explanation
        }

    def task_nine(self, parms):
        parm_one = parms[0]
        parm_two = parms[1]
        parm_three = parms[2]

        # parm_one
        find_one = random.randint(400, 800)
        # parm_two
        find_two = random.randint(400, 800)
        # parm_three
        find_three = random.randint(400, 800)
        # parm_one&parm_two
        find_four = random.randint(50, 300)
        # parm_one&parm_three
        find_five = random.randint(50, 300)
        # parm_one|parm_two|parm_three
        find_six = find_one + find_two + find_three - random.randint(200, 500)

        logical_find = [find_four, find_five]
        logical_find[random.randint(0, 1)] = 0

        answer = (find_one + find_two + find_three) - (find_four + find_five + find_six)

        if find_four == 0:
            text_find = f'{parm_one}&{parm_two}'
        else:
            text_find = f'{parm_one}&{parm_three}'

        explanation = f'Так как {text_find} равен 0, то можно сказать, что эти 2 окружности вовсе не пересекаются.' \
                      f'Значит, чтобы найти {parm_three}&{parm_two}, нужно вычесть из суммы всех 3-х множеств их ' \
                      f'объединение и оставшеесе пересечение окружностей. Получив в ответе {str(answer)}'

        return {
            'request': [
                parm_one,
                parm_two,
                parm_three,
                f'{parm_one}&{parm_two}',
                f'{parm_one}&{parm_three}',
                f'{parm_one}|{parm_two}|{parm_three}'
            ],
            'find': [find_one, find_two, find_three, find_four, find_five, find_six],
            'question': f'{parm_three}&{parm_two};67',
            'answer': answer,
            'explanation': explanation
        }
