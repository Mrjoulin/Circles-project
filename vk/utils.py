from vk_api.keyboard import VkKeyboard, VkKeyboardColor


class Testing(object):
    def __init__(self, number, user_id, api, cnt):
        self.number = number
        self.user_id = user_id
        self.api = api
        self.cnt = cnt

    def test(self):
        number = self.number
        api = self.api
        user_id = self.user_id
        cnt = self.cnt
        msg = 'Отправьте мне ответ'
        if number == 2:
            api.messages.send(user_id=user_id, message=QuestionTwo(cnt[2]).test()[0] + msg, keyboard=self.text())
            answer = QuestionTwo(cnt[2]).test()[1]
        elif number == 3:
            api.messages.send(user_id=user_id, message=QuestionThree(cnt[3]).test()[0] + msg, keyboard=self.text())
            answer = QuestionThree(cnt[2]).test()[1]
        elif number == 4:
            api.messages.send(user_id=user_id, message=QuestionFour(cnt[4]).test()[0] + msg, keyboard=self.text())
            answer = QuestionFour(cnt[2]).test()[1]
        elif number == 5:
            api.messages.send(user_id=user_id, message=QuestionFive(cnt[5]).test()[0] + msg, keyboard=self.text())
            answer = QuestionFive(cnt[2]).test()[1]
        elif number == 6:
            api.messages.send(user_id=user_id, message=QuestionSix(cnt[6]).test()[0] + msg, keyboard=self.text())
            answer = QuestionSix(cnt[2]).test()[1]
        elif number == 7:
            api.messages.send(user_id=user_id, message=QuestionSeven(cnt[7]).test()[0] + msg, keyboard=self.text())
            answer = QuestionSeven(cnt[2]).test()[1]
        elif number == 8:
            api.messages.send(user_id=user_id, message=QuestionEight(cnt[8]).test()[0] + msg, keyboard=self.text())
            answer = QuestionEight(cnt[2]).test()[1]
        elif number == 9:
            api.messages.send(user_id=user_id, message=QuestionNine(cnt[9]).test()[0] + msg, keyboard=self.text())
            answer = QuestionNine(cnt[2]).test()[1]
        elif number == 10:
            api.messages.send(user_id=user_id, message=QuestionTen(cnt[10]).test()[0] + msg, keyboard=self.text())
            answer = QuestionTen(cnt[2]).test()[1]
        elif number == 11:
            api.messages.send(user_id=user_id, message=QuestionEleven(cnt[11]).test()[0] + msg, keyboard=self.text())
            answer = QuestionEleven(cnt[2]).test()[1]
        elif number == 12:
            api.messages.send(user_id=user_id, message=QuestionTwelve(cnt[12]).test()[0] + msg, keyboard=self.text())
            answer = QuestionTwelve(cnt[2]).test()[1]
        elif number == 13:
            api.messages.send(user_id=user_id, message=QuestionThirteen(cnt[13]).test()[0] + msg, keyboard=self.text())
            answer = QuestionThirteen(cnt[2]).test()[1]
        elif number == 14:
            api.messages.send(user_id=user_id, message=QuestionFourteen(cnt[14]).test()[0] + msg, keyboard=self.text())
            answer = QuestionFourteen(cnt[2]).test()[1]

        while True:
            message = (yield).text
            if message == 'Показать текст':

                api.messages.send(user_id=user_id, message=Text(cnt[number]).test() + msg)
            elif message == 'Вернуться назад':
                break
            else:
                api.messages.send(user_id=user_id, message='Пожалуйста, выберете конпку на клавиатуре')

                for j in range(3):
                    message = (yield).text
                    if message == answer:
                        api.messages.send(user_id=user_id, message='Правильный ответ!')
                    else:
                        if j < 2:
                            api.messages.send(user_id=user_id,
                                              message='Неверный ответ!\nПрочтите внимательно '
                                                      'задание и попробуйте ещё раз, ')
                        else:
                            api.messages.send(user_id=user_id,
                                              message='Неверный ответ!\nВам следует больше '
                                                      'тренироваться ')

        if cnt[number] + 1 < 10:
            cnt[number] += 1
        else:
            cnt[number] = 1

    def text(self):
        keyboard = VkKeyboard(one_time=False)
        keyboard.add_button('Показать текст', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button('Вернуться назад', color=VkKeyboardColor.NEGATIVE)
        return keyboard.get_keyboard()


class QuestionTwo(object):
    def __init__(self, number):
        self.number = int(number)

    def test(self):
        if self.number == 1:
            s = ["test 1", 'answer 1']
        elif self.number == 2:
            s = ["test 2", 'answer 2']
        elif self.number == 3:
            s = ["test 3", 'answer 3']
        elif self.number == 4:
            s = ["test 4", 'answer 4']
        elif self.number == 5:
            s = ["test 5", 'answer 5']
        elif self.number == 6:
            s = ["test 6", 'answer 6']
        elif self.number == 7:
            s = ["test 7", 'answer 7']
        elif self.number == 8:
            s = ["test 8", 'answer 8']
        elif self.number == 9:
            s = ["test 9", 'answer 9']
        elif self.number == 10:
            s = ["test 10", 'answer 10']
        else:
            s = ['error']
        return s


class QuestionThree(object):
    def __init__(self, number):
        self.number = int(number)

    def test(self):
        if self.number == 1:
            s = ["test 1", 'answer 1']
        elif self.number == 2:
            s = ["test 2", 'answer 2']
        elif self.number == 3:
            s = ["test 3", 'answer 3']
        elif self.number == 4:
            s = ["test 4", 'answer 4']
        elif self.number == 5:
            s = ["test 5", 'answer 5']
        elif self.number == 6:
            s = ["test 6", 'answer 6']
        elif self.number == 7:
            s = ["test 7", 'answer 7']
        elif self.number == 8:
            s = ["test 8", 'answer 8']
        elif self.number == 9:
            s = ["test 9", 'answer 9']
        elif self.number == 10:
            s = ["test 10", 'answer 10']
        else:
            s = ['error']
        return s


class QuestionFour(object):
    def __init__(self, number):
        self.number = int(number)

    def test(self):
        if self.number == 1:
            s = ["test 1", 'answer 1']
        elif self.number == 2:
            s = ["test 2", 'answer 2']
        elif self.number == 3:
            s = ["test 3", 'answer 3']
        elif self.number == 4:
            s = ["test 4", 'answer 4']
        elif self.number == 5:
            s = ["test 5", 'answer 5']
        elif self.number == 6:
            s = ["test 6", 'answer 6']
        elif self.number == 7:
            s = ["test 7", 'answer 7']
        elif self.number == 8:
            s = ["test 8", 'answer 8']
        elif self.number == 9:
            s = ["test 9", 'answer 9']
        elif self.number == 10:
            s = ["test 10", 'answer 10']
        else:
            s = ['error']
        return s


class QuestionFive(object):
    def __init__(self, number):
        self.number = int(number)

    def test(self):
        if self.number == 1:
            s = ["test 1", 'answer 1']
        elif self.number == 2:
            s = ["test 2", 'answer 2']
        elif self.number == 3:
            s = ["test 3", 'answer 3']
        elif self.number == 4:
            s = ["test 4", 'answer 4']
        elif self.number == 5:
            s = ["test 5", 'answer 5']
        elif self.number == 6:
            s = ["test 6", 'answer 6']
        elif self.number == 7:
            s = ["test 7", 'answer 7']
        elif self.number == 8:
            s = ["test 8", 'answer 8']
        elif self.number == 9:
            s = ["test 9", 'answer 9']
        elif self.number == 10:
            s = ["test 10", 'answer 10']
        else:
            s = ['error']
        return s


class QuestionSix(object):
    def __init__(self, number):
        self.number = int(number)

    def test(self):
        if self.number == 1:
            s = ["test 1", 'answer 1']
        elif self.number == 2:
            s = ["test 2", 'answer 2']
        elif self.number == 3:
            s = ["test 3", 'answer 3']
        elif self.number == 4:
            s = ["test 4", 'answer 4']
        elif self.number == 5:
            s = ["test 5", 'answer 5']
        elif self.number == 6:
            s = ["test 6", 'answer 6']
        elif self.number == 7:
            s = ["test 7", 'answer 7']
        elif self.number == 8:
            s = ["test 8", 'answer 8']
        elif self.number == 9:
            s = ["test 9", 'answer 9']
        elif self.number == 10:
            s = ["test 10", 'answer 10']
        else:
            s = ['error']
        return s


class QuestionSeven(object):
    def __init__(self, number):
        self.number = int(number)

    def test(self):
        if self.number == 1:
            s = ["test 1", 'answer 1']
        elif self.number == 2:
            s = ["test 2", 'answer 2']
        elif self.number == 3:
            s = ["test 3", 'answer 3']
        elif self.number == 4:
            s = ["test 4", 'answer 4']
        elif self.number == 5:
            s = ["test 5", 'answer 5']
        elif self.number == 6:
            s = ["test 6", 'answer 6']
        elif self.number == 7:
            s = ["test 7", 'answer 7']
        elif self.number == 8:
            s = ["test 8", 'answer 8']
        elif self.number == 9:
            s = ["test 9", 'answer 9']
        elif self.number == 10:
            s = ["test 10", 'answer 10']
        else:
            s = ['error']
        return s


class QuestionEight(object):
    def __init__(self, number):
        self.number = int(number)

    def test(self):
        if self.number == 1:
            s = ["test 1", 'answer 1']
        elif self.number == 2:
            s = ["test 2", 'answer 2']
        elif self.number == 3:
            s = ["test 3", 'answer 3']
        elif self.number == 4:
            s = ["test 4", 'answer 4']
        elif self.number == 5:
            s = ["test 5", 'answer 5']
        elif self.number == 6:
            s = ["test 6", 'answer 6']
        elif self.number == 7:
            s = ["test 7", 'answer 7']
        elif self.number == 8:
            s = ["test 8", 'answer 8']
        elif self.number == 9:
            s = ["test 9", 'answer 9']
        elif self.number == 10:
            s = ["test 10", 'answer 10']
        else:
            s = ['error']
        return s


class QuestionNine(object):
    def __init__(self, number):
        self.number = int(number)

    def test(self):
        if self.number == 1:
            s = ["test 1", 'answer 1']
        elif self.number == 2:
            s = ["test 2", 'answer 2']
        elif self.number == 3:
            s = ["test 3", 'answer 3']
        elif self.number == 4:
            s = ["test 4", 'answer 4']
        elif self.number == 5:
            s = ["test 5", 'answer 5']
        elif self.number == 6:
            s = ["test 6", 'answer 6']
        elif self.number == 7:
            s = ["test 7", 'answer 7']
        elif self.number == 8:
            s = ["test 8", 'answer 8']
        elif self.number == 9:
            s = ["test 9", 'answer 9']
        elif self.number == 10:
            s = ["test 10", 'answer 10']
        else:
            s = ['error']
        return s


class QuestionTen(object):
    def __init__(self, number):
        self.number = int(number)

    def test(self):
        if self.number == 1:
            s = ["test 1", 'answer 1']
        elif self.number == 2:
            s = ["test 2", 'answer 2']
        elif self.number == 3:
            s = ["test 3", 'answer 3']
        elif self.number == 4:
            s = ["test 4", 'answer 4']
        elif self.number == 5:
            s = ["test 5", 'answer 5']
        elif self.number == 6:
            s = ["test 6", 'answer 6']
        elif self.number == 7:
            s = ["test 7", 'answer 7']
        elif self.number == 8:
            s = ["test 8", 'answer 8']
        elif self.number == 9:
            s = ["test 9", 'answer 9']
        elif self.number == 10:
            s = ["test 10", 'answer 10']
        else:
            s = ['error']
        return s


class QuestionEleven(object):
    def __init__(self, number):
        self.number = int(number)

    def test(self):
        if self.number == 1:
            s = ["test 1", 'answer 1']
        elif self.number == 2:
            s = ["test 2", 'answer 2']
        elif self.number == 3:
            s = ["test 3", 'answer 3']
        elif self.number == 4:
            s = ["test 4", 'answer 4']
        elif self.number == 5:
            s = ["test 5", 'answer 5']
        elif self.number == 6:
            s = ["test 6", 'answer 6']
        elif self.number == 7:
            s = ["test 7", 'answer 7']
        elif self.number == 8:
            s = ["test 8", 'answer 8']
        elif self.number == 9:
            s = ["test 9", 'answer 9']
        elif self.number == 10:
            s = ["test 10", 'answer 10']
        else:
            s = ['error']
        return s


class QuestionTwelve(object):
    def __init__(self, number):
        self.number = int(number)

    def test(self):
        if self.number == 1:
            s = ["test 1", 'answer 1']
        elif self.number == 2:
            s = ["test 2", 'answer 2']
        elif self.number == 3:
            s = ["test 3", 'answer 3']
        elif self.number == 4:
            s = ["test 4", 'answer 4']
        elif self.number == 5:
            s = ["test 5", 'answer 5']
        elif self.number == 6:
            s = ["test 6", 'answer 6']
        elif self.number == 7:
            s = ["test 7", 'answer 7']
        elif self.number == 8:
            s = ["test 8", 'answer 8']
        elif self.number == 9:
            s = ["test 9", 'answer 9']
        elif self.number == 10:
            s = ["test 10", 'answer 10']
        else:
            s = ['error']
        return s


class QuestionThirteen(object):
    def __init__(self, number):
        self.number = int(number)

    def test(self):
        if self.number == 1:
            s = ["test 1", 'answer 1']
        elif self.number == 2:
            s = ["test 2", 'answer 2']
        elif self.number == 3:
            s = ["test 3", 'answer 3']
        elif self.number == 4:
            s = ["test 4", 'answer 4']
        elif self.number == 5:
            s = ["test 5", 'answer 5']
        elif self.number == 6:
            s = ["test 6", 'answer 6']
        elif self.number == 7:
            s = ["test 7", 'answer 7']
        elif self.number == 8:
            s = ["test 8", 'answer 8']
        elif self.number == 9:
            s = ["test 9", 'answer 9']
        elif self.number == 10:
            s = ["test 10", 'answer 10']
        else:
            s = ['error']
        return s


class QuestionFourteen(object):
    def __init__(self, number):
        self.number = int(number)

    def test(self):
        if self.number == 1:
            s = ["test 1", 'answer 1']
        elif self.number == 2:
            s = ["test 2", 'answer 2']
        elif self.number == 3:
            s = ["test 3", 'answer 3']
        elif self.number == 4:
            s = ["test 4", 'answer 4']
        elif self.number == 5:
            s = ["test 5", 'answer 5']
        elif self.number == 6:
            s = ["test 6", 'answer 6']
        elif self.number == 7:
            s = ["test 7", 'answer 7']
        elif self.number == 8:
            s = ["test 8", 'answer 8']
        elif self.number == 9:
            s = ["test 9", 'answer 9']
        elif self.number == 10:
            s = ["test 10", 'answer 10']
        else:
            s = ['error']
        return s


class Text(object):
    def __init__(self, number):
        self.number = number

    def test(self):
        if self.number == 1:
            s = "text 1"
        elif self.number == 2:
            s = "text 2"
        elif self.number == 3:
            s = "text 3"
        elif self.number == 4:
            s = "text 4"
        elif self.number == 5:
            s = "text 5"
        elif self.number == 6:
            s = "text 6"
        elif self.number == 7:
            s = "text 7"
        elif self.number == 8:
            s = "text 8"
        elif self.number == 9:
            s = "text 9"
        elif self.number == 10:
            s = "text 10"
        else:
            s = 'error'
        return s
