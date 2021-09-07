from tracardi.process_engine.action.v1.start_action import StartAction
from tracardi.domain.profile import Profile
from tracardi_plugin_sdk.service.plugin_runner import run_plugin


def test_plugin_start():
    init = {}
    payload = {}

    result = run_plugin(StartAction, init, payload, profile=Profile(id="1"))
    assert result.output.value == {}
    assert result.output.port == 'payload'
