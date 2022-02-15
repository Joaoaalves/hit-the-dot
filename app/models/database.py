import ast
import pyrebase
from firebase_admin import auth as admin_auth
import firebase_admin
from datetime import datetime
import subprocess
from app.models.ferias import Ferias
import mysql.connector
from configparser import ConfigParser

from .admin import Admin
from .funcionario import Funcionario
from .turno import Turno
from .cargo import Cargo
from .tarefa import Tarefa
from .falta import Falta
from .cliente import Cliente
from .feriado import Feriado

class Database():

    def __init__(self):

        # Configs firebase
        with open("config/firebase.cfg", "r") as f:
            firebase_config = ast.literal_eval(f.read())
        
        # Configs mysql
        config = ConfigParser()
        config.read('config/mysql.ini')
        self.mysql_user = config['MYSQL']['user']
        self.mysql_pass = config['MYSQL']['password']

        # Initializing firebase
        firebase = pyrebase.initialize_app(firebase_config)

        # Auth Module
        self.auth = firebase.auth()

        # Admin Module
        firebase_admin.initialize_app()
        self.__admin_auth = admin_auth

    def get_mysql_connection(self):
        return mysql.connector.connect(
            host="localhost",
            user=self.mysql_user,
            passwd=self.mysql_pass,
            database="htd"
        )
    
    # Returns authentication with email and password
    def login(self, email, password):
        return self.auth.sign_in_with_email_and_password(email, password)

    def insert_data(self, table, info):
        cnx = self.get_mysql_connection()
        with cnx.cursor() as cursor:
            placeholders = ', '.join(['%s'] * len(info))
            columns = ', '.join(info.keys())
            sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % (table,  columns, placeholders)
            
            iterator = cursor.execute(sql, tuple(info.values()), multi=True)

        cnx.commit()
        cnx.close()
    
    def remove_data(self, table, id):
        cnx = self.get_mysql_connection()
        with cnx.cursor() as cursor:
            sql = "DELETE FROM %s WHERE id = %s" % (table, id)
            cursor.execute(sql)
            affected_rows = cursor.rowcount

        cnx.commit()
        cnx.close()
        return affected_rows > 0

    def update_data(self, table, id, info):
        cnx = self.get_mysql_connection()
        with cnx.cursor() as cursor:
            sql = "UPDATE %s " % table
            sql += ' SET {}'.format(', '.join('{}=%s'.format(k) for k in info))
            sql += ' WHERE id = %s' % id

            cursor.execute(sql, tuple(info.values()))

        cnx.commit()
        cnx.close()
    

    def get_table_data(self, table):
        cnx = self.get_mysql_connection()
        rows = None
        with cnx.cursor(dictionary=True) as cursor:
            sql = "SELECT * FROM %s" % table
            cursor.execute(sql)
            rows = cursor.fetchall()

        cnx.commit()
        cnx.close()
        return rows

    def get_row_by_id(self, table, row_id):
        rows = self.select(table, 'id', '=', row_id)
        if rows:
            return rows[0]
        return None


    # Signs up a new user on Auth Module and
    # Store his info on Database
    def create_user(self, data):
        email = data['email']
        password = data['password']

        try:
            user = self.auth.create_user_with_email_and_password(email, password)

            self.auth.send_email_verification(user['idToken'])
            
            if 'password' in data:
                data.pop('password')

            self.insert_data("users", data)

        except Exception as e:
            print(e)
            return False

        return True

    # Get user info from DB and returns as an Object
    def get_user_by_id(self, id):
        try:

            u = self.get_row_by_id('users', id)
            
            if u:
                role = u['role']

                if role == 'Admin':
                    return Admin(u)

                if role == 'Funcionario':
                    return Funcionario(u)

            return None

        except Exception as e:

            return e

    def get_user_by_email(self, email):
        try:

            u = self.select('users', 'email', '=', email)[0]

            if u:
                if u['role'] == 'Funcionario':
                    return Funcionario(u)

                if u['role'] == 'Admin':
                    return Admin(u)

            return None
        except Exception as e:
            return e
  
    
    def select(self, table, key, operator, value):
        cnx = self.get_mysql_connection()
        rows = None
        with cnx.cursor(dictionary=True) as cursor:
            sql = "SELECT * FROM %s WHERE %s %s '%s'" % (table, key, operator, value)
            cursor.execute(sql)
            rows = cursor.fetchall()

        cnx.commit()
        cnx.close()
        return rows

    def multiple_select(self, table, operations):
        cnx = self.get_mysql_connection()
        rows = None
        sql = "SELECT * FROM %s WHERE " % (table)
        for op in operations:
            sql += "%s %s %s AND " % (op[0], op[1], op[2])
        sql = sql[:-4]
        with cnx.cursor(dictionary=True) as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()

        cnx.commit()
        cnx.close()
        return rows    

    def filtra_entradas(self,query_arr, collection):
        query = collection
        for q in query_arr:
            query = query.where(
                q[0], '==' ,q[1]
            )

        return query.stream()
    
        
    # Remove all user's info from app
    def remove_user(self, uid):

        user_email = self.get_user_by_id(uid)['email']
        user = self.__admin_auth.get_user_by_email(user_email)
        
        self.__admin_auth.delete_user(user.uid)

        # Remove the user's files
        subprocess.call("rm -rf app/protected/" + str(uid), shell=True)

        self.remove_data('users', uid)

    # Get all funcionarios from db
    def get_all_funcionarios(self):
        return [Funcionario(f) for f in self.select('users', 'role', '=', 'Funcionario')]
    
    def get_funcionario(self, func_id):
        
        return Funcionario(self.get_row_by_id('users', func_id))

    def get_turnos(self):

        return [Turno(t) for t in self.select('turnos', 'current_status', '=', 'clocked_out')]


    def get_turno(self, date, func_id):
        turno = self.multiple_select(
            'turnos', operations=[['dia', '=', f"'{date}'"],['user_id', '=', func_id]]
        )

        if len(turno) == 1:
            return Turno(turno[0])

        return None


    # Add new shift Status to firestore
    def add_new_shitf_status(self, new_status, funcionario):

        now = datetime.now()
        
        current_date = str(now.date())
        
        current_hour = str(now.time())[:-7]
        
        turno = self.get_turno(current_date, funcionario.id)

        if turno:
            current_status = turno.current_status
            
            if new_status == 'clock_in' and current_status == 'clocked_out':
                return False
            
            if new_status == 'clock_out' and current_status == 'clocked_in':
                self.update_data('turnos', turno.id, {'current_status': 'clocked_out','hora_saida' : current_hour})
                
            if new_status == 'break_in' and current_status == 'clocked_in':
                self.update_data('turnos', turno.id, 
                    {
                    'current_status': new_status,
                    'inicio_almoco' : current_hour,
                    'almocou' : 1
                    }
                )
                
            if new_status == 'break_out' and current_status == 'break_in':
                self.update_data('turnos', turno.id, {'current_status': 'clocked_in', 'fim_almoco' : current_hour})
            

        else:
            if new_status == 'clock_in':
                        
                data = {
                    'current_status' : 'clocked_in',
                    'dia' : current_date,
                    'hora_entrada' : current_hour,
                    'user_id' : funcionario.id,
                    'turno_funcionario' : funcionario.turno,
                    'almocou' : False
                }
                
                
                self.insert_data('turnos', data)
                
        return True
    

        
    def get_cargo(self, cargo_id):
        c = self.get_row_by_id('cargos', cargo_id)
        if c:
            return Cargo(c)
        return None   
    
    def get_cargos(self):
        return [Cargo(c) for c in self.get_table_data('cargos')]


    def get_tarefa(self, tarefa_id):

        t = self.get_row_by_id('tarefas', tarefa_id)
        if t:
            return Tarefa(t)
        
        return None
        
    def get_feriado(self, id):
        return Feriado(self.get_row_by_id('feriados', id))
        
    def get_feriados(self):        
        feriados = [Feriado(f) for f in self.get_table_data('feriados')]
            
        return feriados
        
            
    def create_ferias(self, data):
        self.insert_data('ferias', Ferias(data).to_json())
        
    def get_ferias(self, ferias_id):
        f = self.get_row_by_id('ferias', ferias_id)
        if f:
            return Ferias(f)
    
        return None
           
    def get_all_ferias(self):
        
        return [Ferias(f) for f in self.get_table_data('ferias')]
    
    def get_falta(self, falta_id):
        
        return Falta(self.get_row_by_id('faltas', falta_id))
    
    def get_all_faltas(self):
        return [Falta(f) for f in self.get_table_data('faltas')]
        
    def get_falta_with_date(self, func_id, date):
        
        f = self.multiple_select('faltas',[['func_id', '=', func_id],['data', '=', date]])
        
        if f:
            return Falta(f[0])
            
        return None
    
    def get_faltas_funcionario(self, func_id):
        faltas = self.get_all_faltas()
        return [f for f in faltas if f.func_id == func_id]

    def get_all_clientes(self):
        return [Cliente(c) for c in self.get_table_data('clientes')]
