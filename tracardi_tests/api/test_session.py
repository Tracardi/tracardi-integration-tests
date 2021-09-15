from uuid import uuid4

import asyncio

from tracardi.domain.profile import Profile

from tracardi.domain.session import Session
from tracardi.service.storage.driver import storage
from tracardi.service.storage.factory import StorageFor

from tracardi_tests.utils.utils import Endpoint

endpoint = Endpoint()


async def create_session(session_id, profile_id=None):
    if profile_id is not None:
        session = Session(id=session_id, profile=Profile(id=profile_id))
    else:
        session = Session(id=session_id)

    result = await StorageFor(session).index().save()
    assert result.saved == 1
    await storage.driver.session.refresh()
    return result


async def delete_session(session_id):
    result = await StorageFor(Session(id=session_id)).index().delete()
    return result['deleted'] == 1


def test_get_session():
    session_id = str(uuid4())
    assert endpoint.get(f'/session/{session_id}').status_code == 404

    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_session(session_id))
    loop.close()

    assert endpoint.get(f'/session/{session_id}').status_code == 200
