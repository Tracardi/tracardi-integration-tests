from tracardi.process_engine.action.v1.new_profile_action import NewProfileAction
from tracardi.domain.profile import Profile
from tracardi_plugin_sdk.service.plugin_runner import run_plugin


def test_plugin_new_profile_true():
    init = {}
    payload = {}
    profile = Profile(id="1")
    profile.operation.new = True

    result = run_plugin(NewProfileAction, init, payload, profile=profile)
    assert result.output.value == payload
    assert result.output.port == 'true'


def test_plugin_new_profile_false():
    init = {}
    payload = {}
    profile = Profile(id="1")
    profile.operation.new = False

    result = run_plugin(NewProfileAction, init, payload, profile=profile)
    assert result.output.value == payload
    assert result.output.port == 'false'
