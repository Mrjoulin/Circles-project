import logging
import requests
import random
from circles.init import Main


def check_network_connection():
    try:
        _ = requests.get('http://216.58.192.142', timeout=5)
        connection = True
    except requests.ConnectionError:
        connection = False
    logging.info(f'Check internet connection - {str(connection)}')
    return connection


class Tests10Class(Main):
    def __init__(self, number_of_task):
        super().__init__()
        names = [
            ['Австралия', 'Утконос', 'Коала'],
            ['Смартфон', 'Платформа', 'Дисплей'],
            ['Гаджеты', 'Часы', 'Док-станция'],
            ['Валюта', 'Кредит', 'Рынок'],
            ['Модель', 'Технология', 'Патент'],
            ['Грибы', 'Рыжики', 'Фото'],
            ['Человек', 'Первобытный', 'Археология'],
            ['Суфле', 'Корзина', 'Эклер'],
            ['Стольник', 'Рында', 'Парус'],
            ['Кот', 'Дикий', 'Гепард'],
            ['Сканер', 'Принтер', 'Модем'],
            ['Автомобиль', 'Мотоцикл', 'Велосипед']
        ]
        tests = [
            self.task_one(*names[random.randint(0, len(names) - 1)]),
            self.task_two(*names[random.randint(0, len(names) - 1)]),
            self.task_three(*names[random.randint(0, len(names) - 1)]),
            self.task_four(*names[random.randint(0, len(names) - 1)]),
            self.task_five(*names[random.randint(0, len(names) - 1)]),
            self.task_six(*names[random.randint(0, len(names) - 1)]),
            self.task_seven(*names[random.randint(0, len(names) - 1)]),
            self.task_eight(*names[random.randint(0, len(names) - 1)]),
            self.task_nine(*names[random.randint(0, len(names) - 1)]),
        ]
        try:
            self.return_task = {'success': True, 'payload': tests[number_of_task - 1]}
            # return statements:
            # 'request': requests of task
            # 'find': [number of pages on request]
            # 'question': question to find
            # 'answer': answer to question
            # 'explanation': explanation of task
            # TODO create txt file to write a names and with connection of network - get updates
            # TODO write the names in the array and pass them in the parameters to the unique task
        except Exception as e:
            logging.error('Error: ' + str(e))
            self.return_task = {'success': False, 'payload': {}}

    def task_one(self, parm_one, parm_two, parm_three):
        logging.info('Search by parameters: ' + parm_one + parm_two + parm_three)
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
            'question': parm_three,
            'answer': answer,
            'explanation': explanation
        }

    def task_two(self, parm_one, parm_two, parm_three):
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
            'question': f'{parm_one}|{parm_two}|{parm_three}',
            'answer': answer,
            'explanation': explanation
        }

    def task_three(self, parm_one, parm_two, parm_three):
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
        elif sum_find == find_five:
            find_five = find_one + find_two
            text_find = f'{parm_one}|{parm_two}'
            text_question = f'({text_find})&{parm_three}'
        else:
            find_six = find_two + find_three
            text_find = f'{parm_three}|{parm_two}'
            text_question = f'({text_find})&{parm_one}'

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
            'question': text_question,
            'answer': answer,
            'explanation': explanation
        }

    def task_four(self, parm_one, parm_two, parm_three):
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
            'question': f'{parm_one}&({parm_three}|{parm_two})',
            'answer': answer,
            'explanation': explanation
        }

    def task_five(self, parm_one, parm_two, parm_three):
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
            'question': f'{parm_one}|{parm_two}',
            'answer': answer,
            'explanation': explanation
        }

    def task_six(self, parm_one, parm_two, parm_three):
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
            'question': f'({parm_one}|{parm_three})&{parm_two}',
            'answer': answer,
            'explanation': explanation
        }

    def task_seven(self, parm_one, parm_two, parm_three):
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
        else:
            find_four = find_one + find_three - random.randint(50, 300)
        # parm_one&parm_two
        if random_zero == 1:
            find_five = 0
            text_find = f'{parm_one}&{parm_two}'
            text_question = f'({parm_one}|{parm_two})&{parm_three}'
        else:
            find_five = random.randint(100, 300)
        # parm_three&parm_two
        if random_zero == 2:
            find_six = 0
            text_find = f'{parm_three}&{parm_two}'
            text_question = f'({parm_three}|{parm_two})&{parm_one}'
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
            'question': text_question,
            'answer': answer,
            'explanation': explanation
        }

    def task_eight(self, parm_one, parm_two, parm_three):
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
            'question': f'{parm_one}|{parm_two}|{parm_three}',
            'answer': answer,
            'explanation': explanation
        }

    def task_nine(self, parm_one, parm_two, parm_three):
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
            'question': f'{parm_three}&{parm_two}',
            'answer': answer,
            'explanation': explanation
        }
