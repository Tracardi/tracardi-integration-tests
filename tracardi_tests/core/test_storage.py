import asyncio
from tracardi.domain.entity import Entity
from tracardi.domain.record.flow_action_plugin_record import FlowActionPluginRecord
from tracardi.domain.record.event_debug_record import EventDebugRecord
from tracardi.domain.segment import Segment
from tracardi.domain.named_entity import NamedEntity
from tracardi.domain.type import Type
from tracardi.domain.rule import Rule
from tracardi.process_engine.action.v1.start_action import StartAction, register
from tracardi.domain.flow_action_plugin import FlowActionPlugin
from tracardi.domain.flow import Flow
from tracardi.domain.profile import Profile
from tracardi.domain.resource import Resource, ResourceRecord
from tracardi.domain.session import Session
from tracardi.service.storage.factory import StorageFor, storage


def test_storage():
    objects = [
        Session(id="1"),
        Profile(id="1"),
        Flow(**{
            "id": "1",
            "name": "name",
            "description": "desc",
            "enabled": True,
            "projects": [
                "General", "Test"
            ],
            "draft": "",
            "lock": False
        }),
        # Resource(id="2", type="test"),  # todo moze nie byc wymagane
        ResourceRecord(id="2", type="test"),
        Rule(id="1", name="rule", event=Type(type="type"), flow=NamedEntity(id="1", name="flow")),
        Segment(id="1", name="segment", condition="a>1"),  # todo segment needs validation on condition
        EventDebugRecord(id="1", content="abc"),
        FlowActionPluginRecord.encode(FlowActionPlugin(id="2", plugin=register())),
    ]

    loop = asyncio.get_event_loop()

    async def main():
        for instance in objects:
            db = StorageFor(instance).index()
            # print(db.domain_class_ref)

            result = await db.save()
            assert result.saved == 1
            await asyncio.sleep(.5)
            result = await db.load()
            assert isinstance(result, db.domain_class_ref)
            # result = await db.delete()

        result = await StorageFor(Entity(id="1")).index("session").save({"properties": {"a": 1}})
        assert result.saved == 1
        await storage('session').refresh()
        result = await StorageFor(Entity(id="1")).index("session").load(Session)
        assert result.properties == {"a": 1}

    loop.run_until_complete(main())
    loop.close()
