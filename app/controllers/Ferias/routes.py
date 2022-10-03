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
    #
    # List all the ferias
    #

    user = get_user_object(session['user'])
    all_ferias = db.get_all_ferias()
    
    return render_template('listar_ferias.html', ferias_active='active', all_ferias=all_ferias, user=user)
  
@ferias_blueprint.route('/adicionar', methods=['GET', 'POST'])
@admin_required
def adicionar():
    #
    # Add a new ferias
    # GET: Return the ferias add page
    # POST: Add the ferias
    #
    
    user = get_user_object(session['user'])
    
    if request.method == 'GET':
        return render_template('adicionar-ferias.html', ferias_active='active', user=user)
    
    else:
        form = dict(request.form)
        
        inicio, fim = form['daterange'].split(' - ')

        ferias = {
            'inicio': datetime.strptime(inicio, '%d/%m/%Y'),
            'fim': datetime.strptime(fim, '%d/%m/%Y'),
        }
        
        db.create_ferias(ferias)
        
        return redirect(url_for('ferias.listar_ferias'))
    
@ferias_blueprint.route('/editar/<int:ferias_id>', methods=['GET', 'POST'])
@admin_required
def editar(ferias_id):
    #
    # Edit a ferias
    # GET: Return the ferias edit page
    # POST: Update the ferias
    #

    user = get_user_object(session['user'])
    
    if request.method == 'GET':
        ferias = db.get_ferias(ferias_id)
        inicio_ferias = ferias.inicio.strftime('%Y-%m-%d')
        fim_ferias = ferias.fim.strftime('%Y-%m-%d')

        return render_template("editar-ferias.html", ferias_active='active',
                                 user=user, ferias=ferias, inicio_ferias=inicio_ferias, fim_ferias=fim_ferias)
    
    else:
        
        editar_ferias(request.form, ferias_id)
        
        return redirect(url_for('ferias.listar_ferias'))
    

@ferias_blueprint.route('/excluir', methods=['DELETE'])
@admin_required
def excluir():
    #
    # Delete a ferias
    #
    
    try:
        ferias_id = int(request.form['id'])
        
        db.remove_data('Ferias', ferias_id)

        return '', 200
        
    except:
        
        return '', 404
