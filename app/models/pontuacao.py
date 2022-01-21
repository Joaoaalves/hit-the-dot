from datetime import datetime

class Pontuacao:
       
    def __init__(self, data):
        
        self.data_consolidacao = datetime.fromtimestamp(data['data_consolidacao'])
        
        try:
            self.id = int(data['id'])
            self.pontuacao = int(data['pontuacao'])
            self.funcionario = int(data['funcionario'])
        
        except Exception as e:
            raise e

    def get_data_consolidacao_str(self):
        return self.data_consolidacao.strftime('%d/%m/%Y %H:%M')

    def to_json(self):
        return {
            'id': self.id,
            'pontuacao': self.pontuacao,
            'funcionario': self.funcionario,
            'data_consolidacao': self.data_consolidacao.timestamp()
        }