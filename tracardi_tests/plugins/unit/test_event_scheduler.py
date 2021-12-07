import time

from tracardi.domain.entity import Entity
from tracardi.domain.event import Event
from tracardi.domain.profile import Profile
from tracardi.domain.session import Session
from tracardi_plugin_sdk.service.plugin_runner import run_plugin

from tracardi_event_scheduler.plugin import EventSchedulerAction


def test_event_scheduler():
    init = {
        "event_type": "new-event",
        "postpone": "+2m"
    }
    payload = {}

    profile = Profile(id="1")
    event = Event(
        id='1',
        type='text',
        session=Session(id='1'),
        context={},
        source=Entity(id='d94ffd0f-ee16-40f9-a81b-61893f20aa1f')
    )
    print(event)
    session = Session(
        id='1'
    )

    result = run_plugin(
        EventSchedulerAction,
        init,
        payload,
        profile,
        session,
        event
)
    assert result.output.port == 'payload'
    assert result.output.value['timestamp'] > time.time()
