import pytest

from pingout import create_app


@pytest.fixture
def app():
    """ Create a new app instance for each test """
    app = create_app()

    yield app


@pytest.fixture
def client(app):
    """ Test client for the app """
    return app.test_client()
