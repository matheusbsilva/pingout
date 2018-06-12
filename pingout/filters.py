import datetime


def filter_pingout_all_pings(uuid, collection):
    pings = collection.find_one({'uuid': uuid})['pings']

    return pings


# TODO: Refact this to filter on mongo
def filter_pings_of_date(uuid, collection, date):
    """ Filter all pings of a given date, which must be an
    instance of datetime """

    if not isinstance(date, datetime.date):
        raise ValueError('Invalid date type')

    pings = filter_pingout_all_pings(uuid, collection)

    pings_data = [ping for ping in pings if ping['date'] == date]

    return pings_data


def filter_pings_range_of_dates(uuid, collection, initial, final):
    """ Filter pings by range of date"""
    if not isinstance(initial, datetime.date) or\
            not isinstance(final, datetime.date):

        raise ValueError('Invalid date type')

    pings = filter_pingout_all_pings(uuid, collection)
    pings_range = []

    for ping in pings:
        if ping['date'] >= initial and ping['date'] <= final:
            pings_range.append(ping)

    return pings_range

