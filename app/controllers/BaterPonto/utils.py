from . import datetime, db    

def get_current_shift(user_id):
    current_date = get_current_date()
    
    query = db.get_turno(current_date, user_id)
    
    for s in query:
        return s.to_dict()
    
    
def get_current_date():
    now = datetime.now()
    return f"{now.day:02d}/{now.month:02d}/{now.year:04d}"