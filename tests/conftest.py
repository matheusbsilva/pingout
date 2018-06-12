import pytest
import mongomock

from pingout import create_app
from pingout.db import connect_to_database


@pytest.fixture
def app():
    """ Create a new app instance for each test """
    app = create_app()

    yield app


@pytest.fixture
def client(app):
    """ Test client for the app """
    return app.test_client()


@pytest.fixture
def db():
    """ Mongomock for db tests """
    return connect_to_database(engine=mongomock, host='test', port=10)
