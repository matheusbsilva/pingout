import datetime
import os

from uuid import uuid4

from pingout.utils import validate_uuid


def test_return_200_on_root(client):
    """ Return status code 200 on root url"""
    response = client.get('/')
    assert response.status_code == 200


def test_return_405_post_on_root(client):
    """ Return status code 405 when post on root url """
    response = client.post('/')
    assert response.status_code == 405


def test_post_return_201_on_create_pingout(client):
    """ Return status code 201 when post on create pingout url """
    response = client.post('/create-pingout')
    assert response.status_code == 201


def test_get_405_on_create_pingout(client):
    """ Return status code 405 when get on create pingout url """
    response = client.get('/create-pingout')
    assert response.status_code == 405


def test_return_json_when_post_on_create_pingout(client):
    """ Return json dict when post on create pingout url """
    response = client.post('/create-pingout')
    assert response.json


def test_return_uuid_when_post_on_create_pingout(client):
    """ Return uuid when post on create_pingout url """
    response = client.post('/create-pingout')
    assert 'uuid' in response.json.keys()


def test_return_not_empty_uuid_post_on_create_pingout(client):
    """ Return not empty uuid when post on create_pingout url """
    response = client.post('/create-pingout')
    assert response.json['uuid']


def test_return_valid_uuid4_post_on_create_pingout(client):
    """ Return valid uuid version 4 when post on create_pingout url """
    response = client.post('/create-pingout')
    assert validate_uuid(response.json['uuid'])


def test_return_different_uuid4_post_on_create_pingout(client):
    """ Return different uuids when post on create_pingout url"""
    response1 = client.post('/create-pingout')
    response2 = client.post('/create-pingout')

    assert response1.json['uuid'] != response2.json['uuid']


def test_save_uuid_on_db_post_create_pingout(client, db_collection):
    """ Create a new registry on database with the created uuid
    when post on create-pingout url """

    response = client.post('/create-pingout')
    assert db_collection.find_one({'uuid': response.json['uuid']})


def test_create_empty_pings_list_post_create_pingout(client, db_collection):
    """ Create an empty pings list for the new registry of the created uuid
    when post on create-pingout url """

    response = client.post('/create-pingout')
    registry = db_collection.find_one({'uuid': response.json['uuid']})

    assert registry['pings'] == []


def test_return_400_post_on_ping_for_bad_uuid(client):
    """ Return 400 when post on ping url passing a bad formated
    uuid as parameter """

    uuid = 'test'
    response = client.post('/{}/ping'.format(uuid))

    assert response.status_code == 400
    assert response.json['errors'] == 'Bad format uuid'


def test_return_201_post_on_ping_ok_format(client, pingout):
    """ Return 201 for uuid with correct format when post on ping url """
    response = client.post('/{}/ping'.format(pingout))

    assert response.status_code == 201


def test_return_404_post_on_ping_not_created_pingout(client):
    """ Return 404 when post on ping with a not created uuid pingout """
    uuid = uuid4().hex
    response = client.post('/{}/ping'.format(uuid))

    assert response.status_code == 404


def test_create_push_new_ping_post_on_ping(client, pingout, db_collection):
    """ Push new ping on the list of pingout pings """

    client.post('/{}/ping'.format(pingout))

    assert db_collection.find_one({'uuid': pingout})['pings']


def test_pushed_ping_values_post_on_ping(client, pingout, db_collection):
    """ Push ping with a dict containing count and date """

    client.post('/{}/ping'.format(pingout))

    ping_pushed = db_collection.find_one({'uuid': pingout})['pings'][0]

    assert 'count' in ping_pushed.keys()
    assert 'date' in ping_pushed.keys()


def test_first_ping_push_count_is_1_on_ping(client, pingout, db_collection):
    """ First ping pushd count must be 1 """

    client.post('/{}/ping'.format(pingout))

    ping_pushed = db_collection.find_one({'uuid': pingout})['pings'][0]

    assert ping_pushed['count'] == 1


