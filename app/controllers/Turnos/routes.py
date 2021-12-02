from app.controllers.decorators import funcionario_required
from . import *
from .utils import *

turnos_blueprint = Blueprint('turnos', __name__,
                    template_folder='templates',
                    static_folder='static',
                    static_url_path='/Turnos/static')


@turnos_blueprint.route('/turnos')
@admin_required
def turnos():
    try:
        user = get_user_object(session['user'])
        
        turnos = None
        funcionarios = None

        turnos = get_turnos()
        
        funcionarios, dict_func_ids = get_funcionarios()

        if turnos and funcionarios:
            if request.args.get('date'):
                try:
                    date_arr = request.args.get('date').split('-')
                    date = f'{date_arr[2]}/{date_arr[1]}/{date_arr[0]}'
                    turnos = filtra_turnos(turnos, lambda x: x.dia == date)

                except:
                    pass

            if request.args.get('funcionario'):
                try:
                    func_id = int(request.args.get('funcionario'))
                    turnos = filtra_turnos(turnos, lambda x: x.user_id == func_id)

                except:
                    pass

            else:
                return render_template('turnos.html', turnos=turnos, turnos_active='active',
                                                    funcionarios=funcionarios, dict_func_ids=dict_func_ids,
                                                    user=user)

        else:
            return render_template('turnos.html', turnos_active='active', user=user,
                                                funcionarios=funcionarios)

    except Exception as e:            
        return flask.abort(500, e)

@turnos_blueprint.route('/turno')
@funcionario_required
def turno():

    user = get_user_object(session['user'])
    date = request.args.get('date')
    func_id = int(request.args.get('user_id'))
    turno = db.get_turno(date, func_id)
    
    if is_admin(user) or (user.id == func_id):
        if turno:
            funcionario = db.get_funcionario(func_id)
            cargo = db.get_cargo(funcionario.cargo)
            percentage,turno_total, extras_percentage, trabalho_extra = get_work(turno, funcionario)
            
            horas = timedelta(seconds=turno_total)
            horas_string = str(horas)[:4]
            horas_extras = timedelta(seconds=trabalho_extra)
            extras_string = str(horas_extras)[:4]
            
            return render_template('turno.html', turno=turno, 
                                funcionario=funcionario, 
                                cargo=cargo, 
                                user=user,
                                percentage=percentage,
                                extras_percentage=extras_percentage,
                                horas=horas_string,
                                horas_extras=extras_string,
                                turnos_active='active')

        return flask.abort(404, f'Turno não encontrado!')
    
    else:
        return flask.abort(401, 'Você não tem permissão para acessar a página!')

@turnos_blueprint.route('/editar-turno', methods=['GET', 'POST'])
@admin_required
def editar_turno():
    user = get_user_object(session['user'])
    
    try:
        user_id = int(request.args['user_id'])
        date = request.args['date']
        if request.method == 'GET':
            turno = db.get_turno(date, user_id)
                
            #yyyy-mm-dd
            html_date = f'{date[6:]}-{date[3:5]}-{date[:2]}'
            return render_template('editar_turno.html', user=user,
                                                        turno=turno,
                                                        html_date=html_date,
                                                        turnos_active='active')
            
        else:
            
            form = request.form
            update_turno(form, date, user_id)
            
            return redirect(url_for('turnos.turnos'))
        
    except Exception as e:
        
        return flask.abort(400, e)
    
@turnos_blueprint.route('/excluir-turno', methods=['DELETE'])
@admin_required
def excluir_turno():
    
    try:
        form = request.form
        date = form['date']
        user_id = int(form['user_id'])
        
        if db.remove_data_from_firestore('Turnos', query_arr=[['dia', date], 
                                                              ['user_id', user_id]]):
            return '', 200
    
        return 'falhou',404
    
    except Exception as e:
        return e, 400
    

@turnos_blueprint.route('/meus-turnos')
@funcionario_required
def meus_turnos():
    
    user = get_user_object(session['user'])
    
    turnos = db.get_turnos(user.id)
    
    if request.args.get('date'):
        try:
            date_arr = request.args.get('date').split('-')
            date = f'{date_arr[2]}/{date_arr[1]}/{date_arr[0]}'
            turnos = filtra_turnos(turnos, lambda x: x.dia == date)
        
        except:
            pass
    
    return render_template('meus-turnos.html', user=user,
                                            turnos=turnos,
                                            turnos_active='active')