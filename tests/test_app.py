
def test_return_200_on_root(client):
    """ Return status code 200 on root url"""
    response = client.get('/')
    assert response.status_code == 200


def test_post_return_201_on_root(client):
    """ Return status code 201 when post on root url """
    response = client.post('/')
    assert response.status_code == 201
