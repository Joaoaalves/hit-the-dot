from .tarefa import Tarefa
from app import db
from datetime import datetime
class Cliente():

    def __init__(self, data):

        self.id = data['id']
        self.nome = data['nome']
        
        self.tarefas = list()
        self.set_tarefas(data['tarefas'])

        self.funcionario_responsavel = data['funcionario_responsavel']

        self.data_inicio = datetime.fromtimestamp(data['data_inicio'])
        self.data_fim = datetime.fromtimestamp(data['data_fim'])

    def get_data_inicio_str(self):
        return self.data_inicio.strftime('%d/%m/%Y %H:%M')

    def get_data_fim_str(self):
        return self.data_fim.strftime('%d/%m/%Y %H:%M')

    def set_tarefas(self, data):
        self.tarefas = [db.get_tarefa(id) for id in data]
    
    def to_json(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'tarefas': [tarefa.id for tarefa in self.tarefas],
            'funcionario_responsavel': self.funcionario_responsavel,
            'data_inicio': self.data_inicio.timestamp(),
            'data_fim': self.data_fim.timestamp()
        }