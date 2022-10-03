from re import M
from time import strptime


from datetime import datetime

class ServicoEntregue():

        def __init__(self, data):

                self.id = data['id'] if 'id' in data else None
                self.service_id = data['service_id']
                self.user_id = data['user_id']
                self.status = data['status']
                self.cliente_id = data['cliente_id']
                self.link_trello = data['link_trello']
                self.entrega = data['entrega']
                self.descricao = data['descricao'] if 'descricao' in data else ''
                self.prazo = data['prazo'] if 'prazo' in data else None
                self.valor = data['valor'] if 'valor' in data else None 

        def get_formated_date(self):
                return datetime.strftime(self.entrega, '%d/%m/%Y')
                
          
        def to_json(self):
                return {
                        'id' : self.id,
                        'service_id' : self.service_id,
                        'user_id' : self.user_id,
                        'status' : self.status,
                        'cliente_id' : self.cliente_id, 
                        'link_trello' : self.link_trello,
                        'entrega' : datetime.strftime(self.entrega, '%Y-%m-%d'),
                        'descricao' : self .descricao,
                        'prazo' : self.prazo,
                        'valor' : self.valor
                }