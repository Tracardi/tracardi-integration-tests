import asyncio
from datetime import datetime, timedelta

from tracardi_local_timespan.plugin import LocalTimeSpanAction


def test_time_span_ok():
    start = datetime.now() - timedelta(minutes=2)
    end = datetime.now() + timedelta(minutes=2)

    init = {
        "timezone": 'europe/warsaw',
        "start": start.strftime("%H:%M:%S"),
        "end": end.strftime("%H:%M:%S")
    }

    payload = {}

    async def main():
        plugin = LocalTimeSpanAction(**init)
        result_true, result_false = await plugin.run(payload)
        assert result_true.value is True
        assert result_false.value is None

    asyncio.run(main())


def test_time_span_fail():
    init = {
        "timezone": 'europe/warsaw',
        "start": (datetime.now() + timedelta(minutes=2)).strftime("%H:%M:%S"),
        "end": (datetime.now() + timedelta(minutes=4)).strftime("%H:%M:%S"),
    }

    payload = {}

    async def main():
        plugin = LocalTimeSpanAction(**init)
        result_true, result_false = await plugin.run(payload)
        assert result_true.value is None
        assert result_false.value is True

    asyncio.run(main())
