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
    #
    # List all the turnos
    #

    try:
        user = get_user_object(session['user'])
        
        turnos = None
        funcionarios = None

        turnos = get_sorted_turnos()
   
        funcionarios, dict_user_ids = get_funcionarios()
        
        if turnos and funcionarios:
            if request.args.get('date'):
                turnos = filter_turnos_by_date(turnos, request.args.get('date'))

            if request.args.get('funcionario'):
                turnos = filter_turnos_by_funcionario(turnos, request.args.get('funcionario'))

            return render_template('turnos.html', turnos=turnos, turnos_active='active',
                                                    funcionarios=funcionarios, dict_user_ids=dict_user_ids,
                                                    user=user)

        else:
            return render_template('turnos.html', turnos_active='active', user=user,
                                                funcionarios=funcionarios)

    except Exception as e:            
        return abort(500, e)

@turnos_blueprint.route('/turno')
@funcionario_required
def turno():
    #
    # List all the turnos
    #

    user = get_user_object(session['user'])
    
    user_id = int(request.args.get('user_id'))
    if is_admin(user) or (user.id == user_id):
        date = request.args.get('date')

        turno = db.get_turno(date, user_id)
        if turno:
    
            funcionario = db.get_funcionario(user_id)
            cargo = db.get_cargo(funcionario.cargo)
            percentage,turno_total, extras_percentage, trabalho_extra = get_work(turno)
            
            horas = timedelta(seconds=turno_total)
            horas_extras = timedelta(seconds=trabalho_extra)
            horas_string = str(horas)[:4]
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

        return abort(404, f'Turno não encontrado!')
    
    else:
        return abort(401, 'Você não tem permissão para acessar a página!')

@turnos_blueprint.route('/editar-turno', methods=['GET', 'POST'])
@admin_required
def editar_turno():
    #
    # Edit a turno
    # GET: Return the turno edit page
    # POST: Update the turno
    #

    user = get_user_object(session['user'])
    
    try:
        user_id = int(request.args['user_id'])
        date = request.args['date']
        turno = db.get_turno(date, user_id)
        if request.method == 'GET':
                
            hora_entrada = (datetime.min + turno.hora_entrada).time()
            hora_saida = None
            if turno.current_status == 'clocked_out':
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
        
        return abort(400, e)
    
@turnos_blueprint.route('/excluir-turno', methods=['DELETE'])
@admin_required
def excluir_turno():
    #
    # Delete a turno
    #

    try:
        form = request.form
        turno_id = int(form['turno_id'])
        
        if db.remove_data('Turnos', turno_id):
            return '', 200
    
        return 'falhou',404
    
    except Exception as e:
        return e, 400
    

@turnos_blueprint.route('/meus-turnos')
@funcionario_required
def meus_turnos():
    #
    # List all the turnos for current user
    #
    
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