class Pontuacao:
       
    def __init__(self, data):
        
        self.data_consolidacao = data['data_consolidacao']
        
        try:
            self.id = int(data['id'])
            self.pontuacao = int(data['pontuacao'])
            self.funcionario = int(data['funcionario'])
        
        except Exception as e:
            raise e