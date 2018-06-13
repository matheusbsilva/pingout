import pytest
import datetime

from pingout.filters import filter_pingout_all_pings
from pingout.filters import filter_pings_of_date
from pingout.filters import filter_pings_range_of_dates
from pingout.filters import filter_occurrences_ping_range_date


def test_filter_pingout_all_pings(pingout, db_collection):
    """ Filter all pings of a given pingout """

    pings = filter_pingout_all_pings(pingout, db_collection)
    db_pings = db_collection.find_one({'uuid': pingout})['pings']

    assert pings == db_pings


def test_filter_pings_date_invalid(pingout, db_collection):
    """ Raise ValueError when filter pings by a invalid date as param """

    with pytest.raises(ValueError):
        filter_pings_of_date(pingout, db_collection, 'date')


def test_filter_pings_by_date(pingout, db_collection, today):
    """ Return all pings of a given date """

    db_collection.update_one({'uuid': pingout}, {
        '$push': {'pings': {'count': 2, 'date': today}}})
    db_collection.update_one({'uuid': pingout}, {
        '$push': {'pings': {'count': 3, 'date': datetime.datetime(2001, 8, 17, 0, 0)}}})

    pings = filter_pings_of_date(pingout, db_collection, today)

    assert len(pings) == 1


def test_filter_pings_by_range_of_date_invalid(pingout, db_collection):
    """ Raise ValueError if one of dates is invalid """

    with pytest.raises(ValueError):
        filter_pings_range_of_dates(pingout, db_collection, 'date', 'date')


def test_filter_pings_by_range_of_date(pingout, db_collection, today):
    """ Filter all pings of a date range """

    db_collection.update_one({'uuid': pingout}, {
        '$push': {'pings': {'count': 2, 'date': today}}})
    db_collection.update_one({'uuid': pingout}, {
        '$push': {'pings': {'count': 3, 'date': datetime.datetime(2001, 8, 17, 0, 0)}}})
    db_collection.update_one({'uuid': pingout}, {
        '$push': {'pings': {'count': 3, 'date': datetime.datetime(2018, 8, 17, 0, 0)}}})
    db_collection.update_one({'uuid': pingout}, {
        '$push': {'pings': {'count': 2, 'date': today}}})
    db_collection.update_one({'uuid': pingout}, {
        '$push': {'pings': {'count': 3, 'date': datetime.datetime(2020, 8, 17, 0, 0)}}})

    initial = datetime.datetime(2018, 1, 1, 0, 0)
    final = datetime.datetime(2018, 12, 20, 0, 0)

    pings = filter_pings_range_of_dates(pingout, db_collection, initial, final)

    assert len(pings) == 3


def test_number_of_occurrences_ping_range_date(pingout, db_collection, today):
    """ Filter number of occurrences of dates on pings list """


    db_collection.update_one({'uuid': pingout}, {
        '$push': {'pings': {'count': 2, 'date': today}}})
    db_collection.update_one({'uuid': pingout}, {
        '$push': {'pings': {'count': 3, 'date': datetime.datetime(2001, 8, 17, 0, 0)}}})
    db_collection.update_one({'uuid': pingout}, {
        '$push': {'pings': {'count': 3, 'date': datetime.datetime(2018, 8, 17, 0, 0)}}})
    db_collection.update_one({'uuid': pingout}, {
        '$push': {'pings': {'count': 2, 'date': today}}})

    initial = datetime.datetime(2001, 1, 1, 0, 0)
    final = datetime.datetime(2018, 12, 20, 0, 0)

    pings = filter_occurrences_ping_range_date(pingout, db_collection,
                                               initial, final)
    assert pings[str(today)] == 2
    assert pings[str(datetime.datetime(2001, 8, 17, 0, 0))] == 1
    assert pings[str(datetime.datetime(2018, 8, 17, 0, 0))] == 1
