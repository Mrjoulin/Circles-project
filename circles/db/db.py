import pymongo
import logging
from openpyxl import load_workbook

nameDatabase = 'circles-database'


def connect_to_database_and_get_a_collection(nameDB, nameCollection):
    logging.info('Connecting to MongoDB Client')
    #client = pymongo.MongoClient("mongodb+srv://kvm202.vdsina.ru: 5980/")
    client = pymongo.MongoClient("mongodb://v108909.hosted-by-vdsina.ru:27017")

    logging.info('Get a database:' + nameDB)
    db = client[nameDB]

    logging.info('Get a collection:' + nameCollection)
    col = db[nameCollection]

    return col


def add_user(name, surname, email, password):
    user = (connect_to_database_and_get_a_collection(nameDB=nameDatabase, nameCollection='user'))

    post = {
            'name': name,
            'surname': surname,
            'email': email,
            'password': password
            }

    logging.info('Inserting a post:' + str(post))
    ins = user.insert_one(post)
    logging.info('Insert info:' + str(ins))
    return post


def is_registered_email(email):
    user = connect_to_database_and_get_a_collection(nameDB=nameDatabase, nameCollection='user')

    logging.info(f'Search email:{email} in DB emails')
    for usr in user.find():
        if usr['email'] == email:
            return True

    return False


def check_user(email, password):
    user = connect_to_database_and_get_a_collection(nameDB=nameDatabase, nameCollection='user')
    logging.info(f'Search user with email:{email}')
    for usr in user.find():
        if usr['email'] == email and usr['password'] == password:
            logging.info(f"User with name - '{usr['name']}', "
                         f"surname - '{usr['surname']}', email - '{usr['email']}' is found")
            return usr
    logging.info('User is not found')
    return None


def add_main_tasks():
    tasks = connect_to_database_and_get_a_collection(nameDB=nameDatabase, nameCollection='tasks')
    wb_task = load_workbook('./excel/задачиПримерыИванов.xlsx')
    ws_task = wb_task.active

    for row in ws_task.values:
        text_task = row[2].split(';')
        post = {
            'class': row[0],
            'theme': row[1],
            'text task': text_task,
            'question': row[4]
        }
        logging.info('Inserting a post:' + str(post))
        ins = tasks.insert_one(post)
        logging.info('Insert info:' + str(ins))

    wb_task.save('./excel/задачиПримерыИванов.xlsx')


def get_main_tasks(class_to_find):
    tasks = connect_to_database_and_get_a_collection(nameDB=nameDatabase, nameCollection='tasks')
    logging.info(f'Get tasks to {class_to_find} class')
    list_of_task = []

    for task in tasks.find():
        if task['class'] == int(class_to_find):
            list_of_task.append(task)

    return list_of_task


def add_user_question_for_task(user_email, user_question, class_of_task,  number_of_task):
    question = connect_to_database_and_get_a_collection(nameDB=nameDatabase, nameCollection='question_about_task')
    logging.info('Add question to collection question_about_task')

    post = {
        'user_email': user_email,
        'user_question': user_question,
        'class_of_task': class_of_task,
        'number_of_task': number_of_task
    }

    logging.info('Insert post: ' + str(post))
    ins = question.insert_one(post)
    logging.info(f'Insert ID: {str(ins)}')


def get_and_remove_all_data_in_collection(collection):
    data = connect_to_database_and_get_a_collection(nameDB=nameDatabase, nameCollection=collection)

    logging.info(f'Get all docs in {collection} collection')
    docs = data.find()

    logging.info(f'Remove all docs in {collection} collection')
    data.delete_many({})

    return docs
