from uuid import uuid4

from tracardi.process_engine.action.v1.increase_views_action import IncreaseViewsAction
from tracardi.domain.flow import Flow
from tracardi.process_engine.action.v1.end_action import EndAction
from tracardi.process_engine.action.v1.start_action import StartAction
from tracardi.process_engine.action.v1.debug_payload_action import DebugPayloadAction
from tracardi_tests.api.test_resource import create_resource
from tracardi_graph_runner.service.builders import action
from tracardi_tests.utils.utils import Endpoint

endpoint = Endpoint()


def test_source_rule_and_flow():
    source_id = 'source-id'
    profile_id = str(uuid4())
    flow_id_1 = "flow-id-1"
    rule_id_1 = "rule-id-1"
    event_type = 'my-event'
    session_id = str(uuid4())

    # Delete profile
    assert endpoint.delete(f'/profile/{profile_id}').status_code in [200, 404]

    # Delete flows and rules
    # assert endpoint.delete(f'/rule/{rule_id_1}').status_code in [200, 404]
    assert endpoint.delete(f'/flow/{flow_id_1}').status_code in [200, 404]

    # Create resource
    assert create_resource(source_id, type='web-page', name="End2End test").status_code == 200
    assert endpoint.get('/resources/refresh').status_code == 200

    response = endpoint.post('/rule', data={
        "id": rule_id_1,
        "name": "Multiple events in one track",
        "event": {
            "type": event_type
        },
        "flow": {
            "id": flow_id_1,
            "name": "Multiple events in one track"
        },
        "source": {
            "id": source_id,
            "name": "my test source"
        },
        "enabled": True
    })

    assert response.status_code == 200
    assert endpoint.get('/rules/refresh').status_code == 200

    # Create flows

    debug = action(DebugPayloadAction, init={"event": {"type": event_type}})
    start = action(StartAction)
    increase_views = action(IncreaseViewsAction)
    end = action(EndAction)

    flow = Flow.build("Profile quick update - test", id=flow_id_1)
    flow += debug('event') >> start('payload')
    flow += start('payload') >> increase_views('payload')
    flow += increase_views('payload') >> end('payload')

    assert endpoint.post('/flow', data=flow.dict()).status_code == 200
    assert endpoint.get('/flows/refresh').status_code == 200

    # Send event
    payload = {
            "source": {
                "id": source_id
            },
            "session": {
                "id": session_id
            },
            "profile": {
                "id": profile_id
            },
            "events": [
                {"type": event_type},
                {"type": event_type},
                {"type": event_type},
                {"type": event_type},
                {"type": event_type},
                {"type": event_type},
                {"type": event_type},
                {"type": event_type},
                {"type": event_type},
                {"type": event_type},
                {"type": event_type},
                {"type": event_type},
                {"type": event_type},
                {"type": event_type},
                {"type": event_type},
                {"type": event_type},
                {"type": event_type},
                {"type": event_type},
                {"type": event_type},
                {"type": event_type},
                {"type": event_type},
                {"type": event_type},
                {"type": event_type},
                {"type": event_type},
                {"type": event_type},
                {"type": event_type},
                {"type": event_type},
                {"type": event_type},
                {"type": event_type},
                {"type": event_type},
            ],
            "options": {"profile": True}
        }

    response = endpoint.post("/track", data=payload)
    assert response.status_code == 200
    result = response.json()
    profile_id = result['profile']['id']

    assert result['profile']['stats']['views'] == 30

    # Delete profile
    assert endpoint.delete(f'/profile/{profile_id}').status_code in [200, 404]

    # Delete flows and rules
    assert endpoint.delete(f'/flow/{flow_id_1}').status_code in [200, 404]
