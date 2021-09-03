from utils.utils import Endpoint

endpoint = Endpoint()


def test_source_types_ok():
    result = endpoint.get('/resources/types')
    result = result.json()
    if result:
        assert 'total' in result
        assert 'result' in result


def test_source_list_ok():
    result = endpoint.get('/resources')
    result = result.json()
    if result:
        assert 'total' in result
        assert 'result' in result


def test_source_create_ok():
    resource = dict(
        id="1",
        type="mysql",
        config={"host": "localhost"}
    )
    result = endpoint.post('/resource', data=resource)
    result = result.json()
    assert result == {'saved': 1, 'errors': [], 'ids': ['1']}

    # refresh result and see if there is new data
    response = endpoint.get('/resources/refresh')
    assert response.status_code == 200

    # get new data
    response = endpoint.get('/resource/1')
    assert response.status_code == 200
    result = response.json()
    assert result is not None


def test_resource_get_ok():
    response = endpoint.delete('/resource/2')
    assert response.status_code in [404, 200]

    response = endpoint.get('/resource/2')
    assert response.status_code == 404


def test_source_toggle_on_off_ok():
    # Enable on

    result = endpoint.get('/resource/1/enabled/on').json()
    assert result == {'saved': 1, 'errors': [], 'ids': ['1']}

    result = endpoint.get('/resource/1').json()
    assert result['enabled'] is True

    # Enable off

    result = endpoint.get('/resource/1/enabled/off').json()
    assert result == {'saved': 1, 'errors': [], 'ids': ['1']}

    result = endpoint.get('/resource/1').json()
    assert result['enabled'] is False

    # Consent on

    result = endpoint.get('/resource/1/consent/on').json()
    assert result == {'saved': 1, 'errors': [], 'ids': ['1']}

    result = endpoint.get('/resource/1').json()
    assert result['consent'] is True

    # Consent off

    result = endpoint.get('/resource/1/consent/off').json()
    assert result == {'saved': 1, 'errors': [], 'ids': ['1']}

    result = endpoint.get('/resource/1').json()
    assert (result['consent'] is False)


def test_source_delete_ok():
    response = endpoint.delete('/resource/1')
    if response.status_code == 200:
        result = response.json()
        assert result['result'] == 'deleted'
    else:
        response = endpoint.delete('/resource/1')
        assert response.status_code == 404


def test_resources_refresh():
    response = endpoint.get('/resources/refresh')
    assert response.status_code == 200


def test_resources_by_tag_refresh():
    response = endpoint.get('/resources/by_tag')
    assert response.status_code == 200
    result = response.json()
    assert 'total' in result
    assert 'grouped' in result
