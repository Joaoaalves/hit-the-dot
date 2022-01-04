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
    
        form['inicio'] = html_date_to_timestamp(form['inicio'], '00:00:00')
        form['fim'] = html_date_to_timestamp(form['fim'], '23:59:59')
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
        form['inicio'] = html_date_to_timestamp(form['inicio'], '00:00:00')
        form['fim'] = html_date_to_timestamp(form['fim'], '23:59:59')
        form['id'] = ferias_id
        ferias = Ferias(form)

        db.update_info('Ferias', ferias.to_json(), 'id', ferias.id)
        
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
