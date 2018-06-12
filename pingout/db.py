import pymongo


def connect_to_database(engine=pymongo, host='localhost', port=27017):
    """ Connect to mongo db and return the main database """
    client = engine.MongoClient(host, port)

    return client['pingout_db']
