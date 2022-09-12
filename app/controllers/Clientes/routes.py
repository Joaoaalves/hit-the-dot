from . import *
from .utils import *

clientes_blueprint = Blueprint('clientes', __name__,
                                template_folder='templates',
                                static_folder='static',
                                static_url_path='/Clientes/static')



@clientes_blueprint.route('/cliente/cadastro', methods=['GET', 'POST'])
@gestor_required
def criar_cliente():
        if request.method == 'GET':
                user = get_user_object(session['user'])
                return render_template('cadastro-cliente.html', user=user, clientes_active='active')
        
        else:
                form = request.form
                name = form['name']
                try:
                        db.insert_data('cliente', {'name' : name})

                        cliente_criado = db.select('cliente', 'name', '=', name)[0]
                        
                        save_logo_cliente(cliente_criado['id'])

                        return redirect(url_for('clientes.clientes'))

                except Exception as e:
                        return abort(500, e)


@clientes_blueprint.route('/clientes')
@gestor_required
def clientes():
        user = get_user_object(session['user'])
        clientes = db.get_table_data('cliente')
        return render_template('clientes.html', user=user, clientes=clientes, clientes_active='active')

@clientes_blueprint.route('/editar-cliente/<id>', methods=['GET', 'POST'])
@gestor_required
def editar_cliente(id):
                
        
        if request.method == 'POST':
                cliente = Cliente(request.form)
                save_logo_cliente(id)
                db.update_data('cliente', id, cliente.to_json())

                return redirect(url_for('clientes.clientes'))
        

        user = get_user_object(session['user'])
        cliente = db.select('cliente', 'id', '=', id)[0]
        return render_template('editar-cliente.html', user=user, cliente=cliente,
                                        clientes_active='active')


@clientes_blueprint.route('/deletar-cliente', methods=['delete'])
@gestor_required
def deletar_cliente():

        id = request.form.get('uid', type=int)  
        
        db.remove_data('cliente', id)

        return '', 200