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
    if repete:
        data['ano'] = ano

    feriado = Feriado(data)
    
    db.insert_data('feriados', feriado.to_json())
    
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
    

    db.update_data('feriados', feriado.id, feriado.to_json())
