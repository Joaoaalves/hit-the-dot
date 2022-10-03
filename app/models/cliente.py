class Cliente():

    def __init__(self, data):

        self.id = data['id'] if 'id' in data else None
        self.name = data['name']
        
    def to_json(self):
        return {
            'name' : self.name
        }