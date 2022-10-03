class TagServico():

        def __init__(self, data):
                self.id = data['id'] if 'id' in data else None
                self.tag = data['tag']
                self.servicos = None

        def set_servicos(self, servicos):
                self.servicos = servicos
        
        def num_servicos(self):
                return len(self.servicos)
                
        def to_json(self):
                return {
                        'id': self.id,
                        'tag' : self.tag
                }
        