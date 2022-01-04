from datetime import datetime, timedelta
from workalendar.america import BrazilDistritoFederal
import csv
import os
from random import randint
import mysql.connector
from configparser import ConfigParser

def finaliza_turno(funcionario, turno):
    
    from app import db
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
    from app import db
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
        from app import db
        for ferias in list_ferias:
            if ferias.is_working_day(now.timestamp()):
                funcionarios = db.get_all_funcionarios()
                now = f"{'%.02d' % now.day}/{'%.02d' % now.month}/{now.year}"
                for funcionario in funcionarios:
                    turno_hoje = db.get_turno(now, funcionario.id)
                    if turno_hoje:
                        if turno_hoje.current_status == 'clocked_in':       
                            finaliza_turno(funcionario, turno_hoje)
                    else:
                        adiciona_falta(funcionario, now)
                break
     
def backup_db():
    
    now = datetime.now()
    date_string = f"{'%.2d' % now.day}-{'%.2d' % now.month}-{now.year}"
    filename = f"backups/{date_string}.csv"

    write_backup_file(filename)
    #write_backup_db(date_string)
    
def write_backup_file(filename):
    collections = ['Cargos', 'Faltas', 'Feriados', 'Ferias', 'Turnos', 'Users']
    from app import db
    
    with open(filename, 'w', newline='\n') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"')
        
        for collection in collections:
            rows = db.get_all_rows_from_firestore(collection)
            for row in rows:
                writer.writerow([collection, row])
                
    os.chmod(filename, 000)
    
def write_backup_db(date_string):
    from app import db
    config = ConfigParser()
    config.read('config/mysql.ini')
    
    user = config['MYSQL']['user']
    password = config['MYSQL']['password']
    
    cnx = mysql.connector.connect(
        host="localhost",
        user=user, 
        password=password
    )

    cursor = cnx.cursor()
    
    create_database(cursor, date_string)
    create_tables(cursor)

    collections = ['Cargos', 'Faltas', 'Feriados', 'Ferias', 'Turnos', 'Users']

    for collection in collections:
        rows = db.get_all_rows_from_firestore(collection)

        for row in rows:
            placeholders = ', '.join(['%s'] * len(row))
            columns = ', '.join(row.keys())
            sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % (collection, columns, placeholders)
            cursor.execute(sql, list(row.values()))
            
def create_database(cursor, date_string):
    mysql_table_name = date_string.replace('-', '_')
    
    cursor.execute(f'CREATE DATABASE IF NOT EXISTS {mysql_table_name}')

    cursor.execute(f'USE {mysql_table_name}')

def create_tables(cursor):
    with open('create_backup_db.sql', 'r') as f:    
        cursor.execute(f.read(), multi=True)

def generate_falta_id():
    from app import db
    ids_faltas = db.get_all_rows_from_firestore('Ferias', 'id')
    
    while True:
        new_id = randint(10000, 99999)
        if new_id not in ids_faltas:
            return new_id
