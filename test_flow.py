from utils.utils import Endpoint

endpoint = Endpoint()


def create_flow(id, name, desc):
    data = {
        "id": id,
        "name": name,
        "description": desc,
        "enabled": True,
        "projects": [
            "General", "Test"
        ],
        "draft": "",
        "lock": False
    }

    return endpoint.post('/flow', data=data)


def check_flow_bool(id, lock, type='lock', field='lock'):
    on_off = 'yes' if lock else 'no'

    response = endpoint.get(f'/flow/{id}/{type}/{on_off}')
    assert response.status_code == 200
    result = response.json()
    assert result == {'saved': 1, 'errors': [], 'ids': [id]}

    # flush data to elastic
    assert endpoint.get('/flow/metadata/refresh').status_code == 200

    # read flow
    response = endpoint.get(f'/flow/{id}')
    assert response.status_code == 200
    if response.status_code == 200:
        result = response.json()
        assert result[field] is lock
    else:
        raise Exception("Could not read flow id {}".format(id))


def test_flow_ok():
    result = endpoint.get('/flows')
    result = result.json()
    assert 'total' in result
    assert 'result' in result


def test_add_flow_ok():
    id = '3'

    # delete flow
    assert endpoint.delete(f'/flow/{id}').status_code in [200, 404]

    # add flow

    response = create_flow(id, "Test flow", "Opis")
    result = response.json()
    assert {'saved': 1, 'errors': [], 'ids': [id]} == result

    # flush data to elastic
    assert endpoint.get('/flow/metadata/refresh').status_code == 200

    # read saved flow

    response = endpoint.get(f'/flow/{id}')
    assert response.status_code == 200
    if response.status_code == 200:
        result = response.json()
        assert result['id'] == id
        assert result['name'] == 'Test flow'

        # delete flow
        assert endpoint.delete(f'/flow/{id}').status_code == 200

        # flush data to elastic
        assert endpoint.get('/flow/metadata/refresh').status_code == 200

        # check if do not exist
        assert endpoint.get(f'/flow/{id}').status_code == 404


def test_get_flow_ok():
    id = '3'

    # delete flow
    assert endpoint.delete(f'/flow/{id}').status_code in [200, 404]

    # flush data to elastic
    assert endpoint.get('/flow/metadata/refresh').status_code == 200

    # check if do not exist
    assert endpoint.get(f'/flow/{id}').status_code == 404


def test_update_flow_metadata_ok():
    id = '3'

    # delete flow
    assert endpoint.delete(f'/flow/{id}').status_code in [200, 404]

    # flush data to elastic
    assert endpoint.get('/flow/metadata/refresh').status_code == 200

    # create flow
    response = create_flow(id, "Test flow", "Opis")
    assert response.status_code == 200
    result = response.json()
    assert result == {'saved': 1, 'errors': [], 'ids': [id]}

    # flush data to elastic
    assert endpoint.get('/flow/metadata/refresh').status_code == 200

    response = endpoint.get(f'/flow/{id}')
    assert response.status_code == 200
    if response.status_code == 200:
        result = response.json()
        assert result['id'] == id
        assert result['name'] == 'Test flow'
    else:
        raise Exception("Could not read flow")

    response = endpoint.post('/flow/metadata', data={
        "id": id,
        "name": "New name",
        "description": "New Description",
        "enabled": False,
        "projects": [
            "New"
        ]
    })
    assert response.status_code == 200
    result = response.json()
    assert result == {'saved': 1, 'errors': [], 'ids': [id]}

    # flush data to elastic
    assert endpoint.get('/flow/metadata/refresh').status_code == 200

    # get updated flow

    response = endpoint.get(f'/flow/{id}')
    assert response.status_code == 200
    if response.status_code == 200:
        result = response.json()
        assert result['id'] == id
        assert result['name'] == 'New name'
        assert result['description'] == 'New Description'
        assert result['enabled'] is False
        assert "New" in result['projects']
    else:
        raise Exception("Could not read flow")

    assert endpoint.delete(f'/flow/{id}').status_code == 200


def test_flush_flow():
    assert endpoint.get('/flow/metadata/flush').status_code == 200


def test_flow_lock_enable():
    id = '3'

    # create flow
    response = create_flow(id, "Test flow", "Opis")
    assert response.status_code == 200

    # read flow
    check_flow_bool(id, True, type='lock', field='lock')
    check_flow_bool(id, False, type='lock', field='lock')
    check_flow_bool(id, True, type='enable', field='enabled')
    check_flow_bool(id, False, type='enable', field='enabled')

    assert endpoint.delete(f'/flow/{id}').status_code == 200

# todo flow delete deletes also rules.
