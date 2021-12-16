from datetime import datetime

class Falta():
    
    def __init__(self, data):
        self.id = data['id']
        self.date = datetime.strptime(data['date'], '%d/%m/%Y')    
        self.current_status = data['current_status']
        
        try:
            self.func_id = int(data['func_id'])    
        except:
            return None
        
    def get_formated_date(self):
        return f"{'%.2d' % self.date.day}/{'%.2d' % self.date.month}/{self.date.year}"

    def abonar(self):
        self.current_status = 'abonada'
        
    def to_json(self):
        
        return {
            'id' : self.id,
            'date' : self.get_formated_date(),
            'func_id' : self.func_id,
            'current_status' : self.current_status
        }