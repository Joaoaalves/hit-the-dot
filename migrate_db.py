from app import db
from app.models.turno import Turno
from app.models.ferias import Ferias
from app.models.falta import Falta

import mysql.connector


MYSQL_USER = 'htd'
MYSQL_PASSWORD = 'dbs2021'

def get_database_connection():
    try: 
        return mysql.connector.connect(
            host="localhost",
            user=MYSQL_USER, 
            password=MYSQL_PASSWORD
        )
    except Exception as e:
        print(e)

def insert_into_db(data, table):
    cnx = get_database_connection()
    with cnx.cursor() as cursor:
        cursor.execute('USE htd;')
        for t in data:
            row = t.to_json()
            placeholders = ', '.join(['%s'] * len(row))
            columns = ', '.join(row.keys())
            sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % (table,  columns, placeholders)
            iterator = cursor.execute(sql, tuple(row.values()), multi=True)

    cnx.commit()
    cnx.close()


# Turnos
turnos = [Turno(t) for t in db.get_all_rows_from_firestore('Turnos')]
cnx = get_database_connection()
with cnx.cursor() as cursor:
    cursor.execute('USE htd;')
    for t in turnos:
        if t.current_status == 'clocked_out':
            row = t.to_json()
            placeholders = ', '.join(['%s'] * len(row))
            columns = ', '.join(row.keys())
            sql = "INSERT INTO turnos ( %s ) VALUES ( %s )" % ( columns, placeholders)
            iterator = cursor.execute(sql, tuple(row.values()), multi=True)

    cnx.commit()
    cnx.close()

# Ferias
ferias = [Ferias(f) for f in db.get_all_rows_from_firestore('Ferias')]
insert_into_db(ferias, 'ferias')

# Feriados
feriados = [f for f in db.get_all_rows_from_firestore('Feriados')]
cnx = get_database_connection()
with cnx.cursor() as cursor:
    cursor.execute('USE htd;')
    for t in feriados:
        row = t
        row['repete'] = int(row['repeat'])
        row.pop('repeat')
        row.pop('id')
        data = row['date']
        row.pop('date')
        row['dia'] = int(data[:2])
        row['mes'] = int(data[3:5])
        if row['repete'] == 0:
            row['ano'] = int(data[6:])
        
        row['nome'] = row['name']
        row.pop('name')
        
        placeholders = ', '.join(['%s'] * len(row))
        columns = ', '.join(row.keys())
        sql = "INSERT INTO feriados ( %s ) VALUES ( %s )" % ( columns, placeholders)
        iterator = cursor.execute(sql, tuple(row.values()), multi=True)

    cnx.commit()
    cnx.close()

# Faltas
faltas = [Falta(f) for f in db.get_all_rows_from_firestore('Faltas')]
insert_into_db(faltas, 'faltas')

def write_backup_db():
    
    collections = ['Cargos', 'Users']
    try:

        cnx = get_database_connection()
        
        with cnx.cursor() as cursor:
            cursor.execute(f'USE htd')
            
            for collection in collections:
                rows = db.get_all_rows_from_firestore(collection)

                for row in rows:
                    placeholders = ', '.join(['%s'] * len(row))
                    columns = ', '.join(row.keys())
                    sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % (collection.lower(), columns, placeholders)
                    iterator = cursor.execute(sql, tuple(row.values()), multi=True)
            

        cnx.commit()
        cnx.close()
    except Exception as e:
        print(e)

write_backup_db()

