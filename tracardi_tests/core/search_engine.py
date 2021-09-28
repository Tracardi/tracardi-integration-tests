import asyncio

from tracardi.domain.time_range_query import DatetimeRangePayload, DatePayload, DateDeltaPayload, DatetimeType
from tracardi.service.storage.helpers.search_engine import SearchEngine


async def main():
    query = DatetimeRangePayload(
        minDate=DatePayload(
            delta=DateDeltaPayload(value=-12, entity=DatetimeType.hour),
            absolute=None),
        maxDate=DatePayload(delta=None, absolute=None),
        where='type="personal-data"',
        timeZone='Europe/Warsaw',
        start=0,
        limit=30,
        rand=0.4153204263631034
    )
    s = SearchEngine('event')
    result = await s.time_range(query)
    print(result)


asyncio.run(main())
