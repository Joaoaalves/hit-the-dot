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

        turnos = get_sorted_turnos()
   
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
    
    func_id = int(request.args.get('user_id'))
    if is_admin(user) or (user.id == func_id):
        date = request.args.get('date')

        turno = db.get_turno(date, func_id)
        if turno:
    
            funcionario = db.get_funcionario(func_id)
            cargo = db.get_cargo(funcionario.cargo)
            percentage,turno_total, extras_percentage, trabalho_extra = get_work(turno)
            
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
        turno = db.get_turno(date, user_id)
        if request.method == 'GET':
                
            hora_entrada = (datetime.min + turno.hora_entrada).time()
            hora_saida  = (datetime.min + turno.hora_saida).time()

            return render_template('editar_turno.html', user=user,
                                                        hora_entrada=hora_entrada,
                                                        hora_saida=hora_saida,
                                                        turno=turno,
                                                        turnos_active='active')
            
        else:
            
            form = request.form
            update_turno(form, user_id, turno)
            
            return redirect(url_for('turnos.turnos'))
        
    except Exception as e:
        
        return flask.abort(400, e)
    
@turnos_blueprint.route('/excluir-turno', methods=['DELETE'])
@admin_required
def excluir_turno():
    
    try:
        form = request.form
        turno_id = int(form['turno_id'])
        
        if db.remove_data('turnos', turno_id):
            return '', 200
    
        return 'falhou',404
    
    except Exception as e:
        return e, 400
    

@turnos_blueprint.route('/meus-turnos')
@funcionario_required
def meus_turnos():
    
    user = get_user_object(session['user'])
    
    turnos = get_sorted_turnos(funcionario=user.id)    
    if request.args.get('date'):
        try:
            date_string = request.args.get('date')
            turnos = filtra_turnos(turnos, lambda x: str(x.dia) == date_string)
        
        except:
            pass
    
    return render_template('meus-turnos.html', user=user,
                                            turnos=turnos,
                                            turnos_active='active')

@turnos_blueprint.route('/extrato/<int:func_id>')
@admin_required
def extrato(func_id):
    func = db.get_funcionario(func_id)

    if func:
        turnos = get_sorted_turnos(funcionario=func.id)
        
        return render_template('extrato.html', turnos=turnos,
                                                func=func)

                                            