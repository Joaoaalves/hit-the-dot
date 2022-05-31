class Servico():

        def __init__(self, data):
                self.id = data['id'] if 'id' in  data else None

                self.name = data['name']
                self.valor = data['valor']
                self.tempo = data['tempo']
                self.categoria = data['categoria']

        def to_json(self):
                return {
                        'id' : self.id,
                        'name' : self.name,
                        'tempo' : self.tempo,
                        'categoria' : self.categoria
                }
                