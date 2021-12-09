from re import S
from workalendar.america.brazil import BrazilDistritoFederal
from . import *

def render_painel_func(funcionario, start_date, end_date):

    start_date = get_start_date(start_date, funcionario.get_datetime_inicio_trabalho())
    horas_totais_mes = horas_totais(start_date, end_date, funcionario=funcionario)
        
    horas_trabalhadas = get_total_time(funcionario=funcionario)
    
    dias_uteis = dias_uteis_timedelta(start_date, end_date)
    
    percentage = get_percentage_work(horas_trabalhadas, horas_totais_mes)
    
    
    if horas_trabalhadas > horas_totais_mes:
        horas_extras = horas_trabalhadas - horas_totais_mes
        horas_trabalhadas = horas_trabalhadas - horas_extras
        horas_extras_maximas = dias_uteis * 2
        percentage_extras = get_percentage_work(horas_extras, horas_extras_maximas)
        horas_devendo = 0
    else:
        horas_devendo = horas_totais_mes - horas_trabalhadas
        horas_extras = 0
        percentage_extras = 0
        
    month_work = get_total_work(funcionario=funcionario)

    assiduidade, faltas =  calcula_assiduidade(funcionario, start_date, end_date) 
    assiduidade = '%.1f' % assiduidade
    
    start_date_html = f"{'%.2d' % start_date.day}/{'%.2d' % start_date.month}/{start_date.year}"
    end_date_html = f"{'%.2d' % end_date.day}/{'%.2d' % end_date.month}/{end_date.year}"

    media_horas =  (timedelta(seconds=(( (horas_trabalhadas + horas_extras) * 3600
                             ) / dias_uteis )) if dias_uteis > 0 else timedelta(seconds=0))
    
    media_horas = '0' + str(media_horas)[:4]
    
    dias_trabalhados = dias_uteis - faltas

    return render_template('painel-func.html', user=funcionario, painel_active='active',
                                            percentage=percentage,
                                            percentage_extras=percentage_extras,
                                            horas_mes=horas_trabalhadas,
                                            horas_extras=horas_extras,
                                            horas_totais=horas_trabalhadas + horas_extras,
                                            month_work=month_work,
                                            assiduidade=assiduidade,
                                            faltas=faltas,
                                            start_date=start_date_html,
                                            end_date=end_date_html,
                                            media_horas=media_horas,
                                            dias_trabalhados=dias_trabalhados,
                                            horas_devendo=horas_devendo)

    
def render_filtered_painel_admin(user, start_date, end_date, func_id):
    funcionario = db.get_funcionario(func_id)
    start_date = get_start_date(start_date, funcionario.get_datetime_inicio_trabalho())
    
    dias_uteis = dias_uteis_timedelta(start_date, end_date)
    horas_totais = dias_uteis * funcionario.turno
    
    turnos = db.get_turnos_timedelta(funcionario.id, start_date, end_date)
    funcionario.set_turnos(turnos)
    
    horas_trabalhadas = get_total_time(funcionario=funcionario)
    
    percentage = get_percentage_work(horas_trabalhadas, horas_totais)
    
    horas_extras_maximas = dias_uteis * 2
    
    
    if horas_trabalhadas > horas_totais:
        horas_extras = horas_trabalhadas - horas_totais
        horas_trabalhadas = horas_trabalhadas - horas_extras
        percentage_extras = get_percentage_work(horas_extras, horas_extras_maximas)
        horas_devendo = 0
        
    else:
        horas_devendo = horas_totais - horas_trabalhadas
        horas_extras = 0
        percentage_extras = 0
        
    assiduidade, faltas =  calcula_assiduidade(funcionario, start_date, end_date) 
    assiduidade = '%.1f' % assiduidade
    
    start_date_html = f"{'%.2d' % start_date.day}/{'%.2d' % start_date.month}/{start_date.year}"
    end_date_html = f"{'%.2d' % end_date.day}/{'%.2d' % end_date.month}/{end_date.year}"

    media_horas =  (timedelta(seconds=(( (horas_trabalhadas + horas_extras) * 3600
                             ) / dias_uteis )) if dias_uteis > 0 else timedelta(seconds=0))
    
    media_horas = '0' + str(media_horas)[:4]
    
    dias_trabalhados = dias_uteis - faltas

    return render_template('painel-admin.html', user=user, painel_active='active',
                                            percentage=percentage,
                                            percentage_extras=percentage_extras,
                                            horas_mes=horas_trabalhadas,
                                            horas_extras=horas_extras,
                                            horas_totais=horas_trabalhadas + horas_extras,
                                            funcionarios=db.get_all_funcionarios(),
                                            assiduidade=assiduidade,
                                            faltas=faltas,
                                            start_date=start_date_html,
                                            end_date=end_date_html,
                                            media_horas=media_horas,
                                            dias_trabalhados=dias_trabalhados,
                                            horas_devendo=horas_devendo)
    
    
