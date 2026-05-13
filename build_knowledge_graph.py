import requests
import os 
import json

DB_NAME = "timeline"
URL = f"http://localhost:2480/api/v1/command/{DB_NAME}"
AUTH = ('root', 'xxxxxxxxx')

# An openCypher query to create an event and link it to a timeline
# This stops "event mixing" by creating a physical bridge
cypher_query = """
CREATE (e1:Event {name: 'Event 1', year: 1})
CREATE (e2:Event {name: 'Event 14', year: 14})
CREATE (e1)-[:NEXT_IN_TIMELINE]->(e2)
RETURN e1, e2
"""

with open("timeline.json", "r") as timeline_file:
    timeline = json.loads(timeline_file.read())
    commands = []
    for i, entry in enumerate(timeline):
        props = ", ".join([f'{k}: {json.dumps(v)}' for k, v in entry.items()])
        commands.append(f"CREATE (e{i}:Event {{{props}}})")
        if i > 0:
            commands.append(f"CREATE (e{i - 1})-[:NEXT]->(e{i})")

    response = requests.post(
        URL, 
        auth=AUTH, 
        json={"language": "openCypher", "command": "\n".join(commands)}
    )
    print(response.json())
