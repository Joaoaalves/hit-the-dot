from datetime import datetime
from . import db, Ferias

def html_date_to_timestamp(html_date, hour):
    return datetime.strptime(html_date + hour, '%Y-%m-%d%H:%M:%S').timestamp()

def editar_ferias(form, ferias_id):
    inicio, fim = form['daterange'].split(' - ')

    ferias = Ferias({
        'id' : ferias_id,
        'inicio': datetime.strptime(inicio, '%d/%m/%Y'),
        'fim': datetime.strptime(fim, '%d/%m/%Y'),
    })

    db.update_data('Ferias', ferias.id, ferias.to_json())