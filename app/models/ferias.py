from datetime import datetime
from os import times

class Ferias():
    
    def __init__(self, data):
        self.id = data['id']
        self.set_inicio_ferias(data['inicio'])
        self.set_fim_ferias(data['fim'])
    
    def set_inicio_ferias(self, inicio):
        self.inicio = datetime.fromtimestamp(inicio)
        self.timestamp_inicio = inicio
        
    def set_fim_ferias(self, fim):
        self.fim = datetime.fromtimestamp(fim)
        self.timestamp_fim = fim
                
    def formated_inicio(self):
        return f"{'%.2d' % self.inicio.day}/{ '%.2d' % self.inicio.month}/{self.inicio.year}"
        
    def formated_fim(self):
        return f"{'%.2d' % self.fim.day}/{ '%.2d' % self.fim.month}/{self.fim.year}"
    
    def formated_inicio_html(self):
        return f"{self.inicio.year}-{'%.2d' % self.inicio.month}-{'%.2d' % self.inicio.day}"
        
    def formated_fim_html(self):
        return f"{self.fim.year}-{'%.2d' % self.fim.month}-{'%.2d' % self.fim.day}"
    def is_working_day(self, timestamp):
        return self.timestamp_inicio > timestamp or timestamp > self.timestamp_fim
        

    def to_json(self):
        return {
            'id' : self.id,
            'inicio' : self.timestamp_inicio,
            'fim' : self.timestamp_fim
        }