
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
