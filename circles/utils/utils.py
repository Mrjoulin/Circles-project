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
        names = [
            ['Австралия', 'Утконос', 'Коала'],
            ['Смартфон',  'Платформа', 'Дисплей'],
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
            return tests[number_of_task - 1]

            # return statements:
            # 'find': [number of pages on request]
            # 'question': question to find
            # 'answer': answer to question
            # 'explanation': explanation of task
            # TODO write the names in the array and pass them in the parameters to the unique task
        except Exception as e:
            logging.error('Error: ' + str(e))
            return Exception

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
        # parm_tree
        find_three = random.randint(200, 800)
        # parm_one&parm_tree
        find_four = random.randint(1, 150)
        # parm_one&parm_two
        find_five = random.randint(1, 150)
        # parm_tree&parm_two
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
            'find': [find_one, find_two, find_three, find_four, find_five, find_six],
            'question': f'{parm_one}|{parm_two}|{parm_three}',
            'answer': answer,
            'explanation': explanation
        }

    def task_three(self, parm_one, parm_two, parm_three):
        # Гаджеты
        find_one = random.randint(200, 500)
        # Часы
        find_two = random.randint(200, 500)
        # Док-станция
        find_three = random.randint(200, 500)
        # Гаджеты|Док-станция
        find_four = find_one + find_three - random.randint(50, 150)
        # Гаджеты|Часы
        find_five = find_one + find_two - random.randint(50, 150)
        # Док-станция|Часы
        find_six = find_two + find_three - random.randint(50, 150)

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
            'question': text_question,
            'answer': answer,
            'explanation': explanation
        }

    def task_four(self, parm_one, parm_two, parm_three):
        # Валюта
        find_one = random.randint(200, 500)
        # Кредит
        find_two = random.randint(200, 500)
        # Рынок
        find_three = random.randint(200, 500)
        # Рынок|Валюта
        find_four = find_one + find_three - random.randint(50, 150)
        # Кредит&(Рынок&Валюта)
        find_five = random.randint(1, 150)
        # Валюта|Кредит
        find_six = find_one + find_two - random.randint(50, 150)

        answer = (find_one + find_two - find_six) + (find_two + find_three - find_four) - find_five

        explanation = f'Зная Рынок|Валюта и Валюта|Кредит, а также численное значение каждой оркужности, ' \
                      f'можно найти их пересечения. Они будут равны соответственно {find_one + find_two - find_six}' \
                      f'и {find_two + find_three - find_four}. Значит, чтобы найти Валюта&(Рынок|Кредит), нужно ' \
                      f'сложить эти пересечения и вычесть пересечени всех окружностей, ' \
                      f'то есть Кредит&(Рынок&Валюта). Получив в ответе {str(answer)}'

        return {
            'find': [find_one, find_two, find_three, find_four, find_five, find_six],
            'question': 'Валюта&(Рынок|Кредит)',
            'answer': answer,
            'explanation': explanation
        }

    def task_five(self, parm_one, parm_two, parm_three):
        # Модель
        find_one = random.randint(200, 500)
        # Технология
        find_two = random.randint(200, 500)
        # Патент
        find_three = random.randint(200, 500)
        # Патент|Модель
        find_four = find_one + find_three - random.randint(50, 150)
        # Технология&(Патент|Модель)
        find_five = random.randint(100, 200)
        # Патент&(Модель|Технология)
        find_six = random.randint(100, 200)

        answer = (find_one + find_two) - (find_five - (find_six - (find_one + find_three - find_four)))

        explanation = f'Зная Патент|Модель и численное значение каждой оркужности, можно найти их пересечения и это ' \
                      f'будет {find_one + find_three - find_four}. Далее найдём Технология&Модель: Технология&(Патент' \
                      f'|Модель) - (Патент&(Модель|Технология) - Патент&Модель. Значит, чтобы найти Модель|Технология' \
                      f' - нужно вычесть пересечение этих кругой из из суммы. Получив в ответе {str(answer)}'

        return {
            'find': [find_one, find_two, find_three, find_four, find_five, find_six],
            'question': 'Модель|Технология',
            'answer': answer,
            'explanation': explanation
        }

    def task_six(self, parm_one, parm_two, parm_three):
        # Грибы
        find_one = random.randint(200, 500)
        # Рыжики
        find_two = random.randint(200, 500)
        # Фото
        find_three = random.randint(200, 500)
        # Рыжики|Фото
        find_four = find_two + find_three - random.randint(50, 150)
        # Грибы&Фото
        find_five = random.randint(100, 150)
        # (Рыжики|Фото)&Грибы
        find_six = find_five + random.randint(1, 50)

        answer = (find_six - find_five) + (find_two + find_three - find_four)

        explanation = f'Зная (Рыжики|Фото)&Грибы и Грибы&Фото, можно найти их разницу и это будет ' \
                      f'{find_six - find_five}. Далее найдём Рыжики&Фото, вычев из суммы Рыжиков и Фото их объединени' \
                      f'е, получив {find_two + find_three - find_four}. Далее, чтобы получить (Грибы|Фото)&Рыжики - ' \
                      f'просто сложим Рыжики&Фото и разницу, полученную в начале. Получив в ответе {str(answer)}'

        return {
            'find': [find_one, find_two, find_three, find_four, find_five, find_six],
            'question': '(Грибы|Фото)&Рыжики',
            'answer': answer,
            'explanation': explanation
        }

    def task_seven(self, parm_one, parm_two, parm_three):
        # Человек
        find_one = random.randint(400, 800)
        # Первобытный
        find_two = random.randint(400, 800)
        # Археология
        find_three = random.randint(400, 800)
        # Рандомный 0 в пересечении или сумма в объединение
        random_zero = random.randint(0, 2)
        text_question = ''
        # Человек|Археология
        if random_zero == 0:
            # 0 - так как при дальнейшем решении понадобятся пересечения и для упрощения кода легче взять его
            find_four = 0
            text_find = 'Человек|Археология'
            text_question = '(Человек|Археология)&Первобытный'
        else:
            find_four = find_one + find_three - random.randint(50, 300)
        # Человек&Первобытный
        if random_zero == 1:
            find_five = 0
            text_find = 'Человек&Первобытный'
            text_question = '(Человек|Первобытный)&Археология'
        else:
            find_five = random.randint(100, 300)
        # Археология&Первобытный
        if random_zero == 2:
            find_six = 0
            text_find = 'Археология&Первобытный'
            text_question = '(Археология|Первобытный)&Человек'
        else:
            find_six = random.randint(100, 300)

        answer = find_four + find_five + find_six

        if random_zero == 0:
            cliche_intro = f'Так как {text_find} равен сумме двух его состовляющих окружностей'
            cliche_decision = 'сложить остальные 2 пересечения'
        else:
            cliche_intro = f'Зная, что {text_find} равен 0'
            cliche_decision = 'найти Человек&Археология: Человек + Археология - Человек|Археология, а после сложить ' \
                              'с оставшимся пересечением'

        explanation = f'{cliche_intro}, то можно сказать, что эти 2 окружности вовсе не пересекаются.' \
                      f'Значит, чтобы найти {text_question}, нужно {cliche_decision}. ' \
                      f'Получив в ответе {str(answer)}'
        return {
            'find': [find_one, find_two, find_three, find_four, find_five, find_six],
            'question': text_question,
            'answer': answer,
            'explanation': explanation
        }

    def task_eight(self, parm_one, parm_two, parm_three):
        # Суфле
        find_one = random.randint(400, 800)
        # Корзина
        find_two = random.randint(400, 800)
        # Эклер
        find_three = random.randint(400, 800)
        # Суфле&Корзина
        find_four = random.randint(50, 300)
        # Суфле&Эклер
        find_five = random.randint(50, 300)
        # Корзина&Эклер
        find_six = random.randint(50, 300)

        logical_find = [find_four, find_five, find_six]
        logical_find[random.randint(0, 2)] = 0

        answer = (find_one + find_two + find_three) - (find_four + find_five + find_six)

        if find_four == 0:
            text_find = 'Суфле&Корзина'
        elif find_five == 0:
            text_find = 'Суфле&Эклер'
        else:
            text_find = 'Корзина&Эклер'

        explanation = f'Так как {text_find} равен 0, то можно сказать, что эти 2 окружности вовсе не пересекаются.' \
                      f'Значит, чтобы найти Суфле|Корзина|Эклер, нужно сложить Суфле с Корзиной ' \
                      f'и с Эклерем, а после вычесть их пересечения. Получив в ответе {str(answer)}'

        return {
            'find': [find_one, find_two, find_three, find_four, find_five, find_six],
            'question': 'Суфле|Корзина|Эклер',
            'answer': answer,
            'explanation': explanation
        }

    def task_nine(self, parm_one, parm_two, parm_three):
        # Стольник
        find_one = random.randint(400, 800)
        # Рында
        find_two = random.randint(400, 800)
        # Парус
        find_three = random.randint(400, 800)
        # Стольник&Рында
        find_four = random.randint(50, 300)
        # Стольник&Парус
        find_five = random.randint(50, 300)
        # Стольник|Рында|Парус
        find_six = find_one + find_two + find_three - random.randint(200, 500)

        logical_find = [find_four, find_five]
        logical_find[random.randint(0, 1)] = 0

        answer = (find_one + find_two + find_three) - (find_four + find_five + find_six)

        if find_four == 0:
            text_find = 'Стольник&Рында'
        else:
            text_find = 'Корзина&Эклер'

        explanation = f'Так как {text_find} равен 0, то можно сказать, что эти 2 окружности вовсе не пересекаются.' \
                      f'Значит, чтобы найти Парус&Рында, нужно вычесть из суммы всех 3-х множеств их объединение и ' \
                      f'оставшеесе пересечение окружностей. Получив в ответе {str(answer)}'

        return {
            'find': [find_one, find_two, find_three, find_four, find_five, find_six],
            'question': 'Парус&Рында',
            'answer': answer,
            'explanation': explanation
        }
