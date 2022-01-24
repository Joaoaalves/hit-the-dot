import ast
import pyrebase
from google.cloud import firestore
from firebase_admin import auth as admin_auth
import firebase_admin
from datetime import date, datetime, timedelta
import os
import subprocess
from app.models.ferias import Ferias
import random

from app.models.relatorio import Relatorio

from .admin import Admin
from .funcionario import Funcionario
from .turno import Turno
from .cargo import Cargo
from .relatorio import Relatorio
from .tipo_tarefa import TipoTarefa
from .tarefa import Tarefa
from .pontuacao import Pontuacao
from .falta import Falta
from .cliente import Cliente

class Database():

    def __init__(self):
        self.__firebase_api_key = os.environ.get('FIREBASE_API_KEY')

        # Configs firebase
        with open("config/firebase.cfg", "r") as f:
            firebase_config = ast.literal_eval(f.read())


        # Initializing firebase
        firebase = pyrebase.initialize_app(firebase_config)
        
        # Auth Module
        self.auth = firebase.auth()

        # Database Module
        self.firestore = firestore.Client()

        # Admin Module
        firebase_admin.initialize_app()
        self.__admin_auth = admin_auth

    
    # Returns authentication with email and password
    def login(self, email, password):
        return self.auth.sign_in_with_email_and_password(email, password)

    # add new entry on Database
    def add_data_on_firestore(self, collection, info):
        self.firestore.collection(collection).document().set(info)
            
    # Remove data from Firestore       
    def remove_data_from_firestore(self, collection_name, key=None, value=None, query_arr=None):
        collection = self.firestore.collection(collection_name)
        
        if query_arr:
            stream = self.filtra_entradas(query_arr, collection)
            
        else:
            stream = collection.where(key, '==', value).stream()

            
        for doc in stream:
            doc.reference.delete()
            return True
        
        return False
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

            self.add_data_on_firestore("Users", data)

        except Exception as e:
            print(e)
            return False

        return True

    # Get user info from DB and returns as an Object
    def get_user(self, key, value):
        try:
            query = self.firestore.collection("Users").where(
                key, '==', value
            ).limit(1).stream()

            for result in query:
                u = result.to_dict()
                
                role = u['role']

                if role == 'Admin':
                    return Admin(u)

                if role == 'Funcionario':
                    return Funcionario(u)

                return None

        except Exception as e:

            return e

    # Get specific rows from Database
    def get_rows_from_firestore(self, collection, key, operator, value):

        rows = list()
        query = self.firestore.collection(collection).where(key, operator, value).stream()

        for result in query:
            rows.append(result.to_dict())

        if len(rows) > 0:
            return rows

        return None       

    # Get all rows from specific collection in db
    # if specific_column is None, all columns will be returned
    def get_all_rows_from_firestore(self, collection, specific_column=None):
        rows = list()
        try:
            query = self.firestore.collection(collection).stream()
            
            for result in query:
                u = result.to_dict()

                if specific_column:
                    rows.append(u[specific_column])
                else:
                    rows.append(u)
                
            return rows

        except Exception as e:
            print(e)
            return e

    def filtra_entradas(self,query_arr, collection):
        query = collection
        for q in query_arr:
            query = query.where(
                q[0], '==' ,q[1]
            )

        return query.stream()
    
    # Update data on db on specific collection with identifier tag
    def update_info(self, collection_name, info, key=None, value=None, query_arr=None):
        collection = self.firestore.collection(collection_name)
        
        # Multiple Filters
        if query_arr:
            stream = self.filtra_entradas(query_arr, collection)
        
        # Single Filter
        if key and value:
            stream = collection.where(
                    key, '==', value
                ).stream()
        for r in stream:
            doc = r
            self.firestore.collection(collection_name).document(doc.id).update(info)    
        
    # Remove all user's info from app
    def remove_user(self, uid):

        # Remove credentials in Auth Module
        query = self.firestore.collection("Users").where("id", "==", uid).limit(1).stream()
        for result in query:
            user = self.__admin_auth.get_user_by_email(result.to_dict()['email'])
            
            self.__admin_auth.delete_user(user.uid)

        # Remove the user's files
        subprocess.call("rm -rf app/protected/" + str(uid), shell=True)

        # Remove the user's data from firestore
        self.remove_data_from_firestore("Users", key="id", value=uid)

    # Get all funcionarios from db
    def get_all_funcionarios(self):
        funcionarios = list()

        query = self.firestore.collection('Users').where(
            'role', '==', 'Funcionario'
        ).stream()

        for f in query:
            funcionarios.append(Funcionario(f.to_dict()))

        return funcionarios
    
    def get_funcionario(self, func_id):
        
        query = self.firestore.collection('Users').where(
            'role', '==', 'Funcionario'
        ).where(
            'id', '==', func_id
        ).stream()
        
        for f in query:
            return Funcionario(f.to_dict())
        
        return None
    
    # Add new shift Status to firestore
    def add_new_shift_status_on_firestore(self, new_status, user_id):

        now = datetime.now()
        
        current_date = f"{now.day:02d}/{now.month:02d}/{now.year:04d}"
        
        current_hour = f"{now.hour:02d}:{now.minute:02d}:{now.second:02d}"
        
        turno = self.get_turno(current_date, user_id)
        
        if turno:
            current_status = turno.current_status
            
            if new_status == 'clock_in' and current_status == 'clocked_out':
                return False
            
            if new_status == 'clock_out' and current_status == 'clocked_in':
                turno.hora_saida = current_hour
                turno.current_status = 'clocked_out'
                
            if new_status == 'break_in' and current_status == 'clocked_in':
                turno.inicio_almoco = current_hour
                turno.current_status = 'break_in'
                
            if new_status == 'break_out' and current_status == 'break_in':
                turno.fim_almoco = current_hour
                turno.current_status = 'clocked_in'
                
            self.update_info('Turnos',vars(turno), query_arr=[['dia', turno.dia], ['user_id', turno.user_id]])
        else:
            if new_status == 'clock_in':
                        
                data = {
                    'current_status' : 'clocked_in',
                    'dia' : current_date,
                    'hora_entrada' : current_hour,
                    'user_id' : user_id
                }
                
                turno = Turno(data)
                
                self.add_data_on_firestore('Turnos', vars(turno))
                
        return True

    def get_turno(self, date, user_id):

        query = self.firestore.collection('Turnos').where(
            'user_id', '==', user_id
        ).where(
            'dia', '==', date
        ).limit(1).stream()

        for t in query:
            try:
                turno = Turno(t.to_dict())
                return turno
            except:
                
                return None
            
        return None
    
    def get_turnos(self, func_id):
        turnos = list()
        query = self.firestore.collection('Turnos').where(
            'user_id', '==', func_id
        ).where(
            'current_status', '==', 'clocked_out'    
        ).stream()
        
        for t in query:
            turnos.append(Turno(t.to_dict()))

        return turnos
    
    def get_turnos_timedelta(self,func_id, start_date, end_date):
        turnos = list()
        days  = (end_date - start_date).days
        date_range = [end_date - timedelta(days=x) for x in range(days + 1)]
        query = self.firestore.collection('Turnos').where(
                    'user_id', '==', func_id
            ).where(
                    'current_status', '==', 'clocked_out'
            ).stream()
        
        for result in query:
            turno = Turno(result.to_dict())
            if datetime.strptime(turno.dia, '%d/%m/%Y') in date_range:
                turnos.append(turno)

        return turnos
        
    def get_cargo(self, cargo_id):
        collection = self.firestore.collection('Cargos')

        query = collection.where('id', '==', cargo_id)
            
        for r in query.stream():
            return Cargo(r.to_dict())
        
        return None   

    def get_relatorio(self, relatorio_id):
        
        collection = self.firestore.collection('Relatorios')
        
        query = collection.where(
            'id', '==', relatorio_id
        )
        
        for r in query.stream():
            return Relatorio(r.to_dict())
        
        return None
    
    def get_relatorios(self, func_id):
        
        collection = self.firestore.collection('Relatorios')
        
        query = collection.where('func_id', '==', func_id)
        
        tarefas = list()
        
        for r in query.stream():
            tarefas.append(Relatorio(r.to_dict()))
        
        if len(tarefas) > 0:    
            return tarefas
        
        return None

    def get_tarefa(self, tarefa_id):

        stream = self.firestore.collection('Tarefas').where('id', '==', tarefa_id).stream()

        for t in stream:
            return Tarefa(t.to_dict())
        
        return None
        
    def get_all_relatorios(self, func_id=None):
        relatorios = list()
        collection = self.firestore.collection('Relatorios')
        
        
        if func_id:
            stream = collection.where('func_id', '==', func_id).stream()
            
        else:
            stream = collection.stream()
        
        for rel in stream:
            relatorio = Relatorio(rel.to_dict())
            relatorios.append(relatorio)
            
        if len(relatorios) > 0:
            return relatorios
        
        return None
    
    def get_feriados(self):
        now = datetime.now()
        current_year = str(now.year)
        
        feriados = list()
        query = self.firestore.collection('Feriados').stream()
        
        for result in query:
            f = result.to_dict()['date']

            feriados.append(f if len(f) == 10
                            else f + current_year)
            
        return feriados
        
    def get_tipos_tarefa(self):
        query = self.firestore.collection('TipoTarefa').stream()
        
        for result in query:
            f = result.to_dict()
            
    def create_ferias(self, data):
        
        ids = self.get_all_rows_from_firestore('Ferias', 'id')
        while(True):
            new_id = random.randint(1, 1000000)  
            if new_id not in ids:
                break
            
        data['id'] = new_id
        ferias = Ferias(data)
        
        self.add_data_on_firestore('Ferias', ferias.to_json())
        
    def get_ferias(self, ferias_id):
        stream = self.firestore.collection('Ferias').where(
            'id', '==', ferias_id
        ).stream()
        
        for f in stream:
            return Ferias(f.to_dict())
        
        return None
           
    def get_all_ferias(self):
        
        query = self.firestore.collection('Ferias').stream()
        all_ferias = list()
        for result in query:
            ferias = Ferias(result.to_dict())
            all_ferias.append(ferias)
            
        if len(all_ferias):
            return all_ferias
            
        return None
    
    def get_falta(self, falta_id):
        
        stream = self.firestore.collection('Faltas').where('id', '==', falta_id).stream()
        
        for f in stream:
            return Falta(
                f.to_dict()
            )
        
        return None
    
    def get_all_faltas(self):
        list_faltas = list()
        stream = self.firestore.collection('Faltas').stream()       
        
        for f in stream:
            list_faltas.append(
                Falta(f.to_dict())
            )
            
        return (list_faltas if len(list_faltas) > 0
                else None)
        
    def get_falta_with_date(self, func_id, date):
        
        stream = self.firestore.collection('Faltas').where(
            'func_id', '==', func_id
        ).where(
            'date', '==', date
        ).stream()

        for f in stream:
            return Falta(
                f.to_dict()
            )
            
        return None
    
    def get_faltas_funcionario(self, func_id):
        
        list_faltas = list()
        
        stream = self.firestore.collection('Faltas').where(
            'func_id', '==', func_id
        ).stream()
        
        for f in stream:
            list_faltas.append(
                Falta(f.to_dict())
            )
            
        return (list_faltas if len(list_faltas) > 0
                else None)

    def get_all_clientes(self):
        clientes = list()

        stream = self.firestore.collection('Clientes').stream()

        return [Cliente(c.to_dict()) for c in stream]