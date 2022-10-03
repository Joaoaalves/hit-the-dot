from . import db, datetime, timedelta, time, session


def converter_str_int(dt):
        hr = datetime.strptime(dt,'%H:%M:%S')

        return int(timedelta(hours=hr.hour,minutes=hr.minute,seconds=hr.second).total_seconds())

def editar_funcionario(form, user):
        data = session['user']

        if 'name' in form:
                data['name'] = form['name']
                
        if 'email' in form:
                data['email'] = form['email']

        db.update_data(' users', user.id, user.to_json())

        session['user'] = data

        session.modified = True