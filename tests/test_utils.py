import os
import pytest

from pingout.utils import from_json_to_csv


@pytest.fixture
def file_tear_down():
    yield
    os.remove('files/test.csv')


def test_json_to_csv(file_tear_down):
    """ Parse json to csv """
    js = {'test': 'bla'}

    from_json_to_csv(js, 'test.csv')

    file = open("files/test.csv", "r")

    assert file
