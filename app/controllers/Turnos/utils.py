from . import db, Turno, Funcionario, datetime

def get_sorted_turnos(funcionario=None):

    turnos = db.get_turnos()

    if funcionario:
        turnos_funcionario = list()
        for t in turnos:
            if t.user_id == funcionario:
                turnos_funcionario.append(t)
                
        return sorted(turnos_funcionario, key=lambda x: x.dia, reverse=True)

    return sorted(turnos, key=lambda x: x.dia, reverse=True)

def get_funcionarios():
    
    fs = db.select('users', 'role', '=', 'funcionario')
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

def update_turno(form, user_id, turno):
    data = dict(form)
    if 'inicio_almoco' in data:
        data['almocou'] = True
    data['dia'] = datetime.strptime(data['dia'], '%Y-%m-%d').strftime('%d/%m/%Y')
    data['user_id'] = user_id
    data['current_status'] = 'clocked_out'
    data['turno_funcionario'] = turno.turno_funcionario
    
    updated_turno = Turno(data)
    
    db.update_data('turnos', turno.id, updated_turno.to_json())
    
def get_work(turno):
    
    turno.set_tempo_total()

    trabalho = turno._segundos_totais
    turno_total = turno.turno_funcionario * 3600
    
    percentage = (round((trabalho * 100) / turno_total, 1)
                  if trabalho < turno_total and turno_total > 0
                  else 100)
    
    horas_extras_totais = 2 * 3600

    if trabalho > turno_total:
        
        trabalho_extra = trabalho - (turno_total)
        trabalho = trabalho - trabalho_extra
        percentage_extras = (round((trabalho_extra * 100) / horas_extras_totais, 1)
                            if trabalho_extra < horas_extras_totais
                            else 100)
    else:
        percentage_extras = 0
        trabalho_extra = 0

    return percentage, trabalho, percentage_extras, trabalho_extra