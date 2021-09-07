from time import sleep
from uuid import uuid4

from tracardi.process_engine.action.v1.increase_views_action import IncreaseViewsAction

from tracardi.domain.flow import Flow

from tracardi.process_engine.action.v1.end_action import EndAction

from tracardi.process_engine.action.v1.read_profile_action import ReadProfileAction

from tracardi.process_engine.action.v1.start_action import StartAction

from tracardi.process_engine.action.v1.debug_payload_action import DebugPayloadAction

from test_resource import create_resource
from tracardi_graph_runner.service.builders import action
from utils.utils import Endpoint

endpoint = Endpoint()


def test_source_rule_and_flow():

    source_id = 'source-id'
    flow_id = "flow-id"
    rule_id = "rule-id"
    event_type = 'my-event'
    session_id = str(uuid4())

    # Remove flow

    assert endpoint.delete(f'/flow/{flow_id}').status_code == 200

    # Remove resource
    assert endpoint.delete(f'/resources/{flow_id}').status_code in [200, 404]
    assert endpoint.get('/resources/refresh').status_code == 200

    # Create resource
    assert create_resource(source_id, type='web-page', name="End2End test").status_code == 200
    assert endpoint.get('/resources/refresh').status_code == 200

    response = endpoint.post('/rule', data={
        "id": rule_id,
        "name": "End2End rule",
        "event": {
            "type": event_type
        },
        "flow": {
            "id": flow_id,
            "name": "End2End test"
        },
        "source": {
            "id": source_id,
            "name": "my source"
        },
        "enabled": True
    })
    assert response.status_code == 200

    # Create flow

    debug = action(DebugPayloadAction, {
        "event": {
            "type": event_type,
        }
    })

    start = action(StartAction)
    increase_views = action(IncreaseViewsAction)
    end = action(EndAction)

    flow = Flow.build("End2End - flow", id=flow_id)
    flow += debug('event') >> start('payload')
    flow += start('payload') >> increase_views('payload')
    flow += increase_views('payload') >> end('payload')

    assert endpoint.post('/flow', data=flow.dict()).status_code == 200

    segment_id = "segment-id"

    assert endpoint.post('/segment', data={
        "id": segment_id,
        "name": "Test segment",
        "condition": "profile@stats.views>0",
        "eventType": event_type
    }).status_code == 200

    # Assert rule

    sleep(1)
    response = endpoint.get(f'/rule/{rule_id}')
    assert response.status_code == 200
    result = response.json()
    assert result['source']['id'] == source_id
    assert result['flow']['id'] == flow_id
    assert result['event']['type'] == event_type

    # Assert flow
    assert endpoint.get(f'/flow/{flow_id}').status_code == 200

    # Run /track

    payload = {
        "source": {
            "id": source_id
        },
        "session": {
            "id": session_id
        },
        "events": [{"type": event_type, "options": {"save": True}}],
        "options": {"profile": True}
    }

    response = endpoint.post("/track", data=payload)
    assert response.status_code == 200
    result = response.json()
    assert result['profile']['stats']['views'] == 1
    assert 'test-segment' in result['profile']['segments']

