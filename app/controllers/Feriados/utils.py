from . import db
from . import datetime
import numpy as np
from app.models.feriado import Feriado
            
        
def create_feriado(form):
    ano, mes, dia = form['date'].split('-')

    repete = (form['repete'] == 'true')
    data = {
        'nome' : form['nome'],
        'dia' : dia,
        'mes' : mes,
        'repete' : repete
    }
    if not repete:
        data['ano'] = ano

    feriado = Feriado(data)
    
    db.insert_data('Feriados', feriado.to_json())
    
def edit_feriado(form, feriado):
    ano, mes, dia = form['date'].split('-')
    feriado.dia = dia
    feriado.mes = mes
    feriado.nome = form['nome']
    if form['repete'] == 'true':
        feriado.repete = True
        feriado.ano = None
    
    else:
        feriado.repete = False
        feriado.ano = ano
    

    db.update_data('Feriados', feriado.id, feriado.to_json())

def filtra_feriados_by_date(all_feriados, feriados, mes):
    ano, mes = mes.split('-')

    for f in all_feriados:
        if f.repete and f.mes == int(mes):
            feriados.append(f)
        else:
            if f.mes == int(mes) and f.ano == int(ano):
                feriados.append(f)
    return feriados