from tracardi_tests.utils.utils import Endpoint
from typing import List

endpoint = Endpoint()


def create_request(tags: List[str], event_type: str):
    return {
        "type": event_type,
        "tags": tags
    }


def add():
    request = create_request(["extag1", "extag2"], "integration-test-type")
    result = endpoint.post(f"/event/tag/add", request)
    assert result.status_code == 200
    assert result.json()["new"] == 1 or result.json()["updated"] == 1

    result = endpoint.get("/event/tag/get")
    assert result.status_code == 200
    assert "integration-test-type" in [doc["id"] for doc in result.json()]


def delete_tags():
    request = create_request(["extag1", "extag2"], "integration-test-type")
    result = endpoint.delete(f"/event/tag/delete", request)
    assert result.status_code == 200
    assert result.json()["removed"] == 2

    result = endpoint.get("/event/tag/get")
    assert result.status_code == 200
    assert "integration-test-type" not in [doc["id"] for doc in result.json()]


def delete_by_type():
    result = endpoint.delete(f"/event/tag/delete/{'integration-test-type'}")
    assert result.status_code == 200
    assert result.json()["deleted"] == 1

    result = endpoint.get("/event/tag/get")
    assert result.status_code == 200
    assert "integration-test-type" not in [doc["id"] for doc in result.json()]


def update():
    result = endpoint.put(f"/event/tag/type/{'integration-test-type'}")
    assert result.status_code == 200

    result = endpoint.put(f"/event/tag/type/{'integration-test-type'}")
    assert result.status_code == 200
    assert result.json()["total"] == 0


def test_tags_endpoint():
    add()
    delete_tags()
    add()
    delete_by_type()
    add()
    update()
