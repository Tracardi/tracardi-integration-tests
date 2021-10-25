import json
from tracardi.process_engine.action.v1.inject_action import InjectAction
from tracardi.domain.profile import Profile
from tracardi_plugin_sdk.service.plugin_runner import run_plugin


def test_plugin_inject():
    init = {"value": json.dumps({"data": 1})}

    payload = {}

    result = run_plugin(InjectAction, init, payload, profile=Profile(id="1"))
    assert result.output.value == {"data": 1}
    assert result.output.port == 'payload'



