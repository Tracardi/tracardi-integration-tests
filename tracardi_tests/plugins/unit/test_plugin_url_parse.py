import asyncio
from tracardi.domain.session import Session
from tracardi.process_engine.action.v1.strings.url_parser.plugin import ParseURLParameters


def test_plugin_url_parser_ok():
    async def main():
        init = {
            "url": 'session@context.page.url'
        }

        payload = {}

        plugin = ParseURLParameters(**init)
        plugin.session = Session(
            id='1',
            context={
                'page': {
                    'url': "http://test.url/path/?param=1#hash"
                }
            }
        )

        return await plugin.run(payload)

    result = asyncio.run(main())
    assert result.value['url'] == "http://test.url/path/?param=1#hash"
    assert result.value['scheme'] == 'http'
    assert result.value['hostname'] == 'test.url'
    assert result.value['path'] == '/path/'
    assert result.value['query'] == 'param=1'
    assert result.value['params'] == {'param': '1'}
    assert result.value['fragment'] == 'hash'


def test_plugin_url_parser_fail():
    async def main():
        init = {
            "url": 'session@context.page.url'
        }

        payload = {}

        plugin = ParseURLParameters(**init)
        plugin.session = Session(
            id='1',
            context={
                'page': {
                    'no-key': "http://test.url/path/?param=1#hash"  # Incorrect key
                }
            }
        )

        return await plugin.run(payload)

    try:
        asyncio.run(main())
        assert False
    except KeyError:
        assert True
