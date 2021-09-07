from tracardi.process_engine.action.v1.increase_views_action import IncreaseViewsAction
from tracardi.domain.profile import Profile
from tracardi_plugin_sdk.service.plugin_runner import run_plugin


def test_plugin_increase_views():
    init = {}

    payload = {}

    result = run_plugin(IncreaseViewsAction, init, payload, profile=Profile(id="1"))
    result = run_plugin(IncreaseViewsAction, init, payload, profile=result.profile)
    assert result.profile.stats.views == 2



