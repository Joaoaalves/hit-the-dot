from os import abort
from . import *
from .utils import *
from datetime import datetime

ferias_blueprint = Blueprint('ferias', __name__,
                             template_folder='templates',
                             static_folder='static',
                             static_url_path='/Ferias/static',
                             url_prefix='/ferias')

@ferias_blueprint.route('/')
@funcionario_required
def listar_ferias():
    user = get_user_object(session['user'])
    all_ferias = db.get_all_ferias()
    return render_template('listar_ferias.html', ferias_active='active', all_ferias=all_ferias, user=user)


@ferias_blueprint.route('/<int:ferias_id>')
@admin_required
def ferias(ferias_id):
    user = get_user_object(session['user'])
    ferias = db.get_ferias(ferias_id)
    
    funcionarios = list()
    for f_id in ferias.funcionarios:
        
        funcionarios.append(db.get_funcionario(f_id))
        
    if ferias:
        return render_template('ferias.html', user=user, funcionarios=funcionarios, 
                               ferias=ferias)

    return abort(404, 'Ferias not Found!')

@ferias_blueprint.route('/<int:ferias_id>/remover-funcionario', methods=['DELETE'])
@admin_required
def remover_funcionario(ferias_id):
    try:
        ferias = db.get_ferias(ferias_id)
        
        func_id = int(request.form['id'])
        
        ferias.funcionarios.remove(func_id)
        
        db.update_info('Ferias', ferias.to_json(), 'id', ferias_id)
        
        return '', 200
    
    except Exception as e:
        
        return e, 500
    
@ferias_blueprint.route('/adicionar', methods=['GET', 'POST'])
@admin_required
def adicionar():
    user = get_user_object(session['user'])
    
    if request.method == 'GET':
        funcionarios = db.get_all_funcionarios()
        return render_template('adicionar-ferias.html', funcionarios=funcionarios, ferias_active='active', user=user)
    
    else:
        form = dict(request.form)
    
        form['inicio'] = html_date_to_timestamp(form['inicio'])
        form['fim'] = html_date_to_timestamp(form['fim'])
        form['funcionarios'] = [int(f) for f in request.form.getlist('funcionarios')]
        
        db.create_ferias(form)
        
        return redirect(url_for('ferias.listar_ferias'))
    
@ferias_blueprint.route('/editar/<int:ferias_id>', methods=['GET', 'POST'])
@admin_required
def editar(ferias_id):
    user = get_user_object(session['user'])
    
    if request.method == 'GET':
        ferias = db.get_ferias(ferias_id)
        funcionarios = db.get_all_funcionarios()
        return render_template("editar-ferias.html", ferias_active='active', funcionarios=funcionarios,
                                                    ferias=ferias, user=user)
    
    else:
        
        form = dict(request.form)
        form['inicio'] = html_date_to_timestamp(form['inicio'])
        form['fim'] = html_date_to_timestamp(form['fim'])
        form['funcionarios'] = [int(f) for f in request.form.getlist('funcionarios')]
        form['id'] = ferias_id

        db.update_info('Ferias', form, 'id', ferias_id)
        
        return redirect(url_for('ferias.listar_ferias'))
    

@ferias_blueprint.route('/excluir', methods=['DELETE'])
@admin_required
def excluir():
    
    form = request.form
    try:
        ferias_id = int(form['id'])
        
        db.remove_data_from_firestore('Ferias', 'id', ferias_id)

        return '', 200    
    except:
        
        return '', 404
