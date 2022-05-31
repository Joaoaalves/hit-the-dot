class ServicoAtribuido():

        def __init__(self, data):

                self.id = data['id'] if 'id' in data else None
                self.service_id = data['service_id']
                self.user_id = data['user_id']
                self.status = data['status']
                self.cliente_id = data['cliente_id']
                self.link_trello = data['link_trello']
                
                try:
                        self.is_verified = int(data['is_verified']) == 1
                
                except:
                        self.is_verified = data['is_verified'] == True

        
        def to_json(self):
                return {
                        'id' : self.id,
                        'service_id' : self.service_id,
                        'user_id' : self.user_id,
                        'status' : self.status,
                        'cliente_id' : self.cliente_id,
                        'link_trello' : self.link_trello,
                        'is_verified' : self.is_verified
                }