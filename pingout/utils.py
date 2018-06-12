import pandas
import json
from uuid import UUID


def validate_uuid(uuid_string):
    try:
        val = UUID(uuid_string, version=4)
    except ValueError:
        return False
    return val.hex == uuid_string


def from_json_to_csv(json_dict, filename):
    df = pandas.DataFrame.from_dict(json_dict, orient='index')
    df.to_csv('files/{}'.format(filename))
