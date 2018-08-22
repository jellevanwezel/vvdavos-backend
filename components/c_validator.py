import flask
from bson import ObjectId
from eve.io.mongo import Validator
from flask import g


class CValidator(Validator):

    def get_current_user(self):
        username = g.get('user')
        return flask.current_app.data.driver.db['users'].find_one({"email":username})

    #check if a relation exists
    def _validate_relationexists(self, rel_dict, field, value):
        if value is None: return
        rel_col = flask.current_app.data.driver.db[rel_dict["col_name"]]
        if rel_col.find_one({rel_dict["rel_key"]: ObjectId(value)}) is None:
            desc = "Relation for collection: {}, with: {}: {}, not found".format(rel_dict["col_name"], rel_dict["rel_key"], value)
            self._error(field, desc)

    def _validate_player_owns_subscription(self, user_key, field, value):
        user = self.get_current_user()
        invite_table = flask.current_app.data.driver.db['event_invites']
        invite = invite_table.find_one({'_id':self._id})
        return ObjectId(invite[user_key]) == user['_id']