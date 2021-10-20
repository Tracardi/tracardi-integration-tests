from tracardi.domain.entity import Entity

from tracardi.domain.session import Session

from tracardi.domain.event import Event
from tracardi.process_engine.action.v1.read_event_action import ReadEventAction
from tracardi_plugin_sdk.service.plugin_runner import run_plugin


def test_plugin_read_event():
    init = {}
    payload = {}
    event = Event(
        id='1',
        type='text',
        session=Session(id='1'),
        context={},
        source=Entity(id='1')
    )
    result = run_plugin(ReadEventAction, init, payload, event=event)
    assert result.output.value == event.dict()
    assert result.output.port == 'payload'
