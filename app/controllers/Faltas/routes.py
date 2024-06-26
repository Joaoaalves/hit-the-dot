from . import *

faltas_blueprint = Blueprint('faltas', __name__,
                             template_folder='templates',
                             static_folder='static',
                             static_url_path='/Faltas/static/')


@faltas_blueprint.route('/faltas')
@admin_required
def listar_faltas():
    #
    # List all the faltas
    #

    user = get_user_object(session['user'])
    
    if 'funcionario' in request.args:
        try:
            faltas = db.get_faltas_funcionario(
                int(request.args.get('funcionario'))
            )
            
        except:
            faltas = None
    else:        
        faltas = db.get_all_faltas()
        
    funcionarios = db.get_all_funcionarios()
    func_dict = dict((func.id, func.name) for func in funcionarios)
    
    return render_template('faltas.html', user=user,
                                        faltas=faltas,
                                        func_dict=func_dict,
                                        turnos_active='active')
    

@faltas_blueprint.route('/minhas-faltas')
@funcionario_required
def minhas_faltas():
    #
    # List all the faltas
    #

    user = get_user_object(session['user'])
    
    faltas = db.get_faltas_funcionario(user.id)
    
    return render_template('minhas-faltas.html', user=user,
                                                faltas=faltas,
                                                turnos_active='active')
    
    
@faltas_blueprint.route('/abonar-falta', methods=['POST'])
@admin_required
def abonar_falta():
    #
    # Change Falta status to ABONADA
    #

    try:
        falta_id = int(request.form['falta_id'])
        falta = db.get_falta(falta_id)
        
        if falta:
        
            falta.abonar()
        
            db.update_data('Faltas', falta.id, falta.to_json())
        
            return '', 200
        else:
            
            return '', 402
        
    except Exception as e:
        print(e)
        return '',500
    
    
@faltas_blueprint.route('/falta/<int:falta_id>')
@admin_required
def ver_falta(falta_id):
    #
    # Show a falta
    #

    falta = db.get_falta(falta_id)

    user = get_user_object(session['user'])
    
    funcionario = db.get_funcionario(falta.user_id)
    
    return render_template('falta.html', user=user,
                                        falta=falta,
                                        funcionario=funcionario,
                                        turnos_active='active')