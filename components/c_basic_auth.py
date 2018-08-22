import flask
from eve.auth import BasicAuth


class CBasicAuth(BasicAuth):  # todo hash obviously

    def check_auth(self, username, password, allowed_roles, resource, method):
        users = flask.current_app.data.driver.db['users']
        user = users.find_one({'email': username})
        if user is None: return False
        roles = self.check_roles(user['role'], allowed_roles, method)
        account = "password" in user and user['password'] == password
        return account and roles

    def check_roles(self, user_roles, allowed_roles, method):
        for role_dict in allowed_roles:
            if role_dict['role'] in user_roles and method in role_dict['methods']:
                return True
        return False