class Demanda():

        def __init__(self, data):

                if 'id' in data:
                        self.id = data['id']
                else:
                        self.id = None
                self.func_id = data['func_id']
                self.name = data['name']
                self.url = data['url']
                self.date = data['date']
                self.status = data['status']

        def get_formated_date(self):
                return self.date.strftime('%d/%m/%Y')
        def is_verified(self):
                return self.status == 'Verificada'

        def to_json(self):
                return {
                        'id': self.id,
                        'name': self.name,
                        'func_id' : self.func_id,
                        'url': self.url,
                        'date': self.date,
                        'status' : self.status
                }