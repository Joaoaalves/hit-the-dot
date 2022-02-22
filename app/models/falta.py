from datetime import datetime

class Falta():
    
    def __init__(self, data):
        self.id = data['id']
        self.date = data['data']
        self.current_status = data['current_status']
        
        try:
            self.func_id = int(data['func_id'])    
        except:
            return None
        
    def get_formated_date(self):
        return f"{'%.2d' % self.date.day}/{'%.2d' % self.date.month}/{self.date.year}"

    def is_abonada(self):
        return self.current_status == 'abonada'
    
    def abonar(self):
        self.current_status = 'abonada'
        
    def get_html_date(self):
        return f"{self.date.year}-{'%.2d' % self.date.month}-{'%.2d' % self.date.day}"
        
    def to_json(self):
        
        return {
            'data' : self.date,
            'func_id' : self.func_id,
            'current_status' : self.current_status
        }