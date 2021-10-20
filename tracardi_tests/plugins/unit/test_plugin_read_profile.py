from tracardi.process_engine.action.v1.read_profile_action import ReadProfileAction
from tracardi.domain.profile import Profile
from tracardi_plugin_sdk.service.plugin_runner import run_plugin


def test_plugin_read_profile():
    init = {}
    payload = {}
    profile = Profile(
        id='1'
    )
    result = run_plugin(ReadProfileAction, init, payload, profile=profile)
    assert result.output.value == profile.dict()
    assert result.output.port == 'payload'
