from app import db, app
from datetime import datetime, timedelta
from workalendar.america import BrazilDistritoFederal
import csv
import os

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

def check_turnos():
    now = datetime.now()
    if BrazilDistritoFederal().is_working_day(day=now):
        funcionarios = db.get_all_funcionarios()
        app.logger.info(f'Inicializando finalização de turnos não finalizados: {str(now)}')
        now = f"{'%.02d' % now.day}/{'%.02d' % now.month}/{now.year}"
        for funcionario in funcionarios:
            turno_hoje = db.get_turno(now, funcionario.id)
            if turno_hoje and turno_hoje.current_status == 'clocked_in':       
                finaliza_turno(funcionario, turno_hoje)
                
                
def backup_db():
    collections = ['Cargos', 'Faltas', 'Feriados', 'Ferias', 'Turnos', 'Users']
    
    now = datetime.now()
    filename = f"{'%.2d' % now.day}-{'%.2d' % now.month}-{now.year}.csv"
    with open(filename, 'w', newline='\n') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"')
        
        for collection in collections:
            rows = db.get_all_rows_from_firestore(collection)
            for row in rows:
                writer.writerow([collection, row])
                
    os.chmod(filename, 000)