import ast
from firebase_admin import auth as admin_auth
import firebase_admin
from datetime import datetime
import subprocess
from app.models.ferias import Ferias
import mysql.connector
from configparser import ConfigParser
from .auth import Auth

from .admin import Admin
from .gestor import Gestor
from .estagiario import Estagiario
from .funcionario import Funcionario
from .turno import Turno
from .cargo import Cargo
from .falta import Falta
from .cliente import Cliente
from .feriado import Feriado
from .servico import Servico
from .servico_entregue import ServicoEntregue
from .atributo import AtributoServico
from .pausa import Pausa
from .tag_servico import TagServico

class Database():

    def __init__(self, name):

        self.name = name

        # Configs firebase
        with open("config/firebase.cfg", "r") as f:
            firebase_config = ast.literal_eval(f.read())

        # Configs mysql
        config = ConfigParser()
        config.read('config/mysql.ini')
        self.mysql_host = config['MYSQL']['host']
        self.mysql_port = config['MYSQL']['port']
        self.mysql_user = config['MYSQL']['user']
        self.mysql_pass = config['MYSQL']['password']

        # # Initializing firebase
        # firebase = pyrebase.initialize_app(firebase_config)

        self.auth = Auth(firebase_config['apiKey'])
        
        # # Auth Module
        # self.auth = firebase.auth()

    def get_mysql_connection(self):
        return mysql.connector.connect(
            host=self.mysql_host,
            port=self.mysql_port,
            user=self.mysql_user,
            passwd=self.mysql_pass,
            database=self.name
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
            insert_id = cursor.lastrowid
        cnx.commit()
        cnx.close()
        return insert_id
    
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

            self.insert_data("Users", data)

        except Exception as e:
            print(e)
            return False

        return True

    def get_user_by_email(self, email):
        try:

            u = self.select('Users', 'email', '=', email)[0]

            if u:
                if u['role'] == 'Estagiario':
                    return Estagiario(u)

                if u['role'] == 'Funcionario':
                    return Funcionario(u)

                if u['role'] == 'Admin':
                    return Admin(u)

                if u['role'] == 'Gestor':
                    return Gestor(u)

            return None
        except Exception as e:
            return e
  
    
    def select(self, table, key, operator, value):
        cnx = self.get_mysql_connection()
        rows = None
        with cnx.cursor(dictionary=True) as cursor:
            if operator != 'IN':
                sql = "SELECT * FROM %s WHERE %s %s '%s'" % (table, key, operator, value)
            else:
                sql = "SELECT * FROM %s WHERE %s %s %s" % (table, key, operator, value)
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
        return rows if len(rows) > 0 else None

    def filtra_entradas(self,query_arr, collection):
        query = collection
        for q in query_arr:
            query = query.where(
                q[0], '==' ,q[1]
            )

        return query.stream()
    

    # Get all funcionarios from db
    def get_all_funcionarios(self):
        funcionarios = self.get_table_data('Users')
        return [Funcionario(f) for f in funcionarios if f['role'] in ['Funcionario', 'Gestor', 'Estagiario']] if funcionarios else None
    
    def get_funcionario(self, user_id):
        func = self.get_row_by_id('Users', user_id)
        
        if func:
            return Funcionario(func) if func['role'] == 'Funcionario' else Gestor(func)
        return Funcionario(func) if func and func['role'] == 'Funcionario' else None

    def get_turnos(self):
        turnos = self.select('Turnos', 'current_status', '=', 'clocked_out')
        return [Turno(t) for t in turnos] if turnos else None


    def get_turno(self, date, user_id):
        turno = self.multiple_select(
            'Turnos', operations=[['dia', '=', f"'{date}'"],['user_id', '=', user_id]]
        )

        return Turno(turno[0]) if turno else None


    # Add new shift Status to firestore
    def add_new_shitf_status(self, new_status, funcionario):

        now = datetime.now()
        
        current_date = str(now.date())
        
        current_hour = str(now.time())[:-7]
        
        turno = self.get_turno(current_date, funcionario.id)

        if turno:
            current_status = turno.current_status
            if new_status == 'pausa':
                self.update_data('Turnos', turno.id,
                    {
                        'current_status' : 'pausado'
                    }
                )

                pausa = Pausa({'inicio' : current_hour, 'turno' : turno.id})
                self.insert_data('Pausas', pausa.to_json())

            if new_status == 'retorno':

                pausa = Pausa(self.select('Pausas', 'turno', '=', turno.id)[-1])
                pausa.fim = current_hour
                self.update_data('Pausas', pausa.id, pausa.to_json())
                
                tempo_total = self.get_pausa(pausa.id).get_tempo()
                self.update_data('Turnos', turno.id,
                    {
                        'current_status' : 'clocked_in',
                        'pausa' : tempo_total.seconds + turno.pausa
                    }
                )


            if new_status == 'clock_out' and current_status == 'clocked_in':

                self.update_data('Turnos', turno.id, 
                    {
                        'current_status': 'clocked_out',
                        'hora_saida' : current_hour
                    }
                )
                
            if new_status == 'break_in' and current_status == 'clocked_in':
                self.update_data('Turnos', turno.id, 
                    {
                    'current_status': new_status,
                    'inicio_almoco' : current_hour,
                    'almocou' : 1
                    }
                )
            if new_status == 'break_out' and current_status == 'break_in':
                self.update_data('Turnos', turno.id, 
                    {
                    'current_status': 'clocked_in', 
                    'fim_almoco' : current_hour
                    }
                )
            
        else:
            if new_status == 'clock_in':
                        
                data = {
                    'current_status' : 'clocked_in',
                    'dia' : current_date,
                    'hora_entrada' : current_hour,
                    'user_id' : funcionario.id,
                    'turno_funcionario' : funcionario.turno,
                    'almocou' : False,
                    'pausa' : 0
                }
                
                self.insert_data('Turnos', data)
                
        return True
        
    def get_cargo(self, cargo_id):
        c = self.get_row_by_id('Cargos', cargo_id)
        if c:
            return Cargo(c)
        return None   
    
    def get_cargos(self):
        cargos = self.get_table_data('Cargos')

        return [Cargo(c) for c in cargos] if cargos else None

    def get_feriado(self, id):
        feriado = self.get_row_by_id('Feriados', id)
        return Feriado(feriado) if feriado else None
        
    def get_feriados(self):        
        feriados = self.get_table_data('Feriados')
            
        return [Feriado(f) for f in feriados] if feriados else None    
            
    def create_ferias(self, data):
        self.insert_data('Ferias', Ferias(data).to_json())
        
    def get_ferias(self, ferias_id):
        f = self.get_row_by_id('Ferias', ferias_id)
        return Ferias(f) if f else None
           
    def get_all_ferias(self):
        ferias = self.get_table_data('Ferias')
        return [Ferias(f) for f in ferias] if ferias else None
    
    def get_falta(self, falta_id):
        falta = self.get_row_by_id('Faltas', falta_id)
        return Falta(falta) if falta else None
    
    def get_all_faltas(self):
        faltas = self.get_table_data('Faltas')  
        
        return [Falta(f) for f in faltas] if faltas else None
        
    def get_falta_with_date(self, user_id, date):
        
        f = self.multiple_select('Faltas',[['user_id', '=', user_id],['data', '=', f"'{date}'"]])

        return Falta(f[0]) if f else None

    
    def get_faltas_funcionario(self, user_id):
        faltas = self.select('Faltas', 'user_id', '=', user_id)

        return [Falta(f) for f in faltas] if faltas else None

    def get_all_clientes(self):
        clientes = self.get_table_data('Clientes')
        return [Cliente(c) for c in clientes] if clientes else None

    def get_servicos_by_funcionario(self, user_id):
        servicos = self.select('ServicosEntregues', 'user_id', '=', user_id)
        return [ServicoEntregue(satb) for satb in servicos] if servicos else None

    def get_servicos_by_funcionario_and_daterange(self, user_id, date_inicio, date_fim):
        servicos = self.multiple_select('ServicosEntregues',[['user_id', '=', user_id],
                                                    ['entrega', '>=', f"'{date_inicio}'"], 
                                                    ['entrega', '<=', f"'{date_fim}'"]])
        return [ServicoEntregue(satb) for satb in servicos] if servicos else None

    def insert_push_endpoint(self, data, user):
        insertion_data = {
            'user' : user,
            'subscription_json' : data
        }

        push_entry = self.select('Pushs', 'subscription_json', '=', data)[0]
        
        if push_entry:
            return self.update_data('Pushs', push_entry['id'], insertion_data)

        return self.insert_data('Pushs', insertion_data)

    def get_push(self, user_id):
        pushs = self.select('Pushs', 'user', '=', user_id)
        return pushs[0] if pushs else None

    def get_pushs(self):
        return self.get_table_data('Pushs')

    def get_servico(self, serv_id):
        serv = self.select('Servicos', 'id', '=', serv_id)
        return Servico(serv[0]) if serv else None

    def get_servicos(self):
        servs = self.get_table_data('Servicos')
        return [Servico(s) for s in servs] if servs else None

    def get_tag(self, id):
        tag = TagServico(self.get_row_by_id('TagServicos', id))
        tag.set_servicos(self.get_servicos_by_tag(id))
        return tag

    def get_tags(self):
        tags = [TagServico(t) for t in self.get_table_data('TagServicos')] if self.get_table_data('TagServicos') else None
        if tags:
            for tag in tags:
                tag.set_servicos(self.get_servicos_by_tag(tag.id))

        return tags

    def get_servicos_by_tag(self, id):
        servicos_map = self.select('TagServicos_Maps', 'tag', '=', id)
        servs = []

        if servicos_map:
            for serv in servicos_map:
                servs.append(self.get_servico(serv['servico']))
        
        return servs

    def get_servico_entregue(self, at_id):
        serv_atb = self.select('ServicosEntregues', 'id', '=', at_id)

        return ServicoEntregue(serv_atb[0]) if serv_atb else None

    def get_servicos_atribuidos(self):
        svs_atb = self.get_table_data('ServicosEntregues')

        return [ServicoEntregue(s_ent) for s_ent in svs_atb] if svs_atb else None

    def get_servicos_atribuidos_funcionario(self, user_id):
        return [ServicoEntregue(s_ent) for s_ent in self.select('ServicosEntregues', 'user_id', '=', user_id)]

    def get_clientes(self):

        return self.get_table_data('Clientes')

    def get_atributo(self, atb_id):
        atb = self.select('AtributosServicos', 'id', '=', atb_id)
        return AtributoServico(atb[0]) if atb else None

    def get_atributo_from_serv(self, serv_atribuido):
        value = self.select('AtributosValues', 'servico_entregue', '=', serv_atribuido)

        if value:
            value = value[0]
            atributo = self.get_atributo(value['atributo'])
            atributo.set_value(value['value'])
            return atributo

        return None

    def get_pausa(self, pausa_id):
        pausa = self.select('Pausas', 'id', '=', pausa_id)
        return Pausa(pausa[0]) if pausa else None

    def get_pausas_turno(self, turno_id):
        pausas = self.select('Pausas', 'turno', '=', turno_id)
        return [Pausa(p) for p in pausas] if pausas else None
