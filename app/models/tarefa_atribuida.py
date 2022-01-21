import datetime

class TarefaAtribuida:
    
    _aprovacao = False
    
    def __init__(self, data):
        
        self.id = data['id']
        self.id_tarefa = data['id_tarefa']
        self.funcionario = data['funcionario']
        self.data_inicio = datetime.datetime.fromtimestamp(data['data_inicio'])
        self.data_fim = datetime.datetime.fromtimestamp(data['data_fim'])
        self._aprovacao = data['aprovacao']
        
    def set_aprovacao(self,aprovacao):
        self._aprovacao = aprovacao
        
    def get_aprovacao(self):
        return self._aprovacao

    def get_data_inicio_str(self):
        return self.data_inicio.strftime('%d/%m/%Y %H:%M')

    def get_data_fim_str(self):
        return self.data_fim.strftime('%d/%m/%Y %H:%M')
        
    def to_json(self):
        return {
            'id': self.id,
            'id_tarefa': self.id_tarefa,
            'funcionario': self.funcionario,
            'data_inicio': self.data_inicio.timestamp(),
            'data_fim': self.data_fim.timestamp(),
            'aprovacao': self._aprovacao
        }