def test_count_ping_pushed_is_sum_of_previous(client, pingout, db_collection):
    """ Count of ping pushed to the list is the sum
    of the previous ping count """

    db_collection.update_one({'uuid': pingout},
                             {'$push': {'pings': {'count': 1, 'date': 1}}})

    client.post('/{}/ping'.format(pingout))

    ping_pushed = db_collection.find_one({'uuid': pingout})['pings'][-1]

    assert ping_pushed['count'] == 2


def test_date_ping_pushed_on_ping(client, pingout, db_collection):
    """ Save date of pushed ping as the today datetime """

    client.post('/{}/ping'.format(pingout))

    ping_pushed = db_collection.find_one({'uuid': pingout})['pings'][-1]

    pushed_date = ping_pushed['date']
    today = datetime.datetime.today().replace(second=0, microsecond=0)

    assert pushed_date == today


def test_return_404_for_invalid_pingout_occur_range_date(client):
    """ Return 404 when get on pingout occur by range date
    with a invalid uuid"""

    response = client.get('/{}'.format(uuid4().hex))

    assert response.status_code == 404


def test_return_302_on_pingout_occur_range_date(client, pingout, db_collection):
    """ Return 302 when get on pingout url """

    db_collection.update_one({'uuid': pingout}, {
        '$push': {'pings': {'count': 2, 'date': datetime.date.today()}}})
    db_collection.update_one({'uuid': pingout}, {
        '$push': {'pings': {'count': 3, 'date': datetime.date(2001, 8, 17)}}})

    response = client.get('/{}?initial_date=2018-01-01&final_date=2018-12-01'.format(pingout))

    assert response.status_code == 302


def test_save_file_with_bad_dates_pingout_occur(client, pingout):
    """ Return 400 for bad formated or empty inital and final dates """
    response = client.get('/{}?initial_date=203'.format(pingout))

    assert response.status_code == 400


def test_save_result_query_file_pingout_occur(client, pingout, db_collection):
    """ Save csv with the result of the data range occurence query """

    db_collection.update_one({'uuid': pingout}, {
        '$push': {'pings': {'count': 2, 'date': datetime.date.today()}}})
    db_collection.update_one({'uuid': pingout}, {
        '$push': {'pings': {'count': 3, 'date': datetime.date(2001, 8, 17)}}})

    client.get('/{}?initial_date=2018-01-01&final_date=2020-01-01'.format(pingout))

    assert os.path.isfile('files/{}.csv'.format(pingout))

    os.remove('files/{}.csv'.format(pingout))


def test_redirect_after_save_file_pingout_occur(client, pingout, db_collection):
    """ Redirect to file download after create csv with the query result """

    db_collection.update_one({'uuid': pingout}, {
        '$push': {'pings': {'count': 2, 'date': datetime.date.today()}}})
    db_collection.update_one({'uuid': pingout}, {
        '$push': {'pings': {'count': 3, 'date': datetime.date(2001, 8, 17)}}})

    response = client.get('/{}?initial_date=2018-01-01&final_date=2020-01-01'.format(pingout))
    redirect_url = response.location.split('http://localhost')[-1]
    assert redirect_url == "/{}/download".format(pingout)


def test_return_200_on_get_download_page(client, pingout):
    """ Return 200 when get on download page """

    response = client.get('/{}/download'.format(pingout))

    assert response.status_code == 200


def test_return_200_on_get_download_file(client, pingout, db_collection):
    """ Return 200 when get on download file url """
    db_collection.update_one({'uuid': pingout}, {
        '$push': {'pings': {'count': 2, 'date': datetime.date.today()}}})
    db_collection.update_one({'uuid': pingout}, {
        '$push': {'pings': {'count': 3, 'date': datetime.date(2001, 8, 17)}}})

    client.get('/{}?initial_date=2018-01-01&final_date=2020-01-01'.format(pingout))
    response = client.get('{}/download/{}.csv'.format(pingout, pingout))

    assert response.status_code == 200


