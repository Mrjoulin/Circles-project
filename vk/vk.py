import logging
import os

from botal import Botal
from vk_api import VkApi
from vk_api.longpoll import VkLongPoll
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk.utils import *

logging.info("Get token")
sess = VkApi(token=os.getenv("VK_TOKEN"))
api = sess.get_api()
lp = VkLongPoll(sess)

cnt = {}
for i in range(2, 15):
    cnt[i] = 1


def safe_listen():
    while True:
        try:
            yield from lp.listen()
        except Exception as e:
            logging.exception(e)


logging.info("Start bot")
handler = Botal(filter(lambda x: x.to_me, safe_listen()), lambda x: x.user_id)


def start(user_id):
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Попробовать решить', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('Тренировка', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('Как пользоваться', color=VkKeyboardColor.PRIMARY)
    api.messages.send(user_id=user_id, message='Выбери нужную тебе опцию:',
                      keyboard=keyboard.get_keyboard())


def tests():
    keyboard = VkKeyboard(one_time=False)
    cnt = 1
    for i in range(4):
        for j in range(3):
            keyboard.add_button(str(cnt), color=VkKeyboardColor.PRIMARY)
            cnt += 1
        keyboard.add_line()
    keyboard.add_button('13', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('14', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('Вернуться назад', color=VkKeyboardColor.PRIMARY)
    return keyboard.get_keyboard()


def message_reply(user_id):
    api.messages.send(user_id=user_id, message='Привет!\nЭто бот для помощи в подготовке к ОГЭ')
    while True:
        start(user_id)
        message = (yield).text
        if message == 'Попробовать решить':
            #остаток
            break
        elif message == 'Тренировка':
            api.messages.send(user_id=user_id, message='Выберете цифру задания для тренировки на клавиатуре.\n'
                                                       'Задания:\n'
                                                       '2 - для проверки внимательности при прочтение текста'
                                                       '... и тд',
                              keyboard=tests())
            while True:
                try:
                    message = (yield).text
                    if 2 <= int(message) <= 14:
                        Testing(int(message), user_id, api, cnt).text()
                        break

                    api.messages.send(user_id=user_id, message='Пожалуйста, выберете конпку на клавиатуре')

                except Exception as e:
                    if message == 'Вернуться назад':
                        break
                    logging.info(e)
                    api.messages.send(user_id=user_id, message='Пожалуйста, выберете конпку на клавиатуре')

        elif message == 'Как пользоваться':
            keyboard = VkKeyboard(one_time=False)
            keyboard.add_button('Назад', color=VkKeyboardColor.PRIMARY)
            api.messages.send(user_id=user_id,
                              message='Если вы хотите поробовать решить тестовое задание ОГЭ, '
                                      'то нажмите на кнопку "Назад", а затем "Попробовать решить"\n'
                                      'Если вы хотите потренироваться в решение затруднительных для вас заданий,'
                                      'то нажмите на конпку "Назад", а затем "Тренировка"',
                              keyboard=keyboard.get_keyboard())
        else:
            api.messages.send(user_id=user_id, message='Пожалуйста, выберете конпку на клавиатуре')


@handler.handler
def on_message(user_id):
    yield
    logging.info("Start bot")
    yield from message_reply(user_id)


@handler.error_handler(Exception)
def on_error(user_id, e):
    if not isinstance(e, StopIteration):
        logging.exception(e)
        api.messages.send(user_id=user_id, message='Извините, произошла внутренняя ошибка: "{}"'.format(str(e)))


if __name__ == "__main__":
    handler.run()
