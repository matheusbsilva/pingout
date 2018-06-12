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


def test_return_201_post_on_ping(client):
    """ Return 201 when post on ping url """
    uuid = 'test'
    response = client.post('/{}/ping'.format(uuid))

    assert response.status_code == 201
