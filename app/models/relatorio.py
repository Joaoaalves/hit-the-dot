from datetime import datetime

class Relatorio():
    def __init__(self, data):
        self.id = data['id']
        self.date = datetime.fromtimestamp(data['date'])
        self.day = self.date.day
        self.month = self.date.month
        self.year = self.date.year
        self.user_id = data['user_id']
        self.tarefas = data['tarefas']
        
    def get_dia_str(self):
        return f'{self.day}/{self.month}/{self.year}'
    
    def get_dia_html(self):
        return f'{self.year}-{self.month}-{self.day}'
    def to_json(self): 
        return {
            'date' : datetime.timestamp(self.date),
            'user_id' : self.user_id,
            'tarefas' : self.tarefas
        }