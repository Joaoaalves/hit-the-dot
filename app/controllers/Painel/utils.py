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

    segundos_trabalhados, segundos_totais, dias_totais = get_trabalho_total(start_date, end_date)

    percentage = get_percentage_work(segundos_trabalhados, segundos_totais)

    horas_extras, percentage_extras, segundos_trabalhados = get_horas_extras(segundos_trabalhados, segundos_totais)

    horas_trabalhadas = segundos_trabalhados // 3600
    horas_totais_mes = segundos_totais // 3600

    start_date_html = start_date.strftime('%d-%m-%Y')
    end_date_html = end_date.strftime('%d-%m-%Y')

    return render_template('painel-admin.html', user=user, painel_active='active',
                                            percentage=percentage,
                                            percentage_extras=percentage_extras,
                                            horas_mes=min(horas_trabalhadas, horas_totais_mes),
                                            horas_extras=horas_extras,
                                            horas_totais=horas_trabalhadas,
                                            funcionarios=db.get_all_funcionarios(),
                                            start_date=start_date_html,
                                            end_date=end_date_html)

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
                                            horas_devendo=horas_devendo)


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
            date_string = dia.strftime('%d/%m/%Y')
            turno = db.get_turno(date_string, funcionario.id)

            if turno and turno.current_status == 'clocked_out':
                len_turno = turno.turno_funcionario

                turno.set_tempo_total()
                segundos_trabalhados += turno._segundos_totais

            else:
                falta = db.get_falta_with_date(funcionario.id, date_string)
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
        start_date_datetime = datetime(year=now.year, month=now.month, day=1)
        end_date_datetime = datetime(year=now.year, month=now.month, day=now.day - 1)

    return start_date_datetime, end_date_datetime