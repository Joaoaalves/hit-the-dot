class TarefaAtribuida:
    
    _aprovacao = False
    
    def __init__(self, data):
        
        self.id = data['id']
        self.id_tarefa = data['id_tarefa']
        self.funcionario = data['funcionario']
        self.data_inicio = data['data_inicio']
        self.data_fim = data['data_fim']
        self._aprovacao = data['aprovacao']
        
    def set_aprovacao(self,aprovacao):
        self._aprovacao = aprovacao
        
    def get_aprovacao(self):
        return self._aprovacao