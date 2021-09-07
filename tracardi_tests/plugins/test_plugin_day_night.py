from datetime import datetime
from tracardi_day_night_split.plugin.day_night_checker import day_night_split, is_day


def test_day_night_split():
    now = datetime(2021, 8, 4, 0, 0, 0, 0)
    sun_rise, sun_set = day_night_split("warsaw", now)
    assert sun_rise.hour == 3
    assert sun_rise.minute == 1
    assert sun_rise.second == 59

    assert sun_set.hour == 18
    assert sun_set.minute == 21
    assert sun_set.second == 5


def test_is_day():
    result = is_day("Europe/Warsaw")
    assert isinstance(result, bool)
