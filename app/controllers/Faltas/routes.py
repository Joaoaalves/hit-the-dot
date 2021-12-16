from . import *

faltas_blueprint = Blueprint('faltas', __name__,
                             template_folder='templates',
                             static_folder='static',
                             static_url_path='/Faltas/static/')


@faltas_blueprint.route('/faltas')
@admin_required
def listar_faltas():
    user = get_user_object(session['user'])
    faltas = db.get_all_faltas()
    funcionarios = db.get_all_funcionarios()
    func_dict = {func.id : func.name for func in funcionarios}
    
    return render_template('faltas.html', user=user,
                                        faltas=faltas,
                                        func_dict=func_dict)
    

@faltas_blueprint.route('/minhas-faltas')
@funcionario_required
def minhas_faltas():
    
    user = get_user_object(session['user'])
    faltas = db.get_faltas_funcionario(user.id)
    
    return render_template('minhas-faltas.html', user=user,
                                                faltas=faltas)
    
    
@faltas_blueprint.route('/abonar-falta', methods=['POST'])
@admin_required
def abonar_falta():
    
    falta_id = request.form['falta_id']
    
    falta = db.get_falta(falta_id)
    
    if falta:
        falta.abonar()
        db.update_info('Faltas', 'id', falta_id, falta.to_json())
        return '', 200
    
    else:
        
        return '', 404
    
@faltas_blueprint.route('/falta/<int:falta_id>')
@admin_required
def ver_falta(falta_id):
    
    falta = db.get_falta(falta_id)
    user = get_user_object(session['user'])
    
    return render_template('falta.html', user=user,
                                        falta=falta)