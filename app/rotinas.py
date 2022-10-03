from datetime import date, datetime, timedelta
from workalendar.america import BrazilDistritoFederal
import csv
import os
from random import randint
import mysql.connector
from configparser import ConfigParser
from app.controllers.Push.utils import trigger_push_notification
from app.models.turno import Turno
from app import app

config = ConfigParser()
config.read('config/mysql.ini')
    
MYSQL_USER = config['MYSQL']['user']
MYSQL_PASSWORD = config['MYSQL']['password']

def finaliza_turno(funcionario, turno):
    
    from app import db
    turno_in_minutes = funcionario.turno * 3600

        
    half_turno = timedelta(seconds=turno_in_minutes/2)
    
    turno.hora_saida = turno.hora_entrada + half_turno

    if turno.current_status == 'break_in':
        turno.fim_almoco = turno.hora_saida

    turno.current_status = 'clocked_out'
    
    db.update_data('Turnos', turno.id, vars(turno))


def adiciona_falta(funcionario):
    from app import db
    now = datetime.now().date()
    db.insert_data('Faltas', {
        'data' : now,
        'user_id' : funcionario.id,
        'current_status' : 'falta'
    })


def check_turnos():
    from app import db

    now = datetime.now()
    current_date = now.date()

    list_ferias = db.get_all_ferias()

    if BrazilDistritoFederal().is_working_day(day=now):
        if list_ferias:
            for ferias in list_ferias:
                if not ferias.is_working_day(current_date):
                    return

        funcionarios = db.get_all_funcionarios()

        for funcionario in funcionarios:
            turno_hoje = db.get_turno(current_date, funcionario.id)
                    
            if turno_hoje:
                # Finaliza turno ao fim do dia caso o funcionario tenha esquecido
                if turno_hoje.current_status != 'clocked_out':       
                    finaliza_turno(funcionario, turno_hoje)

            else:
                # Caso o funcionario esteja ativo e não tenha turno no dia, uma falta é adicionada
                if funcionario.is_active:
                    adiciona_falta(funcionario)
            

def backup_db():
    
    now = datetime.now()
    date_string = f"{'%.2d' % now.day}-{'%.2d' % now.month}-{now.year}"
    filename = f"backups/{date_string}.sql"
    
    write_backup_file(filename)
    
    # Remove old backups
    old_backup_date = now - timedelta(days=15)
    old_date_string = f"{'%.2d' % old_backup_date.day}-{'%.2d' % old_backup_date.month}-{old_backup_date.year}"
    old_backup_filename = f"backups/{old_date_string}.sql"

    remove_old_backup_file(old_backup_filename)
    
    
def write_backup_file(filename):
    try:
        os.system('mysqldump --defaults-file=~/.my.cnf htd > ' + filename)
        
        os.chmod(filename, 600)
        
    except Exception as e:
        app.logger.warning(e)

def remove_old_backup_file(filename):
    try:
        if os.path.exists(filename):
            os.remove(filename)
        
    except Exception as e:
        app.logger.warning(e)

def notifica_turnos():
    from app import db
    turnos_abertos = [Turno(t) for t in db.select('Turnos', 'current_status', '=' ,'clocked_in')]
    for turno in turnos_abertos:
        
            now = datetime.now()
        
            turno.hora_saida = timedelta(seconds=now.second, minutes=now.minute, hours=now.hour)
            turno.set_tempo_total()
    
            tempo_total = turno.turno_funcionario * 3600

            tempo_restante = tempo_total - turno._segundos_totais
            if tempo_restante <= 360 and tempo_restante > 0:
                funcionario = db.get_funcionario(turno.user_id)
                push = db.get_push(funcionario.id)
                if push:
                    trigger_push_notification(push, f'{funcionario.name}, faltam menos de 5 minutos para seu turno finalizar')