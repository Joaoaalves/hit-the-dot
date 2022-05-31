from . import *
from .utils import save_logo_cliente

demandas_blueprint = Blueprint('demandas', __name__,
                                template_folder='templates',
                                static_folder='static',
                                static_url_path='/Demandas/static')


@demandas_blueprint.route('/demandas')
@gestor_required
def demandas():
        user = get_user_object(session['user'])

        if 'funcionario' in request.args:
                funcionario = request.args['funcionario']
                demandas = db.get_demandas_by_funcionario(funcionario)
        else:
                demandas = db.get_all_demandas()
        
        
        if 'date' in request.args and demandas:
                with suppress(ValueError, TypeError): 
                        date = datetime.strptime(request.args['date'], '%Y-%m-%d').date()
                        demandas = [d for d in demandas if d.date == date]

        if 'status' in request.args and demandas:
                status = request.args.getlist('status')
                for d in demandas:
                        print(d.status)
                        
                demandas = [d for d in demandas if d.status.lower() in status]
                
        func_dict = {f.id : f.name for f in db.get_all_funcionarios()}

        funcionarios = db.get_all_funcionarios()
        demandas = sorted(demandas, key=lambda d: d.date, reverse=True)

        return render_template('demandas.html', user=user, 
                                                demandas_active='active',
                                                func_dict=func_dict,
                                                funcionarios=funcionarios,
                                                demandas = demandas)

@demandas_blueprint.route('/minhas-demandas')
@funcionario_required
def minhas_demandas():
        user = get_user_object(session['user'])
        demandas = [d for d in db.get_all_demandas() if d.func_id == user.id]
        funcionarios = {f.id : f.name for f in db.get_all_funcionarios()}
        demandas = sorted(demandas, key=lambda d: d.date, reverse=True)
        return render_template('minhas-demandas.html', user=user, 
                                                demandas_active='active',
                                                funcionarios = funcionarios,
                                                demandas = demandas)

@demandas_blueprint.route('/demanda/<int:id>', methods=['GET', 'POST'])
@funcionario_required
def demanda(id):
        demanda = db.get_demanda(id)
        if request.method == 'GET':
                user = get_user_object(session['user'])
                return render_template('demanda.html', user=user, demanda=demanda,
                                                demandas_active='active')

        else:
                demanda.name = request.form['name']
                demanda.url = request.form['url']

                db.update_data('demandas', id ,demanda.to_json())
                return redirect(url_for('demandas.minhas_demandas'))

@demandas_blueprint.route('/demandas/adicionar', methods=['GET', 'POST'])
@funcionario_required
def adicionar_demanda():
        if request.method == 'GET':
                user = get_user_object(session['user'])
                return render_template('adicionar-demanda.html', user=user, 
                                                        demandas_active='active')

        else:
                user = get_user_object(session['user'])
                form = request.form
                data = dict()
                data['func_id'] = user.id
                data['status'] = 'Pendente'
                data['date'] = datetime.now().date()
                data['url'] = form['url']
                data['name'] = form['name']

                demanda = Demanda(data)
                db.insert_data('demandas', demanda.to_json())
                
                return redirect(url_for('demandas.minhas_demandas'))

@demandas_blueprint.route('/demandas/change-status', methods=['POST'])
@gestor_required
def change_status():
        form = request.form
        demanda_id = form['demanda_id']
        status = form['status']
        demanda = db.get_demanda(demanda_id)
        
        if status == 'true':
                demanda.status = 'Verificada'
        else:
                demanda.status = 'Pendente'

        try:
                db.update_data('demandas', demanda.id, demanda.to_json())
                return redirect(url_for('demandas.demandas'))
        except:
                return abort(400, 'Não foi possível alterar o status da demanda')


@demandas_blueprint.route('/servicos/entregar', methods=['GET', 'POST'])
@funcionario_required
def search():
        user = get_user_object(session['user'])
        if request.method == 'GET':
                servicos = db.get_servicos()
                clientes = db.get_clientes()
                
                return render_template('entrega_servico.html', servicos=servicos, user=user, clientes=clientes)

        else:
                form = request.form 
                cliente = form['cliente']
                servico = form['servico']
                link_trello = form['trello']
                servico_atribuido = {
                        'service_id' : servico,
                        'user_id' : user.id,
                        'status' : 'Pendente',
                        'is_verified' : False,
                        'cliente_id' : cliente,
                        'link_trello' : link_trello
                }

                db.insert_data('servicos_atribuidos', servico_atribuido)
                return redirect(url_for('demandas.servicos_entregues'))


@demandas_blueprint.route('/servicos')
@gestor_required
def servicos():
        user = get_user_object(session['user'])

        servicos = db.get_servicos()

        categorias = dict()
        for c in db.get_table_data('categoria_servico'):
                categorias[c['id']] = c['name']

        return render_template('servicos.html', user=user,
                                                servicos=servicos,
                                                categorias=categorias)

@demandas_blueprint.route('/servicos-atribuidos')
@gestor_required
def servicos_atribuidos():

        user = get_user_object(session['user'])

        servicos = db.get_servicos_atribuidos()
        servicos_dict = dict()
        for servico in db.get_servicos():
                servicos_dict[servico.id] = servico.name

        cliente_dict = dict()
        for cliente in db.get_clientes():
                cliente_dict[cliente['id']] = cliente['name']

        funcionario_dict  = dict()
        for funcionario in db.get_all_funcionarios():
                funcionario_dict[funcionario.id] = funcionario.name

        return render_template('servicos-atribuidos.html', user=user,
                                                        servicos=servicos,
                                                        clientes=cliente_dict,
                                                        funcionarios=funcionario_dict,
                                                        servicos_dict=servicos_dict)

@demandas_blueprint.route('/servicos-atribuidos/excluir', methods=['DELETE'])
@gestor_required
def excluir_servico():

        servico_id = request.form['servico']

        db.remove_data('servicos_atribuidos', servico_id)

        return '', 200

@demandas_blueprint.route('/servicos-atribuidos/atualizar', methods=['POST'])
@gestor_required
def atualizar_status():

        new_status = request.form['status']
        servico_id = request.form['servico']

        servico = db.get_servico_atribuido(servico_id)

        servico.is_verified = new_status == 'true'
        
        db.update_data('servicos_atribuidos', servico.id, servico.to_json())

        return '', 200


@demandas_blueprint.route('/servicos-entregues')
@funcionario_required
def servicos_entregues():
        user = get_user_object(session['user'])

        servicos = [ ServicoAtribuido(s) for s in db.select('servicos_atribuidos', 'user_id', '=', user.id)]
        servicos_dict = dict()
        for s in db.get_servicos():
                servicos_dict[s.id] = s.name

        clientes = dict()
        for c in db.get_table_data('cliente'):
                clientes[c['id']] = c['name']


        return render_template('servicos-entregues.html', user=user,
                                                        servicos=servicos,
                                                        servicos_dict=servicos_dict,
                                                        clientes=clientes)