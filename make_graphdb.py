import requests

DB_NAME = "timeline"
URL = f"http://localhost:2480/api/v1/server"
AUTH = ('root', 'xxxxxx')

create_database = requests.post(URL, json={"command": f"create database {DB_NAME}"}, auth=AUTH)
print(create_database.json())

# Create a type for Events so they have a dedicated folder on your disk
COMMAND_URL = f"http://localhost:2480/api/v1/command/{DB_NAME}"
create_event_type = requests.post(COMMAND_URL, auth=AUTH, json={
    "language": "sql", 
    "command": "CREATE VERTEX TYPE Event"
})
print(create_event_type.json())

create_next_edge_type = requests.post(COMMAND_URL, auth=AUTH, json={
    "language": "sql", 
    "command": "CREATE EDGE TYPE NEXT IF NOT EXISTS"
})
print(create_next_edge_type.json())
