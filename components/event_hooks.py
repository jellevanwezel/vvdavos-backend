import flask
from flask import g


# logic

def get_current_user():
    username = g.get('user')
    return flask.current_app.data.driver.db['users'].find_one({"email": username})


def user_is_admin(user):
    return 'admin' in user['role']


def in_team_lookup(lookup):
    user = get_current_user()
    if user_is_admin(user):
        return
    lookup["team_id"] = {"$eq": user['team_id']}


def owns_lookup(lookup, col):
    user = get_current_user()
    if user_is_admin(user):
        return
    lookup[col] = {"$eq": user['_id']}


# global hooks

def only_admin_hook():
    if not user_is_admin(get_current_user()):
        flask.abort(401)


# local hooks

# event hooks

def pre_event_get_hook(resource, request, lookup):
    in_team_lookup(lookup)


# user hooks

def pre_user_patch_hook(resource, request, lookup):
    owns_lookup(lookup, '_id')

def on_event_created(resource, request, lookup):
    pass
    #todo, create subscriptions.
