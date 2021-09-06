import asyncio

from tracardi.process_engine.action.v1.read_profile_action import ReadProfileAction

from tracardi.process_engine.action.v1.inject_action import InjectAction

from tracardi.domain.flow import Flow

from tracardi.domain.session import Session

from tracardi.domain.profile import Profile

from tracardi.domain.event import Event
from tracardi.process_engine.action.v1.end_action import EndAction
from tracardi.process_engine.action.v1.start_action import StartAction
from tracardi_graph_runner.domain.flow_history import FlowHistory
from tracardi_graph_runner.domain.work_flow import WorkFlow

from tracardi_graph_runner.service.builders import action


async def save():
    start = action(InjectAction, {"a": 1})
    read_profile = action(ReadProfileAction)
    end1 = action(EndAction)
    end2 = action(EndAction)

    flow = Flow.build("test", id="1")
    flow += start('payload') >> read_profile('payload')
    flow += read_profile('profile') >> end1('payload')
    flow += start('payload') >> end2('payload')

    await flow.storage().save()

asyncio.run(save())

# async def main():
#     session = Session(id="1")
#     wf = WorkFlow(flow_history=FlowHistory(), session=session, profile=Profile(id="1"), event=Event.new({
#         "type": "page-view",
#         "source": {"id": "1"},
#         "session": session,
#         "context": {}
#     }))
#     result = await wf.invoke(flow)
#     print(result)
#
#
# asyncio.run(main())