def render_painel_admin(user, start_date, end_date):
    
    funcionarios = get_funcs(start_date, end_date)
    if funcionarios:
        horas_totais_mes = horas_totais(start_date, end_date, funcionarios=funcionarios)

        horas_trabalhadas = get_total_time(funcionarios=funcionarios)

        percentage = get_percentage_work(horas_trabalhadas, horas_totais_mes)
        
        if horas_trabalhadas > horas_totais_mes:
            horas_extras = horas_trabalhadas - horas_totais_mes
            horas_extras_maximas = 40
            
            percentage_extras = get_percentage_work(horas_extras, horas_extras_maximas)
        else:
            horas_extras = 0
            percentage_extras = 0
            
        
        month_work = get_total_work(funcionarios)

        start_date_html = f"{'%.2d' % start_date.day}/{'%.2d' % start_date.month}/{start_date.year}"
        end_date_html = f"{'%.2d' % end_date.day}/{'%.2d' % end_date.month}/{end_date.year}"

        return render_template('painel-admin.html', user=user, painel_active='active',
                                                percentage=percentage,
                                                percentage_extras=percentage_extras,
                                                horas_mes=horas_trabalhadas,
                                                horas_extras=horas_extras,
                                                horas_totais=horas_trabalhadas + horas_extras,
                                                month_work=month_work,
                                                funcionarios=db.get_all_funcionarios(),
                                                start_date=start_date_html,
                                                end_date=end_date_html)
    else:
        return redirect(url_for('login.registrar'))
    
def get_funcs(start_date, end_date):
    
    funcionarios = db.get_all_funcionarios()
    
    for f in funcionarios:
        current_start_date = get_start_date(start_date, f.get_datetime_inicio_trabalho())
        turnos = db.get_turnos_timedelta(f.id, current_start_date, end_date)
        f.set_turnos(turnos)
        
    return funcionarios

def get_month(month):
    month = int(month)
    months = [
        'Janeiro','Fevereiro','Março','Abril',
        'Maio','Junho','Julho','Agosto',
        'Setembro','Outubro','Novembro','Dezembro'
    ]
    
    return months[month - 1]

def horas_totais(start_date, end_date, funcionario=None, funcionarios=None):
    
    
    hrs_totais = 0
    
    if funcionarios:
        for f in funcionarios:
            current_start_date = get_start_date(start_date, f.get_datetime_inicio_trabalho())
            dias_uteis = dias_uteis_timedelta(current_start_date, end_date)
            turno = f.turno
            coeficient = f.dias_trabalho / 5
                
            hrs_totais += turno * dias_uteis * coeficient
    else:
        current_start_date = get_start_date(start_date, funcionario.get_datetime_inicio_trabalho())
        dias_uteis = dias_uteis_timedelta(current_start_date, end_date)
        turno = funcionario.turno
        coeficiente = funcionario.dias_trabalho / 5
        
        hrs_totais += turno * dias_uteis * coeficiente
    
    return int(hrs_totais)

