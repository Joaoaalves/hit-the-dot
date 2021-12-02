from . import db
from . import datetime
import numpy as np

def get_all_feriados():
    dates = db.get_all_rows_from_firestore('Feriados', 'date')

    return treat_dates(dates)

def get_feriado(feriado_id):
    feriados = db.get_all_rows_from_firestore('Feriados')
    
    for f in feriados:
        if f['id'] == feriado_id:
            return f
        
    return None    

def treat_dates(dates):
    current_year = str(datetime.now().year)
    treated_dates = list()
    
    for d in dates:
        d = d.replace('/', '-')
        if current_year in d:
            treated_dates.append(d)
            
        else:
            treated_dates.append(d + '-' + current_year)
            
    return treated_dates
            
            
            
def get_date_range():
    
    current_year = str(datetime.now().year)
    
    return f'01-01-{current_year}', f'31-12-{current_year}'

def generate_id():
    ids = db.get_all_rows_from_firestore('Feriados', 'id')
    if ids:
        return int(np.amax(ids)) + 1

    return 1
    
def create_feriado(form):
    date = form['date'].replace('-', '/')
    nome = form['name']
    
    repeat = (form['repeat'] == 'true')
    
    if repeat:
        date = date[:5]
    
    data = {
        'id' : generate_id(),
        'name' : nome,
        'date' : date,
        'repeat' : repeat
    }
    
    db.add_data_on_firestore('Feriados', data)
    
    
def edit_feriado(form, feriado):
    
    feriado['name'] = form['name']
    feriado['repeat'] = form['repeat']
    
    date = form['date'].replace('-', '/')
    
    if feriado['repeat']:
        feriado['date'] = date[:5]
    else:
        feriado['date'] = date
    

    db.update_info('Feriados', feriado, key='id', value=feriado['id'])

def treat_date(feriado):
    date = feriado['date']
    
    if feriado['repeat']:
        current_year = str(datetime.now().year)
        date = f"{date}/{current_year}"
        
    date = date.replace('/', '-')
    month = date[3:5]
    
    return date, month