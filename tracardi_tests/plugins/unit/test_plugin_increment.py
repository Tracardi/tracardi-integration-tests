from tracardi.process_engine.action.v1.increment_action import IncrementAction

from tracardi.domain.profile import Profile
from tracardi_plugin_sdk.service.plugin_runner import run_plugin


def test_plugin_increment():
    init = {
        "field": "profile@stats.counters.x",
        "increment": 1
    }

    payload = {}

    result = run_plugin(IncrementAction, init, payload, profile=Profile(id="1"))
    assert result.profile.stats.counters['x'] == 1


def test_plugin_increment_2():
    init = {
        "field": "profile@stats.counters.x",
        "increment": 2
    }

    payload = {}

    result = run_plugin(IncrementAction, init, payload, profile=Profile(id="1"))
    assert result.profile.stats.counters['x'] == 2
