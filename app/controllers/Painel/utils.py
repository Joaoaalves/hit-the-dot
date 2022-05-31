from . import *

def render_filtered_painel_admin(start_date, end_date, func_id):
    user = get_user_object(session['user'])
    
    funcionario = db.get_funcionario(func_id)
    
    segundos_trabalhados, faltas, assiduidade, segundos_totais, dias_uteis = get_trabalho_total_funcionario(start_date, end_date, funcionario)

    media_horas =  get_media_horas(segundos_trabalhados, dias_uteis)

    horas_extras, percentage_extras, segundos_trabalhados = get_horas_extras(segundos_trabalhados, segundos_totais)

    percentage = get_percentage_work(segundos_trabalhados, segundos_totais)
    horas_trabalhadas = segundos_trabalhados // 3600
    
    start_date_html = start_date.strftime('%d-%m-%Y')
    end_date_html = end_date.strftime('%d-%m-%Y')

    horas_devendo = get_horas_devendo(segundos_trabalhados, segundos_totais)
    
    dias_trabalhados = dias_uteis - faltas    

    demandas, demanda_dict, demandas_pendentes = get_demandas(start_date, end_date, func_id)

    demandas_diarias, demandas_semanas, demandas_totais = get_relatorio(start_date, end_date, func_id)

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
                                            horas_devendo=horas_devendo,
                                            demandas=demandas,
                                            demanda_dict=demanda_dict,
                                            demandas_pendentes=demandas_pendentes,
                                            demandas_diarias=demandas_diarias,
                                            demandas_semanas=demandas_semanas,
                                            demandas_totais=demandas_totais)


def render_painel_admin(user, start_date, end_date):

    segundos_trabalhados, segundos_totais, dias_totais = get_trabalho_total(start_date, end_date)


    horas_extras, percentage_extras, segundos_trabalhados = get_horas_extras(segundos_trabalhados, segundos_totais)
    percentage = get_percentage_work(segundos_trabalhados, segundos_totais)

    horas_trabalhadas = segundos_trabalhados // 3600
    horas_totais_mes = segundos_totais // 3600

    start_date_html = start_date.strftime('%d-%m-%Y')
    end_date_html = end_date.strftime('%d-%m-%Y')
    demandas, demanda_dict, demandas_pendentes = get_demandas(start_date, end_date)

    return render_template('painel-admin.html', user=user, painel_active='active',
                                            percentage=percentage,
                                            percentage_extras=percentage_extras,
                                            horas_mes=min(horas_trabalhadas, horas_totais_mes),
                                            horas_extras=horas_extras,
                                            horas_totais=horas_trabalhadas + horas_extras,
                                            funcionarios=db.get_all_funcionarios(),
                                            start_date=start_date_html,
                                            end_date=end_date_html,
                                            demandas=demandas,
                                            demanda_dict=demanda_dict,
                                            demandas_pendentes=demandas_pendentes)

def render_painel_func(funcionario, start_date, end_date):
    segundos_trabalhados, faltas, assiduidade, segundos_totais, dias_totais = get_trabalho_total_funcionario(start_date, end_date, funcionario)

    media_horas = get_media_horas(segundos_trabalhados, dias_totais)
    dias_trabalhados = dias_totais - faltas
    
    horas_extras, percentage_extras, segundos_trabalhados = get_horas_extras(segundos_trabalhados, segundos_totais)
        
    horas_devendo = get_horas_devendo(segundos_trabalhados, segundos_totais)
    percentage = get_percentage_work(segundos_trabalhados, segundos_totais)

    horas_trabalhadas = segundos_trabalhados // 3600

    start_date_html = start_date.strftime('%d-%m-%Y')
    end_date_html = end_date.strftime('%d-%m-%Y')

    demandas, demanda_dict, demandas_pendentes = get_demandas(start_date, end_date, funcionario.id)
    
    return render_template('painel-func.html', user=funcionario, painel_active='active',
                                            percentage=percentage,
                                            percentage_extras=percentage_extras,
                                            horas_mes=horas_trabalhadas,
                                            horas_extras=horas_extras,
                                            horas_totais=horas_trabalhadas + horas_extras,
                                            assiduidade=assiduidade,
                                            faltas=faltas,
                                            start_date=start_date_html,
                                            end_date=end_date_html,
                                            media_horas=media_horas,
                                            dias_trabalhados=dias_trabalhados,
                                            horas_devendo=horas_devendo,
                                            demandas=demandas,
                                            demanda_dict=demanda_dict,
                                            demandas_pendentes=demandas_pendentes)


def get_percentage_work(segundos_trabalhados, segundos_totais):
    return '%.1f' %( (segundos_trabalhados / segundos_totais) * 100) if segundos_totais > 0 else '100'


def get_media_horas(segundos_trabalhados, dias_uteis):
    media_segundos = (( segundos_trabalhados/ dias_uteis )
                    if dias_uteis > 0 else 0)

    hours = media_segundos // 3600
    minutes = (media_segundos % 3600) // 60
    return f"{'%.2d' % hours}:{'%.2d' % minutes}"


