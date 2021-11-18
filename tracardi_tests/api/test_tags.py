from tracardi_tests.utils.utils import Endpoint
from typing import List

endpoint = Endpoint()


def test_create_request(tags: List[str], event_type: str):
    return {
        "type": event_type,
        "tags": tags
    }


def test_add():
    request = create_request(["extag1", "extag2"], "integration-test-type")
    result = endpoint.post(f"/event/tag/add", request)
    assert result.status_code == 200
    assert result.json()["new"] == 1 or result.json()["updated"] == 1

    result = endpoint.get("/event/tag/get")
    assert result.status_code == 200
    assert "integration-test-type" in [doc["id"] for doc in result.json()]


def test_delete_tags():
    request = create_request(["extag1", "extag2"], "integration-test-type")
    result = endpoint.delete(f"/event/tag/delete", request)
    assert result.status_code == 200
    assert result.json()["removed"] == 2

    result = endpoint.get("/event/tag/get")
    assert result.status_code == 200
    assert "integration-test-type" not in [doc["id"] for doc in result.json()]


def test_delete_by_type():
    result = endpoint.delete(f"/event/tag/delete/{'integration-test-type'}")
    assert result.status_code == 200
    assert result.json()["deleted"] == 1

    result = endpoint.get("/event/tag/get")
    assert result.status_code == 200
    assert "integration-test-type" not in [doc["id"] for doc in result.json()]


def test_update():
    result = endpoint.put(f"/event/tag/type/{'integration-test-type'}")
    assert result.status_code == 200

    result = endpoint.put(f"/event/tag/type/{'integration-test-type'}")
    assert result.status_code == 200
    assert result.json()["total"] == 0


def test_tags_endpoint():
    test_add()
    test_delete_tags()
    test_add()
    test_delete_by_type()
    test_add()
    test_update()
