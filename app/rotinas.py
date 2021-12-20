from numpy import half
from app import db, app
from datetime import datetime, timedelta
from workalendar.america import BrazilDistritoFederal
from app.models.falta import Falta
from random import randint

def finaliza_turno(funcionario, turno):
    
    turno_in_minutes = funcionario.turno * 3600

    half_turno = timedelta(seconds=turno_in_minutes/2)

    hour,minute,seconds = turno.hora_entrada.split(':')
    
    inicio_turno_segundos = (int(hour) * 3600) + (int(minute) * 60) + (int(seconds))
    
    inicio_turno = timedelta(seconds=inicio_turno_segundos)
    
    fim_turno = inicio_turno + half_turno
    
    turno.hora_saida = str(fim_turno)
    
    turno.current_status = 'clocked_out'
    
    db.update_info('Turnos', turno.to_json(), query_arr=[['dia', turno.dia], ['user_id', funcionario.id]])

def adiciona_falta(funcionario, now):
    
    db.add_data_on_firestore('Faltas', {
        'date' : now,
        'id' : generate_falta_id(),
        'func_id' : funcionario.id,
        'current_status' : 'falta'
    })
    
def check_turnos():
    now = datetime.now()
    list_ferias = db.get_all_ferias()

    if BrazilDistritoFederal().is_working_day(day=now):
        app.logger.info(f'Inicializando finalização de turnos não finalizados: {str(now)}')
        for ferias in list_ferias:
            if ferias.is_working_day(now.timestamp()):
                funcionarios = db.get_all_funcionarios()
                now = f"{'%.02d' % now.day}/{'%.02d' % now.month}/{now.year}"
                for funcionario in funcionarios:
                    turno_hoje = db.get_turno(now, funcionario.id)
                    if turno_hoje:
                        if turno_hoje.current_status == 'clocked_in':       
                            #finaliza_turno(funcionario, turno_hoje)
                            print(vars(turno_hoje))
                            
                    else:
                        adiciona_falta(funcionario, now)
                break
            
def generate_falta_id():
    
    ids_faltas = db.get_all_rows_from_firestore('Ferias', 'id')
    
    while True:
        new_id = randint(10000, 99999)
        if new_id not in ids_faltas:
            return new_id