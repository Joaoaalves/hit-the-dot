from . import *
from .utils import *
from app.models.cargo import Cargo

cargos_blueprint = Blueprint('cargos', __name__,
                            template_folder='templates',
                            static_folder='static',
                            static_url_path='/Cargos/static',
                            url_prefix='/cargos')


@cargos_blueprint.route('/')
@admin_required
def cargos():
    #
    # List all the cargos
    #

    sem_cargo_id = 0
    cargos = [c for c in db.get_table_data('Cargos') if c['id'] != sem_cargo_id]

    user = get_user_object(session['user'])
    
    if cargos:
        return render_template('cargos.html', cargos=cargos, user=user)
    
    else:
        return render_template('cargos.html', user=user)
    

@cargos_blueprint.route('/criar', methods=['GET', 'POST'])
@admin_required
def adicionar_cargo():
    #
    # Create a new cargo
    # GET: Return the cargo creation page
    # POST: Create the cargo
    #

    user = get_user_object(session['user'])
    
    funcionarios = db.get_all_funcionarios()
    
    if request.method == 'GET':
        
        return render_template('criar-cargo.html', user=user, funcionarios=funcionarios)
    
    else:
        
        form = request.form
        adiciona_cargo(form)
            
        return redirect(url_for('cargos.cargos'))
        

@cargos_blueprint.route('/editar/<int:cargo_id>', methods=['GET','POST'])
@admin_required
def editar(cargo_id):
    #
    # Edit a cargo
    # GET: Return the cargo edit page
    # POST: Update the cargo
    #
    
    user = get_user_object(session['user'])
    funcionarios = db.get_all_funcionarios()
    funcionarios_do_cargo = [f.id for f in funcionarios if f.cargo == cargo_id]
    cargo = db.get_cargo(cargo_id)
    
    if request.method == 'GET':
        
        return render_template('editar-cargo.html', user=user, cargo=cargo, funcionarios=funcionarios)
    
    else:
        
        form = request.form
        
        update_cargo(form, cargo_id, funcionarios_do_cargo)
        
        return redirect(url_for('cargos.cargos'))
        
        
@cargos_blueprint.route('/excluir', methods=['DELETE'])
@admin_required
def excluir():
    #
    # Delete a cargo
    #
    
    try:
        cargo_id = int(request.form['cargo_id'])
        excluir_cargo(cargo_id)
        
        return '', 200
    
    except Exception as e:
        return abort(400, e)