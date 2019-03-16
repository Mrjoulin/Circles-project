import logging
import requests
import random
from circles.init import Main


def check_internet_connection():
    try:
        _ = requests.get('http://216.58.192.142', timeout=5)
        connection = True
    except requests.ConnectionError:
        connection = False
    logging.info(f'Check internet connection - {str(connection)}')
    return connection


class Tests10Class(Main):
    def init(self, number_of_task):
        tests = [
            self.task_one(),
            self.task_two()
        ]
        try:
            return tests[number_of_task - 1]

            # return statements:
            # 'find': [number of pages on request]
            # 'question': question to find
            # 'answer': answer to question
            # 'explanation': explanation of task

        except Exception as e:
            logging.error('Error: ' + str(e))
            return Exception

    def task_one(self):
        # Австралия|Утконос|Коала
        find_one = random.randint(700, 1100)
        # Коала&(Австралия|Утконос)
        find_two = random.randint(50, 600)
        # Утконос|Австралия
        find_three = random.randint(50, 600)
        while find_two >= find_three:
            find_two = random.randint(50, 600)

        answer = find_one - find_three + find_two
        explanation = f'Зная, что Австралия|Утконос|Коала это {str(find_one)}, то есть все 3 окружности, тогда ' \
                      f'если мы вычтем из него Утконос|Австралия, то получим {str(find_one - find_three)}. ' \
                      f'Это будет Коала - Коала&(Австралия|Утконос). Подставив, получим что Коала равна {str(answer)}'

        return {
            'find': [find_one, find_two, find_three],
            'question': 'Коала',
            'answer': answer,
            'explanation': explanation
        }

    def task_two(self):
        # Смартфон
        find_one = random.randint(200, 800)
        # Платформа
        find_two = random.randint(200, 800)
        # Дисплей
        find_three = random.randint(200, 800)
        # Смартфон&Дисплей
        find_four = random.randint(0, 150)
        # Смартфон&Платформа
        find_five = random.randint(0, 150)
        # Дисплей&Платформа
        find_six = random.randint(0, 150)

        logical_find = [find_four, find_five, find_six]
        logical_find[random.randint(0, 2)] = 0

        answer = (find_one + find_two + find_three) - (find_four + find_five + find_six)

        if find_four == 0:
            text_find = 'Смартфон&Дисплей'
        elif find_five == 0:
            text_find = 'Смартфон&Платформа'
        else:
            text_find = 'Дисплей&Платформа'

        explanation = f'Так как {text_find} равен 0, то можно сказать, что эти 2 окружности вовсе не пересекаются.' \
                      f'Значит, чтобы найти Смартфон|Дисплей|Платформа, нужно сложить Смартфон с Платформой ' \
                      f'и с Дисплеем, а после вычесть их пересечения. Получив в ответе {str(answer)}'

        return {
            'find': [find_one, find_two, find_three, find_four, find_five, find_six],
            'question': 'Смартфон|Дисплей|Платформа',
            'answer': answer,
            'explanation': explanation
        }

    def task_three(self):
        # Гаджеты
        find_one = random.randint(200, 500)
        # Часы
        find_two = random.randint(200, 500)
        # Док-станция
        find_three = random.randint(200, 500)
        # Гаджеты|Док-станция
        find_four = random.randint(700, 1000)
        # Гаджеты|Часы
        find_five = random.randint(700, 1000)
        # Док-станция|Часы
        find_six = random.randint(700, 1000)

        logical_find = [find_four, find_five, find_six]
        sum_find = logical_find[random.randint(0, 2)]
        if sum_find == find_four:
            find_four = find_one + find_three
            text_find = 'Гаджеты|Док-станция'
            text_question = f'({text_find})&Часы'
        elif sum_find == find_five:
            find_five = find_one + find_two
            text_find = 'Гаджеты|Часы'
            text_question = f'({text_find})&Док-станция'
        else:
            find_six = find_two + find_three
            text_find = 'Док-станция|Часы'
            text_question = f'({text_find})&Гаджеты'

        answer = 2*(find_one + find_two + find_three) - find_four - find_five - find_six

        explanation = f'Зная {text_find} и численное значение каждой оркужности, можно найти их пересечение и ' \
                      f'в итоге получив 0, можно сказать, что эти 2 окружности вовсе не пересекаются. ' \
                      f'Значит, чтобы найти {text_question}, нужно сложить попарно пересекающиеся окружности ' \
                      f'и вычисть объединения этих окружностей. Получив в ответе {str(answer)}'

        return {
            'find': [find_one, find_two, find_three, find_four, find_five, find_six],
            'question': 'Смартфон|Дисплей|Платформа',
            'answer': answer,
            'explanation': explanation
        }

    def task_four(self):
        pass

    def task_five(self):
        pass

    def task_six(self):
        pass

    def task_seven(self):
        pass

    def task_eight(self):
        pass

    def task_nine(self):
        pass

    def task_ten(self):
        pass

    def task_eleven(self):
        pass

    def task_twelve(self):
        pass
