import mongomock


""" Database connection and setup tests """


def test_connect_to_database_client_address(db):
    mock = mongomock.MongoClient('test', 10)['pingout_db']
    assert db.client.address == mock.client.address


def test_connect_to_database_main_database(db):
    assert db.name is 'pingout_db'


def test_main_collection(db_collection):
    assert db_collection.name is 'pings_history'
