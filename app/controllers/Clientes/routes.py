from . import *
from .utils import *

clientes_blueprint = Blueprint('clientes', __name__,
                                template_folder='templates',
                                static_folder='static',
                                static_url_path='/Clientes/static')



@clientes_blueprint.route('/cliente/cadastro', methods=['GET', 'POST'])
@gestor_required
def criar_cliente():
        #
        # Create a new cliente
        # GET: Return the cliente creation page
        # POST: Create the cliente
        #

        if request.method == 'GET':
                user = get_user_object(session['user'])
                return render_template('cadastro-cliente.html', user=user, clientes_active='active')
        
        else:

                try:
                        create_cliente(request.form)

                        return redirect(url_for('clientes.clientes'))

                except Exception as e:
                        return abort(500, e)


@clientes_blueprint.route('/clientes')
@gestor_required
def clientes():
        #
        # List all the clientes
        #

        user = get_user_object(session['user'])
        clientes = db.get_table_data('Clientes')

        return render_template('clientes.html', user=user, clientes=clientes, clientes_active='active')

@clientes_blueprint.route('/editar-cliente/<id>', methods=['GET', 'POST'])
@gestor_required
def editar_cliente(id):
        #
        # Edit a cliente
        # GET: Return the cliente edit page
        # POST: Update the cliente      
        #         
        
        if request.method == 'POST':
                cliente = Cliente(request.form)
                save_logo_cliente(id)
                db.update_data('Clientes', id, cliente.to_json())

                return redirect(url_for('clientes.clientes'))
        

        user = get_user_object(session['user'])
        cliente = db.select('Clientes', 'id', '=', id)[0]
        return render_template('editar-cliente.html', user=user, cliente=cliente,
                                        clientes_active='active')


@clientes_blueprint.route('/deletar-cliente', methods=['delete'])
@gestor_required
def deletar_cliente():
        #
        # Delete a cliente
        #
        id = request.form.get('uid', type=int)  
        try:
        
                db.remove_data('Clientes', id)

                return '', 200
        
        except:
                return '', 404