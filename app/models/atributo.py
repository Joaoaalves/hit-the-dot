class AtributoServico():

        def __init__(self, data):
                self.id = data['id'] if 'id' in data else None
                self.name = data['name']
                self.servico = data['servico']
                self.type = data['type']
                self.default_value = data['default_value']

        def set_value(self, value):
                self.value = value

        def to_json(self):
                return {
                        'id': self.id,
                        'servico': self.servico,
                        'type': self.type,
                        'default_value': self.default_value
                }
