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
@admin_required
def listar_ferias():
    user = get_user_object(session['user'])
    all_ferias = db.get_all_ferias()
    return render_template('listar_ferias.html', ferias_active='active', all_ferias=all_ferias, user=user)
  
@ferias_blueprint.route('/adicionar', methods=['GET', 'POST'])
@admin_required
def adicionar():
    user = get_user_object(session['user'])
    
    if request.method == 'GET':
        return render_template('adicionar-ferias.html', ferias_active='active', user=user)
    
    else:
        form = dict(request.form)
    
        form['inicio'] = datetime.strptime(form['inicio'], '%Y-%m-%d')
        form['fim'] = datetime.strptime(form['fim'], '%Y-%m-%d')
        db.create_ferias(form)
        
        return redirect(url_for('ferias.listar_ferias'))
    
@ferias_blueprint.route('/editar/<int:ferias_id>', methods=['GET', 'POST'])
@admin_required
def editar(ferias_id):
    user = get_user_object(session['user'])
    
    if request.method == 'GET':
        ferias = db.get_ferias(ferias_id)
        return render_template("editar-ferias.html", ferias_active='active',
                                                    ferias=ferias, user=user)
    
    else:
        
        form = dict(request.form)
        form['inicio'] = datetime.strptime(form['inicio'], '%Y-%m-%d')
        form['fim'] = datetime.strptime(form['fim'], '%Y-%m-%d')
        form['id'] = ferias_id
        ferias = Ferias(form)

        db.update_data('ferias', ferias.id, ferias.to_json())
        
        return redirect(url_for('ferias.listar_ferias'))
    

@ferias_blueprint.route('/excluir', methods=['DELETE'])
@admin_required
def excluir():
    
    form = request.form
    try:
        ferias_id = int(form['id'])
        
        db.remove_data('ferias', ferias_id)

        return '', 200
    except:
        
        return '', 404
