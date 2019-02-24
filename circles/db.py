import pymongo
import logging

nameDatabase = 'database'


def connect_to_database_and_get_a_collection(nameDB, nameCollection):
    logging.info('Connecting to MongoDB Client')
    client = pymongo.MongoClient("mongodb://localhost:27017/")

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
    return ins.inserted_id


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
