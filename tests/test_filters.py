import pytest

from pingout.filters import filter_pingout_all_pings
from pingout.filters import filter_pings_of_date


def test_filter_pingout_all_pings(pingout, db_collection):
    """ Filter all pings of a given pingout """

    pings = filter_pingout_all_pings(pingout, db_collection)
    db_pings = db_collection.find_one({'uuid': pingout})['pings']

    assert pings == db_pings


def test_filter_pings_date_invalid(pingout, db_collection):
    """ Raise ValueError when filter pings by a invalid date as param """

    with pytest.raises(ValueError):
        filter_pings_of_date(pingout, db_collection, 'date')
