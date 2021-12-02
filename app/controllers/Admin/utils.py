from datetime import timedelta
from mimetypes import init
from workalendar.america.brazil import BrazilDistritoFederal
from . import db, datetime, app, date


def get_current_date():
    now = datetime.now()
    return f"{now.day:02d}/{now.month:02d}/{now.year:04d}"

def filtra_funcionarios(funcionarios, filter):
    tns_flt = list()
    for x in funcionarios:
        if filter(x):
            tns_flt.append(x)

    return tns_flt
    
def update_func_info(form, funcionario):
    print(form)
    funcionario.name = form['nome']
    funcionario.turno = int(form['turno'])
    funcionario.dias_trabalho = int(form['dias_trabalho'])
    funcionario.celular = form['celular']
    
    cargo_id = int(form['cargo'])

    funcionario.cargo = cargo_id
    
    db.update_info('Users', vars(funcionario), key='id', value=funcionario.id )

def get_cargos():
    
    return db.get_all_rows_from_firestore('Cargos')


def timedelta_to_hours(time):
    return time.days * 24 + time.seconds //3600


def excluir_funcionario(func_id):
    # Remove Func
    db.remove_user(func_id)
    
    # Remove Func's Turnos
    db.remove_data_from_firestore('Turnos', 'user_id', func_id)
    

    
def dias_uteis_mes():
    now = datetime.now()
    
    year = now.year
    month = now.month
    
    initial_date = date(year,month,1)
    ending_date = datetime(year, month + 1, 1) - timedelta(days=1)
    calendar = BrazilDistritoFederal()
    
    return calendar.get_working_days_delta(initial_date, ending_date, include_start=True)


#
# JINJA Utils
#

def get_cargo_nome(cargos, id):
    for cargo in cargos:
        if cargo['id'] == id:
            return cargo['nome']
        
app.jinja_env.globals.update(get_cargo_nome=get_cargo_nome)