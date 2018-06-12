import datetime


def filter_pingout_all_pings(uuid, collection):
    pings = collection.find_one({'uuid': uuid})['pings']

    return pings


def filter_pings_of_date(uuid, collection, date):
    """ Filter all pings of a given date, which must be an
    instance of datetime """

    if not isinstance(date, datetime.datetime):
        raise ValueError('Invalid date type')
