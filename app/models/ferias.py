from datetime import datetime
from os import times

class Ferias():
    
    def __init__(self, data):
        if 'id' in data:
            self.id = data['id']
        self.inicio = data['inicio']
        self.fim = data['fim']
                
    def formated_inicio(self):
        return datetime.strftime(self.inicio, '%d/%m/%Y')
        
    def formated_fim(self):
        return datetime.strftime(self.fim, '%d/%m/%Y')
    
    def formated_inicio_html(self):
        return datetime.strftime(self.inicio, '%Y-%m-%d')
        
    def formated_fim_html(self):
        return datetime.strftime(self.fim, '%Y-%m-%d')

    def is_working_day(self, date):
        return self.inicio > date or date > self.fim

    def to_json(self):
        return {
            'inicio' : self.inicio,
            'fim' : self.fim
        }