def get_horas_extras(segundos_trabalhados, segundos_totais):
    if segundos_totais < segundos_trabalhados:
        percentage_extras = get_percentage_work(segundos_trabalhados - segundos_totais, segundos_trabalhados)
        horas_extras = (segundos_trabalhados - segundos_totais) // 3600
        segundos_trabalhados = segundos_totais
    else:
        percentage_extras = 0
        horas_extras = 0
        
    return horas_extras, percentage_extras, segundos_trabalhados


def get_trabalho_total(start_date, end_date):
    segundos_trabalhados = 0
    dias_totais = 0
    tempo_total = 0

    funcionarios = db.get_all_funcionarios()
    for funcionario in funcionarios:
        (segundos_trabalhados_funcionario, 
            faltas, assiduidade, 
            tempo_total_funcionario, 
            dias_totais_funcionario
        ) = get_trabalho_total_funcionario(start_date, end_date, funcionario)

        segundos_trabalhados += segundos_trabalhados_funcionario
        dias_totais += dias_totais_funcionario
        tempo_total += tempo_total_funcionario
    
    return segundos_trabalhados, tempo_total, dias_totais


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


def get_horas_devendo(segundos_trabalhados, segundos_totais):
    horas_totais = (segundos_totais - segundos_trabalhados) // 3600
    minutos_totais = ((segundos_totais - segundos_trabalhados) % 3600) // 60

    return f"{'%.2d' % horas_totais}:{'%.2d' % minutos_totais}"


def get_start_end_date(args):
    try:
        s_date, e_date = args.get('range').split(' - ')
        start_date_datetime = datetime.strptime(s_date, '%d/%m/%Y')
        end_date_datetime = datetime.strptime(e_date, '%d/%m/%Y')
        
        if start_date_datetime > end_date_datetime:
            raise Exception('Date Range inválido')
        
    except Exception as e:
        now = datetime.now()
        if now.day == 1:
            start_date_datetime = now
            end_date_datetime = now
        else:
            start_date_datetime = datetime(year=now.year, month=now.month, day=1)
            end_date_datetime = datetime(year=now.year, month=now.month, day=now.day - 1)

    return start_date_datetime, end_date_datetime


def get_demandas(start_date, end_date, func_id=None):


    demanda_dict = { 'Segunda': 0, 'Terça': 0, 'Quarta': 0, 'Quinta': 0, 'Sexta': 0 }
    week_days = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta']
    
    demandas_veririficadas = list()
    demandas_pendentes = list()
    demandas = list()
    if func_id:
        demandas = db.get_demandas_by_funcionario_and_daterange(func_id, start_date, end_date)
        if not demandas:
            return [], demanda_dict, []
            
    else:
        funcionarios = db.get_all_funcionarios()
        for f in funcionarios:
            ds = db.get_demandas_by_funcionario_and_daterange(f.id, start_date, end_date)
            if ds:
                demandas += ds

    for demanda in demandas:
        if demanda.status == 'Verificada':
            with suppress(TypeError):
                week_day = week_days[demanda.date.weekday()] if demanda.date.weekday() < 5 else 'Sexta'
                demanda_dict[week_day] += 1
                demandas_veririficadas.append(demanda)
        else:
            demandas_pendentes.append(demanda)

    return demandas_veririficadas, demanda_dict, demandas_pendentes

def get_relatorio(start_date, end_date, func):
    demandas_diarias = dict() 
    demandas_semanas = dict()
    calendario = calendar.monthcalendar(start_date.year, start_date.month)
    month = start_date.month
    year = start_date.year
    total = 0
    dias_semana = ['Segunda Feira', 'Terça Feira', 'Quarta Feira', 'Quinta Feira', 'Sexta-feira']
    for week in calendario:
        if week[0] != 0:
            inicio = f"{'%.2d' % week[0]}/{'%.2d' % month}/{year}"

        else:
            inicio = f"01/{'%.2d' % month}/{year}"

        if week[6] == 0:
            fim = f"{end_date.day}/{'%.2d' % month}/{year}"

        else:
            fim = f"{week[6]}/{'%.2d' % month}/{year}"
        inicio_dt = datetime.strptime(inicio, '%d/%m/%Y')
        fim_dt = datetime.strptime(fim, '%d/%m/%Y')

        dem = db.get_demandas_by_funcionario_and_daterange(func, inicio_dt, fim_dt)

        qtd_sem = len(dem) if dem else 0
        demandas_semanas[f"{inicio} - {fim}"] = qtd_sem 
        total += qtd_sem
        for day in week:
            if  day > 0:
                dia = f"{'%.2d' % day}/{'%.2d' % month}/{year}"
                dt = datetime.strptime(dia, '%d/%m/%Y').date()
                qtd = 0
                if dt.weekday() < 5:
                    if dem:
                        for d in dem:
                            if d.date == dt:
                                qtd += 1

                    demandas_diarias[f"{dia} ({dias_semana[dt.weekday()]})"] = qtd

    return demandas_diarias, demandas_semanas, total