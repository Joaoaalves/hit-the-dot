import json

class User:

    _privilege = 1

    def __init__(self, data):
        self.id = int(data['id'])
        self.name = data['name']
        self.email = data['email']

    def get_privilege(self):
        return self._privilege

    def to_json(self):
        return vars(self)

    def from_json(self, json_data):
        session = json.dumps(json_data)
        user_data = session['user']
        try:
            self.id = int(user_data['id'])
            self.name = user_data['name']
            self.email = user_data['email']
        
        except Exception as e:
            return e

    