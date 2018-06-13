import datetime
import pandas


def filter_pingout_all_pings(uuid, collection):
    pings = collection.find_one({'uuid': uuid})['pings']

    return pings


# TODO: Refact this to filter on mongo
def filter_pings_of_date(uuid, collection, date):
    """ Filter all pings of a given date, which must be an
    instance of datetime """

    if not isinstance(date, datetime.datetime):
        raise ValueError('Invalid date type')

    pings = filter_pingout_all_pings(uuid, collection)

    pings_data = [ping for ping in pings if ping['date'] == date]

    return pings_data


def filter_pings_range_of_dates(uuid, collection, initial, final):
    """ Filter pings by range of date"""
    if not isinstance(initial, datetime.datetime) or\
            not isinstance(final, datetime.datetime):

        raise ValueError('Invalid date type')

    pings = filter_pingout_all_pings(uuid, collection)
    pings_range = []

    for ping in pings:
        if ping['date'].date() >= initial.date() and ping['date'].date() <= final.date():
            ping['date'] = ping['date'].date()
            pings_range.append(ping)

    return pings_range


def filter_occurrences_ping_range_date(uuid, collection, initial, final):
    """ Filter number of occurences of pings by each date
    in the range given """

    if not isinstance(initial, datetime.datetime) or\
            not isinstance(final, datetime.datetime):

        raise ValueError('Invalid date type')

    pings = filter_pings_range_of_dates(uuid, collection, initial, final)
    df = pandas.DataFrame(pings)
    df['date'] = df['date'].astype(str)
    df = df['date'].value_counts()

    return df.to_dict()