def dias_uteis_timedelta(start_date, end_date):
    cal = BrazilDistritoFederal()
    dias_totais = 0
    feriados = db.get_feriados()

    for i in range( (end_date - start_date).days + 1 ):
        dt = start_date + timedelta(days=i)
        dt_string = f"{'%.2d' % dt.day}/{'%.2d' % dt.month}/{dt.year}"

        if cal.is_working_day(dt) and not dt_string in feriados:
            dias_totais += 1
            
    return dias_totais

def get_total_time(funcionarios=None, funcionario=None):
    total_time = 0
    
    if funcionarios:
        for f in funcionarios:
            for t in f.turnos:
                tturno = t._horas_totais
                
                total_time += timedelta(hours=tturno.hour, minutes=tturno.minute, seconds=tturno.second).seconds
                
    else:  
        for t in funcionario.turnos:
            tturno = t._horas_totais
            total_time += timedelta(hours=tturno.hour, minutes=tturno.minute, seconds=tturno.second).seconds
            

    return total_time // 3600


def get_total_work(funcionarios=None, funcionario=None):
    month = str(datetime.now().month)
    
    month_work = dict()
    
    if funcionarios:
        for f in funcionarios:
            total_time = timedelta(seconds = 0)
            for t in f.turnos:
                if t.dia[3:5] == month:
                    ttotal = t._horas_totais
                    total_time += timedelta(hours=ttotal.hour, minutes=ttotal.minute, seconds=ttotal.second)
                
            month_work[f.name] = str(total_time.seconds // 3600)    
            
    else:
        total_time = timedelta(seconds = 0)
        for t in funcionario.turnos:
            if t.dia[3:5] == month:
                ttotal = t._horas_totais
                total_time += timedelta(hours=ttotal.hour, minutes=ttotal.minute, seconds=ttotal.second)
            
        month_work[funcionario.name] = str(total_time.seconds // 3600)  
        
    return month_work    


def filtra_funcionarios(funcionarios, filter):
    tns_flt = list()
    for x in funcionarios:
        if filter(x):
            tns_flt.append(x)

    return tns_flt

def get_start_date(start_date, inicio_trabalho):
    return (start_date if start_date > inicio_trabalho
                              else inicio_trabalho)
    
def get_percentage_work(horas_trabalhadas, horas_totais):
    return ('%.1f' % ((horas_trabalhadas * 100) / horas_totais)
                  if horas_trabalhadas < horas_totais and horas_totais > 0
                  else 100)
    
def calcula_assiduidade(funcionario, start_date, end_date):
    if not 'turnos' in vars(funcionario):
        return 0
      
    cal = BrazilDistritoFederal()
    trabalhou = 0
    faltas = 0
    current_start_date = get_start_date(start_date, funcionario.get_datetime_inicio_trabalho())
    dias_uteis = dias_uteis_timedelta(current_start_date, end_date)
    
    feriados = db.get_feriados()
    ferias_user = db.get_ferias_user(funcionario.id)
    
    for i in range( (end_date - current_start_date).days + 1 ):
    
        c_date = current_start_date + timedelta(days=i)

        date_string = f"{'%.2d' % c_date.day}/{'%.2d' % c_date.month}/{c_date.year}"
        if cal.is_working_day(c_date) and date_string not in feriados:
            if ferias_user:
                for f in ferias_user:
                    if f.is_working_day(c_date.timestamp()):
                        if funcionario.worked_this_date(c_date):
                            trabalhou += 1
                        else:
                            faltas += 1
            else:
                if funcionario.worked_this_date(c_date):
                    trabalhou += 1
                    
                else:
                    faltas += 1

    return ((trabalhou * 100 / dias_uteis)
            if dias_uteis > 0
            else 100
            ), faltas
