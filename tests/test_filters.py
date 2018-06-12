import pytest
import datetime

from pingout.filters import filter_pingout_all_pings
from pingout.filters import filter_pings_of_date
from pingout.filters import filter_pings_range_of_dates


def test_filter_pingout_all_pings(pingout, db_collection):
    """ Filter all pings of a given pingout """

    pings = filter_pingout_all_pings(pingout, db_collection)
    db_pings = db_collection.find_one({'uuid': pingout})['pings']

    assert pings == db_pings


def test_filter_pings_date_invalid(pingout, db_collection):
    """ Raise ValueError when filter pings by a invalid date as param """

    with pytest.raises(ValueError):
        filter_pings_of_date(pingout, db_collection, 'date')


def test_filter_pings_by_date(pingout, db_collection):
    """ Return all pings of a given date """

    db_collection.update_one({'uuid': pingout}, {
        '$push': {'pings': {'count': 2, 'date': datetime.date.today()}}})
    db_collection.update_one({'uuid': pingout}, {
        '$push': {'pings': {'count': 3, 'date': datetime.date(2001, 8, 17)}}})

    pings = filter_pings_of_date(pingout, db_collection, datetime.date.today())

    assert len(pings) == 1


def test_filter_pings_by_range_of_date_invalid(pingout, db_collection):
    """ Raise ValueError if one of dates is invalid"""

    with pytest.raises(ValueError):
        filter_pings_range_of_dates(pingout, db_collection, 'date', 'date')
