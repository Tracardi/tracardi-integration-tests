from tracardi.domain.session import Session

from tracardi.process_engine.action.v1.increase_visits_action import IncreaseVisitsAction
from tracardi.domain.profile import Profile
from tracardi_plugin_sdk.service.plugin_runner import run_plugin


def test_plugin_increase_visits_1():
    init = {}
    payload = {}

    session1 = Session(id="1")
    session1.operation.new = True
    result = run_plugin(IncreaseVisitsAction, init, payload, profile=Profile(id="1"), session=session1)
    session1.operation.new = False
    result = run_plugin(IncreaseVisitsAction, init, payload, profile=result.profile, session=session1)
    assert result.profile.stats.visits == 1


def test_plugin_increase_visits_2():
    init = {}
    payload = {}

    session2 = Session(id="2")
    session2.operation.new = True
    session1 = Session(id="1")
    session1.operation.new = True
    result = run_plugin(IncreaseVisitsAction, init, payload, profile=Profile(id="1"), session=session1)
    result = run_plugin(IncreaseVisitsAction, init, payload, profile=result.profile, session=session2)
    assert result.profile.stats.visits == 2



