import pytest

from tracardi_remote_call.plugin import RemoteCallAction

from tracardi_tests.utils.utils import Endpoint


@pytest.mark.asyncio
async def test_remote_call_ok():
    endpoint = Endpoint()
    init = {
        "url": "http://localhost:8686/healthcheck",
        "method": "post",
        "timeout": 1,
        "headers": [
            ("Authorization", endpoint.token),
            ("x-AAA", "test")
        ],
        "body": {"type":"plain/text", "content": "test body"}
    }

    plugin = RemoteCallAction(**init)

    payload = {}

    results = await plugin.run(payload)
    response, error = results

    assert response.value['status'] == 200
    assert response.value['content'] == init['body']['content']


@pytest.mark.asyncio
async def test_remote_call_invalid_cookie():
    init = {
        "url": "http://localhost:8686/healthcheck",
        "method": "post",
        "timeout": 1,
        "headers": [
            ("x-AAA", "test")
        ],
        "cookies": {"a": [
            "a"
        ]},
        "body":  {"type":"plain/text", "content": "test body"}
    }

    plugin = RemoteCallAction(**init)

    payload = {}

    try:
        await plugin.run(payload)
    except ValueError:
        assert True
