from tracardi.domain.profile import Profile
from tracardi_plugin_sdk.service.plugin_runner import run_plugin
from tracardi.process_engine.action.v1.decrement_action import DecrementAction


def test_plugin_decrement():
    init = {
        "field": "profile@stats.counters.x",
        "decrement": 1
    }

    payload = {}

    result = run_plugin(DecrementAction, init, payload, profile=Profile(id="1"))
    assert result.profile.stats.counters['x'] == -1


def test_plugin_decrement_2():
    init = {
        "field": "profile@stats.counters.x",
        "decrement": 2
    }

    payload = {}

    result = run_plugin(DecrementAction, init, payload, profile=Profile(id="1"))
    assert result.profile.stats.counters['x'] == -2
