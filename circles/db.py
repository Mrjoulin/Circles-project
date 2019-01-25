import pymongo

client = pymongo.MongoClient("mongodb+srv://joulin:<PASSWORD>@cluster0-j9vys.mongodb.net/test?retryWrites=true")
db = client.database

