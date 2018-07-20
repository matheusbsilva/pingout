import pymongo
import os

DB_HOST = os.environ.get('MONGO_HOST', 'localhost')
DB_PORT = int(os.environ.get('MONGO_PORT', 27017))


def connect_to_database(engine=pymongo, host=DB_HOST, port=DB_PORT):
    """ Connect to mongo db and return the main database """
    client = engine.MongoClient(host=host, port=port)

    return client['pingout_db']


def connect_to_collection(db):
    """ Connect to app main collection """

    return db['pings_history']
