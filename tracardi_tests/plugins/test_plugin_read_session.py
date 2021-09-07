from tracardi.process_engine.action.v1.read_session_action import ReadSessionAction
from tracardi.domain.session import Session
from tracardi_plugin_sdk.service.plugin_runner import run_plugin


def test_plugin_read_session():
    init = {}
    payload = {}
    session = Session(
        id='1'
    )
    result = run_plugin(ReadSessionAction, init, payload, session=session)
    assert result.output.value == session.dict()
    assert result.output.port == 'payload'
