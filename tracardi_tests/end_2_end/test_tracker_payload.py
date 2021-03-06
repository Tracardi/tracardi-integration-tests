from uuid import uuid4

from tracardi_tests.api.test_resource import create_resource
from tracardi_tests.utils.utils import Endpoint

endpoint = Endpoint()


def test_track_payload():

    id = "1"

    response = create_resource(id, "web-page")
    assert response.status_code == 200

    payload = {
        "source": {
            "id": id
        },
        "session": {
            "id": str(uuid4())
        },
        "events": [{"type": "page-view"}, {"type": "page-view", "options": {"save": False}}]
    }

    response = endpoint.post("/track", data=payload)
    assert response.status_code == 200

    result = response.json()
    assert result['debugging']['events']['saved'] == 1
    assert len(result['debugging']['events']['errors']) == 0
    assert len(result['debugging']['events']['ids']) == 1
    assert 'id' in result['profile']

    # Delete resource

    assert endpoint.delete(f'/resource/{id}').status_code == 200
