from . import *

clientes_blueprint = Blueprint('clientes', __name__,
                                template_folder='templates',
                                static_folder='static',
                                static_url_path='/Clientes/static')



@clientes_blueprint.route('/listar-clientes')
@funcionario_required
def clientes():
        
        user = get_user_object(session['user'])
        
        clientes = db.get_all_clientes()
        
        return render_template('clientes.html', user=user,
                                                clientes=clientes,
                                                clientes_active='active')


@clientes_blueprint.route('/cliente/cadastro', methods=['GET', 'POST'])
@admin_required
def cadastrar_cliente():
                
        user = get_user_object(session['user'])
        
        if request.method == 'POST':
                nome = request.form['nome']
                cpf = request.form['cpf']
                rg = request.form['rg']
                endereco = request.form['endereco']
                numero = request.form['numero']
                complemento = request.form['complemento']
                bairro = request.form['bairro']
                cidade = request.form['cidade']
                estado = request.form['estado']
                cep = request.form['cep']
                telefone = request.form['telefone']
                celular = request.form['celular']
                email = request.form['email']
                data_nascimento = request.form['data_nascimento']

                cliente = Cliente(nome, cpf, rg, endereco, 
                        numero, complemento, bairro, cidade, estado, 
                        cep, telefone, celular, email, data_nascimento)
                
                db.add_data_on_firestore('Clientes', cliente)
                
                return redirect(url_for('clientes.clientes'))
        
        return render_template('cadastro-cliente.html', user=user, clientes_active='active')

@clientes_blueprint.route('/editar-cliente/<id>', methods=['GET', 'POST'])
@admin_required
def editar_cliente(id):
                
        user = get_user_object(session['user'])
        
        cliente = db.get_data_from_firestore('Clientes', id)
        
        if request.method == 'POST':
                nome = request.form['nome']
                cpf = request.form['cpf']
                rg = request.form['rg']
                endereco = request.form['endereco']
                numero = request.form['numero']
                complemento = request.form['complemento']
                bairro = request.form['bairro']
                cidade = request.form['cidade']
                estado = request.form['estado']
                cep = request.form['cep']
                telefone = request.form['telefone']
                celular = request.form['celular']
                email = request.form['email']
                data_nascimento = request.form['data_nascimento']

                cliente = Cliente(nome, cpf, rg, endereco, 
                        numero, complemento, bairro, cidade, estado, 
                        cep, telefone, celular, email, data_nascimento)
                
                db.update_info('Clientes', cliente, key='id', value=cliente.id)
                
                return redirect(url_for('clientes.clientes'))
        
        return render_template('editar_cliente.html', user=user, cliente=cliente,
                                        clientes_active='active')


@clientes_blueprint.route('/deletar-cliente', methods=['delete'])
@admin_required
def deletar_cliente():

        id = request.form.get('uid', type=int)  
        
        return '', 200 if db.remove_data_from_firestore('Clientes', key='id', value=id) else '', 404