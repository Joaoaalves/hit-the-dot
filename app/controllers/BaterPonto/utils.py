from datetime import timedelta
from . import datetime, db, app

def get_current_shift(user_id):
    current_date = get_current_date()
    
    query = db.get_turno(current_date, user_id)
    
    for s in query:
        return s.to_dict()
    
    
def get_current_date():
    now = datetime.now()
    return f"{now.day:02d}/{now.month:02d}/{now.year:04d}"

def is_dia_util():
    now = datetime.now()
    
    # Sabado ou domingo
    if now.weekday() > 4:
        return False
    
    current_date = get_current_date()
    timestamp_now = now.timestamp()
    
    feriados = db.get_all_rows_from_firestore('Feriados', 'date')
    list_ferias = db.get_all_ferias()
    
    if current_date[:5] in feriados:
        return False
    
    if list_ferias:
        for ferias in list_ferias:
            if ferias.is_working_day(timestamp_now):
                return False
        
    return True
    
def get_current_shift_time(turno):
    
    now = datetime.now()
    
    inicio_turno = turno.converter_str_datetime(turno.hora_entrada)
    
    correct_date = datetime(day=now.day, month=now.month, year=now.year, 
                            hour=inicio_turno.hour, minute=inicio_turno.minute, 
                            second=inicio_turno.second)

    return int((now - correct_date).total_seconds() - turno.get_tempo_almoco().seconds) if turno.almocou and 'fim_almoco' in vars(turno) else int((now - correct_date).total_seconds()) 


app.jinja_env.globals.update(is_dia_util=is_dia_util)