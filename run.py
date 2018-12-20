from eve import Eve
import jsonref
from flask_cors import CORS

import components.event_hooks as hooks

from components.c_basic_auth import CBasicAuth
from components.c_validator import CValidator


def read_json(path):
    with open(path) as json_file:
        d = jsonref.load(json_file)
    return d


def merge_dicts(arr):
    if not arr: return {}
    merged = arr[0].copy()
    for d in arr[1:]:
        merged.update(d)
    return merged


domain = {
    "users": read_json('./domain/users.json'),
    "teams": read_json('./domain/teams.json'),
    "events": read_json('./domain/events.json'),
    "event_chains": read_json('./domain/event_chains.json'),
    "event_invites": read_json('./domain/event_invites.json'),
    "subscriptions": read_json('./domain/subscriptions.json'),
}

db_config = read_json('./config/mongo.json')
server_config = read_json('./config/server.json')

config = merge_dicts([server_config, db_config])
config['DOMAIN'] = domain

app = Eve(
    settings=config,
    validator=CValidator,
    auth=CBasicAuth
)

CORS(app)

if __name__ == '__main__':
    app.run()
