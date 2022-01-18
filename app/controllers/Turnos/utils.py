from datetime import timedelta
from . import db, Turno, Funcionario

def get_turnos():
    turnos = list()

    list_turnos = db.get_all_rows_from_firestore('Turnos')
    
    if list_turnos:
        for t in list_turnos:
            if t['current_status'] == 'clocked_out':
                turnos.append(Turno(t))

        return turnos

    return None


def get_turno(date, user_id):

    turno = db.get_turno(date, user_id)
    if turno:
        return Turno(turno)

    return None

def get_funcionarios():
    
    fs = db.get_rows_from_firestore('Users', 'role', '==', 'Funcionario')
    if not fs:
        return None, None
    
    funcionarios = list()
    dict_func_ids = dict()

    for f in fs:
        func = Funcionario(f)
        funcionarios.append(func)
        dict_func_ids[func.id] = [func.name, func.turno]
        
    return funcionarios, dict_func_ids


def filtra_turnos(turnos, filter):
    tns_flt = list()
    for x in turnos:
        if filter(x):
            tns_flt.append(x)

    return tns_flt

def update_turno(form, date, user_id):
    data = dict(form)
    # data['report'] = form.getlist('report')
    print(data)
    dt = form['dia']
    dt = f'{dt[-2:]}/{dt[5:7]}/{dt[:4]}'  
    
    data['dia'] = dt
    
    data['user_id'] = user_id
    data['current_status'] = 'clocked_out'
    updated_turno = Turno(data)
    
    
    query = db.firestore.collection('Turnos').where(
        'user_id', '==', user_id).where(
        'dia', '==', date
    ).stream()
    for s in query:
        doc_id = s.id
    db.firestore.collection('Turnos').document(document_id=doc_id).update(updated_turno.to_json())
    
def get_work(turno, funcionario):
    horas_trabalhadas = turno.get_total_time_str()
    
    trabalho = datetime_seconds(turno.converter_str_datetime(horas_trabalhadas))

    turno_total = funcionario.turno * 3600
    
    percentage = ('%.1f' % ((trabalho * 100) / turno_total) 
                  if trabalho < turno_total and turno_total > 0
                  else 100)
    
    horas_extras_totais = 2 * 3600
    if trabalho > funcionario.turno * 3600:
        
        trabalho_extra = trabalho - (funcionario.turno * 3600)
        trabalho = trabalho - trabalho_extra
        percentage_extras = ('%.1f' % ((trabalho_extra * 100) / horas_extras_totais)
                            if trabalho_extra < horas_extras_totais
                            else 100)
    else:
        percentage_extras = 0
        trabalho_extra = 0
    return percentage, trabalho, percentage_extras, trabalho_extra

def datetime_seconds(dt):
    return timedelta(hours=dt.hour, minutes=dt.minute, seconds=dt.second).seconds

