import pymongo
import logging
from openpyxl import load_workbook

nameDatabase = 'circles-database'
# all collections:
#   user
#   tasks
#   question_about_task
#   teacher_option


def connect_to_database_and_get_a_collection(nameDB, nameCollection):
    logging.info('Connecting to MongoDB Client')
    client = pymongo.MongoClient("mongodb://v108909.hosted-by-vdsina.ru:27017")

    logging.info('Get a database:' + nameDB)
    db = client[nameDB]

    logging.info('Get a collection:' + nameCollection)
    col = db[nameCollection]

    return col


def add_user(name, surname, patronymic, email, password):
    user = (connect_to_database_and_get_a_collection(nameDB=nameDatabase, nameCollection='user'))

    post = {
            'name': name,
            'surname': surname,
            'patronymic': patronymic,
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
    docs = []
    for item in data.find():
        docs += [item]

    logging.info(f'Remove all docs in {collection} collection')
    data.delete_many({})

    return docs


def add_teacher_option(number_option, open_access, name_teacher, email_teacher, topic, number_of_circles, procent_to_5,
                       procent_to_4, procent_to_3, show_mark, tasks):
    option = connect_to_database_and_get_a_collection(nameDB=nameDatabase, nameCollection='teacher_option')
    logging.info('Add option to collection teacher_option')

    post = {
        'number_option': number_option,
        'open_access': open_access,
        'name_teacher': name_teacher,
        'email_teacher': email_teacher,
        'topic': topic,
        'number_of_circles': number_of_circles,
        'procent_to_5': procent_to_5,
        'procent_to_4': procent_to_4,
        'procent_to_3': procent_to_3,
        'show_mark': show_mark,
        'tasks': tasks
    }

    logging.info('Insert post: ' + str(post))
    ins = option.insert_one(post)
    logging.info(f'Insert ID: {str(ins)}')
    return True


def get_teacher_option(find_option):
    options = connect_to_database_and_get_a_collection(nameDB=nameDatabase, nameCollection='teacher_option')
    logging.info('Get option drom collection teacher_option')

    data = []

    for option in options.find():
        if find_option.isdigit():
            if option['number_option'] == int(find_option):
                data.append(option)
        elif option['open_access']:
            if (len(find_option.split()) == 2) and \
                    (find_option.lower().split()[0] in option['name_teacher'].lower().split()) and \
                    (find_option.lower().split()[1] in option['name_teacher'].lower().split()) and \
                    find_option.lower().split()[0] != find_option.lower().split()[1]:
                data.append(option)
            elif len(find_option.lower().split()) == 3 and \
                    ((find_option.lower().split()[0] in option['name_teacher'].lower().split() and
                     find_option.lower().split()[1] in option['name_teacher'].lower().split()) or
                     (find_option.lower().split()[0] in option['name_teacher'].lower().split() and
                      find_option.lower().split()[2] in option['name_teacher'].lower().split()) or
                     (find_option.lower().split()[1] in option['name_teacher'].lower().split() and
                      find_option.lower().split()[2] in option['name_teacher'].lower().split())) and \
                    find_option.lower().split()[0] != find_option.lower().split()[1] and \
                    find_option.lower().split()[0] != find_option.lower().split()[2] and \
                    find_option.lower().split()[1] != find_option.lower().split()[2]:
                data.append(option)
            elif option['email_teacher'].lower() == find_option.lower():
                data.append(option)
            elif option['topic'].lower() == find_option.lower():
                data.append(option)

    return data
