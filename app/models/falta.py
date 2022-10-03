from datetime import datetime

class Falta():
    
    def __init__(self, data):
        self.id = data['id']
        self.date = data['data']
        self.current_status = data['current_status']
        
        try:
            self.user_id = int(data['user_id'])    
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
            'user_id' : self.user_id,
            'current_status' : self.current_status
        }