from tracardi_key_counter.service.key_counter import KeyCounter

from tracardi.domain.profile import Profile
from tracardi_plugin_sdk.service.plugin_runner import run_plugin

from tracardi_key_counter.plugin import KeyCounterAction


def test_key_counter():
    c = KeyCounter({"d": 1})
    c.count('a')
    c.count('b')
    c.count(['a', 'c'])
    c.count({"a": 10, "b": 1, "f": 1, "g": "asas"})

    result = c.counts

    assert result == {'d': 1, 'a': 12, 'b': 2, 'c': 1, 'f': 1}


def test_key_counter_plugin():
    init = {
        "key": ['mobile', 'desktop', 'mobile'],
        'save_in': 'profile@stats.counters.MobileVisits'
    }

    payload = {}
    profile = Profile(id="aaa")
    result = run_plugin(KeyCounterAction, init, payload, profile)
    assert result.output.value == {'mobile': 2, 'desktop': 1}
