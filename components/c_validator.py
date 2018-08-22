import flask
from bson import ObjectId
from eve.io.mongo import Validator


class CValidator(Validator):
    def _validate_relationexists(self, rel_dict, field, value):
        if value is None: return
        rel_col = flask.current_app.data.driver.db[rel_dict["col_name"]]
        if rel_col.find_one({rel_dict["rel_key"]: ObjectId(value)}) is None:
            desc = "Relation for collection: {}, with: {}: {}, not found".format(rel_dict["col_name"], rel_dict["rel_key"], value)
            self._error(field, desc)
