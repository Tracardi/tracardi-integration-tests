from tracardi.domain.session import Session
from tracardi.process_engine.action.v1.new_visit_action import NewVisitAction
from tracardi_plugin_sdk.service.plugin_runner import run_plugin


def test_plugin_new_visit_true():
    init = {}
    payload = {}
    session = Session(id="1")
    session.operation.new = True

    result = run_plugin(NewVisitAction, init, payload, session=session)
    assert result.output.value == payload
    assert result.output.port == 'true'


def test_plugin_new_visit_false():
    init = {}
    payload = {}
    session = Session(id="1")
    session.operation.new = False

    result = run_plugin(NewVisitAction, init, payload, session=session)
    assert result.output.value == payload
    assert result.output.port == 'false'
