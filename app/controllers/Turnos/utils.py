from . import db, Turno, Funcionario, datetime, BrazilDistritoFederal, rrule, DAILY

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
    
    funcionarios = db.get_all_funcionarios()
    if not funcionarios:
        return None, None
    
    dict_func_ids = dict()

    for func in funcionarios:
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

def get_trabalho_total_funcionario(start_date, end_date, funcionario):
    
    segundos_trabalhados = 0
    faltas = 0
    dias_totais = 0
    tempo_total = 0
    len_turno = 0

    cal = BrazilDistritoFederal()
    for dia in rrule(DAILY, dtstart=start_date, until=end_date):
        if cal.is_working_day(dia):
            turno = db.get_turno(dia.date(), funcionario.id)

            if turno and turno.current_status == 'clocked_out':
                len_turno = turno.turno_funcionario

                turno.set_tempo_total()
                segundos_trabalhados += turno._segundos_totais

            else:
                falta = db.get_falta_with_date(funcionario.id, dia.date())
                if falta and not falta.is_abonada():
                    faltas += 1
        
            if turno or falta:
                dias_totais += 1
                tempo_total += len_turno * 3600
    
    assiduidade = ( round((dias_totais - faltas) * 100/ dias_totais, 1)
                    if faltas > 0 
                    else 100)
    
    return segundos_trabalhados, faltas, assiduidade, tempo_total, dias_totais