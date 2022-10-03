class Pausa:
        def __init__(self, data):

                self.id = data['id'] if 'id' in data else None
                self.inicio = data['inicio']
                self.turno = data['turno']
                self.fim = data['fim'] if 'fim' in data else None
        def get_tempo(self):
                return self.fim - self.inicio

        def to_json(self):
                return {
                        'id': self.id,
                        'inicio': self.inicio,
                        'turno': self.turno,
                        'fim': self.fim
                }