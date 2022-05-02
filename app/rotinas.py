from datetime import date, datetime, timedelta
from workalendar.america import BrazilDistritoFederal
import csv
import os
from random import randint
import mysql.connector
from configparser import ConfigParser

config = ConfigParser()
config.read('config/mysql.ini')
    
MYSQL_USER = config['MYSQL']['user']
MYSQL_PASSWORD = config['MYSQL']['password']

def finaliza_turno(funcionario, turno):
    
    from app import db
    turno_in_minutes = funcionario.turno * 3600

    half_turno = timedelta(seconds=turno_in_minutes/2)
 
    turno.hora_saida = turno.hora_entrada + half_turno

    turno.current_status = 'clocked_out'
    
    db.update_data('turnos', turno.id, vars(turno))

def adiciona_falta(funcionario, now):
    from app import db
    db.insert_data('faltas', {
        'data' : now,
        'func_id' : funcionario.id,
        'current_status' : 'falta'
    })

def check_turnos():
    from app import db
    now = datetime.now()
    list_ferias = db.get_all_ferias()

    if BrazilDistritoFederal().is_working_day(day=now):
        from app import db
        for ferias in list_ferias:
            if ferias.is_working_day(now.date()):
                funcionarios = db.get_all_funcionarios()

                for funcionario in funcionarios:
                    turno_hoje = db.get_turno(now.date(), funcionario.id)
                    if turno_hoje:
                        if turno_hoje.current_status == 'clocked_in':       
                            finaliza_turno(funcionario, turno_hoje)
                    else:
                        if funcionario.is_active:
                            adiciona_falta(funcionario, now.date())
                break
            
     
def backup_db():
    
    now = datetime.now()
    date_string = f"{'%.2d' % now.day}-{'%.2d' % now.month}-{now.year}"
    filename = f"backups/{date_string}.sql"
    
    write_backup_file(filename)
    #write_backup_db(date_string)
    
    # Remove old backups
    old_backup_date = now - timedelta(days=15)
    old_date_string = f"{'%.2d' % old_backup_date.day}-{'%.2d' % old_backup_date.month}-{old_backup_date.year}"
    old_backup_filename = f"backups/{old_date_string}.sql"

    remove_old_backup_db(old_date_string.replace('-', '_'))
    remove_old_backup_file(old_backup_filename)
    
    
def write_backup_file(filename):
    try:
        os.system('mysqldump htd > ' + filename)
        
        os.chmod(filename, 600)
        
    except Exception as e:
        print(e)
        
    
def write_backup_db(date_string):
    from app import db
    
    mysql_db_name = date_string.replace('-', '_')
    
    collections = ['cargos', 'faltas', 'ferias', 'turnos', 'users']
    try:
        create_database(mysql_db_name)
        create_tables(mysql_db_name)

        cnx = get_database_connection()
        
        with cnx.cursor() as cursor:
            cursor.execute(f'USE {mysql_db_name}')
            
            for collection in collections:
                rows = db.get_table_data()

                for row in rows:
                    placeholders = ', '.join(['%s'] * len(row))
                    columns = ', '.join(row.keys())
                    sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % (collection, columns, placeholders)
                    iterator = cursor.execute(sql, tuple(row.values()), multi=True)
            

        cnx.commit()
        cnx.close()
    except Exception as e:
        print(e)

def get_database_connection():
    try: 
        return mysql.connector.connect(
            host="localhost",
            user=MYSQL_USER, 
            password=MYSQL_PASSWORD
        )
    except Exception as e:
        print(e)
            
def create_database(mysql_db_name):
    try:
        
        cnx = get_database_connection()
        cursor = cnx.cursor()
        
        cursor.execute(f'CREATE DATABASE IF NOT EXISTS {mysql_db_name}')

        cnx.close()
        
    except Exception as e:
        print(e)    

def create_tables(mysql_db_name):
    
    try:
        cnx = get_database_connection()

        with open('create_backup_db.sql', 'r') as f:
            with cnx.cursor() as cursor:    
                cursor.execute(f'USE {mysql_db_name}')
                cursor.execute(f.read(), multi=True)
        
        cnx.close()  
    except Exception as e:
        print(e)      

def remove_old_backup_db(date_string):
    try:
        conn = get_database_connection()
        with conn.cursor() as cursor:
            query = f'DROP DATABASE {date_string}';
            cursor.execute(query)
            
        conn.commit()
        conn.close()
        
    except Exception as e:
        print(e)

def remove_old_backup_file(filename):
    try:
        if os.path.exists(filename):
            os.remove(filename)
        
    except Exception as e:
        print(e)
