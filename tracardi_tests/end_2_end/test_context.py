from uuid import uuid4
import asyncio

from tracardi.service.storage.driver import storage

from tracardi_tests.api.test_resource import create_resource
from tracardi_tests.api.test_session import create_session
from tracardi_tests.api.test_profile import create_profile
from tracardi_tests.utils.utils import Endpoint

endpoint = Endpoint()


async def session_exists_profile_exists():
    source_id = 'test-source'
    session_id = str(uuid4())
    profile_id = str(uuid4())

    await create_session(session_id, profile_id)
    await create_profile(profile_id)

    # Assert session and profile exists

    assert endpoint.get(f'/session/{session_id}').status_code == 200
    assert endpoint.get(f'/profile/{profile_id}').status_code == 200
    assert create_resource(source_id, 'web-page').status_code == 200

    response = endpoint.post("/track", data={
        "source": {
            "id": source_id
        },
        "session": {
            "id": session_id
        },
        "profile": {
            "id": profile_id
        },
        "events": [{"type": "page-view", "options": {"save": True}}]
    })
    result = response.json()
    assert result['debugging']['session']['saved'] == 0  # session is not saved because it did not change
    assert result['debugging']['events']['saved'] == 1
    assert result['debugging']['profile']['saved'] == 0  # profile is not saved because it exists

    # IMPORTANT: Everything is ok session and profile exists.

    new_profile_id = result['profile']['id']
    assert new_profile_id == profile_id

    assert endpoint.delete(f'/profile/{new_profile_id}').status_code == 200


async def session_exists_profile_not_exists():
    source_id = 'test-source'
    session_id = str(uuid4())
    profile_id = str(uuid4())

    await create_session(session_id)

    assert endpoint.get(f'/session/{session_id}').status_code == 200
    assert create_resource(source_id, 'web-page').status_code == 200
    assert endpoint.get(f'/profile/{profile_id}').status_code == 404  # No profile

    response = endpoint.post("/track", data={
        "source": {
            "id": source_id
        },
        "session": {
            "id": session_id
        },
        "profile": {
            "id": profile_id
        },
        "events": [{"type": "page-view", "options": {"save": False}}]
    })
    result = response.json()
    assert result['debugging']['session']['saved'] == 1  # session is saved again because
    # new profile is created and session has to be updated.
    assert result['debugging']['events']['saved'] == 0
    assert result['debugging']['profile']['saved'] == 1

    # IMPORTANT: when there is no profile in storage it must be recreated.
    # this is very important security feature.

    new_profile_id = result['profile']['id']
    assert new_profile_id != profile_id

    assert endpoint.delete(f'/profile/{new_profile_id}').status_code == 200


async def session_not_exists_profile_not_exists():
    source_id = 'test-source'
    session_id = str(uuid4())
    profile_id = str(uuid4())

    assert endpoint.get(f'/session/{session_id}').status_code == 404  # No session
    assert endpoint.get(f'/profile/{profile_id}').status_code == 404  # No profile
    assert create_resource(source_id, 'web-page').status_code == 200

    response = endpoint.post("/track", data={
        "source": {
            "id": source_id
        },
        "session": {
            "id": session_id
        },
        "profile": {
            "id": profile_id
        },
        "events": [{"type": "page-view", "options": {"save": True}}]
    })
    result = response.json()
    assert result['debugging']['session']['saved'] == 1
    assert result['debugging']['events']['saved'] == 1
    assert result['debugging']['profile']['saved'] == 1

    # IMPORTANT: when there is no profile in storage it must be recreated.
    # this is very important security feature.

    new_profile_id = result['profile']['id']
    assert new_profile_id != profile_id

    assert result['debugging']['session']['ids'][0] == session_id

    await storage.driver.session.refresh()
    await storage.driver.profile.refresh()

    assert endpoint.get(f'/session/{session_id}').status_code == 200  # Session exists
    assert endpoint.get(f'/profile/{new_profile_id}').status_code == 200  # Profile exists

    assert endpoint.delete(f'/profile/{new_profile_id}').status_code == 200


def test_context():
    async def main():
        await session_exists_profile_exists()
        await session_exists_profile_not_exists()
        await session_not_exists_profile_not_exists()

    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
