from time import sleep

from test_source import create_resource
from utils.utils import Endpoint

endpoint = Endpoint()


def test_new_rule():
    data = {
        "id": "rule_id",
        "name": "string",
        "event": {
            "type": "string"
        },
        "flow": {
            "id": "flow_id",
            "name": "string"
        },
        "source": {
            "id": "string",
            "name": "string"
        },
        "enabled": True
    }

    response = endpoint.post('/rule', data=data)
    assert response.status_code == 422

    result = response.json()
    assert result['detail'] == 'Missing source id: `string`'

    # Add source

    response = create_resource("1", "mysql")
    assert response.status_code == 200

    # Create rule with new source

    data['source']['id'] = "1"

    response = endpoint.post('/rule', data=data)
    result = response.json()
    assert response.status_code == 200
    assert result == {'saved': 1, 'errors': [], 'ids': ['rule_id']}

    # Check if flow was created
    sleep(1)
    response = endpoint.get('/flow/flow_id')
    assert response.status_code == 200
    result = response.json()
    assert result['id'] == 'flow_id'

    # Delete flow - it should delete also rule
    assert endpoint.delete('/flow/flow_id').status_code == 200
