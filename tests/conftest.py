import pytest
import mongomock
import datetime
from uuid import uuid4

from pingout import create_app
from pingout.db import connect_to_database
from pingout.db import connect_to_collection


@pytest.fixture
def app(db):
    """ Create a new app instance for each test """
    app = create_app(db=db)

    yield app


@pytest.fixture
def client(app):
    """ Test client for the app """
    return app.test_client()


@pytest.fixture
def db():
    """ Mongomock for db tests """
    return connect_to_database(engine=mongomock, host='test', port=10)


@pytest.fixture
def db_collection(db):
    """ Main db collection """
    return connect_to_collection(db=db)


@pytest.fixture
def pingout(db_collection):
    uuid = uuid4().hex
    db_collection.insert_one({'uuid': uuid, 'pings': []})

    return uuid


@pytest.fixture
def today():
    return datetime.datetime.today().replace(second=0, microsecond=0)
