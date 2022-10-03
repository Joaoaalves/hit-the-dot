from . import *
from .utils import *

servicos_blueprint = Blueprint('servicos',
                               __name__,
                               template_folder='templates',
                               static_folder='static',
                               static_url_path='/Servicos/static')


@servicos_blueprint.route('/servicos')
@admin_required
def servicos():
    #
    #   List all services
    #
    user = get_user_object(session['user'])

    servicos = db.get_servicos()

    return render_template('servicos.html', user=user,
                           servicos_active='active',
                           servicos=servicos)


@servicos_blueprint.route('/servicos/tags')
@admin_required
def servicos_tags():
    #
    #  List all services tags
    #
    user = get_user_object(session['user'])

    servicos = db.get_servicos()

    tags = db.get_tags()

    return render_template('servicos_tags.html', user=user,
                           servicos_active='active',
                           tags=tags,
                           servicos=servicos)


@servicos_blueprint.route('/servicos/tags/excluir/', methods=['DELETE'])
@admin_required
def servicos_tags_excluir():
    #
    #  Delete a service tag
    #
    tag_id = request.form['tag']

    excluir_tag(tag_id)

    return '', 200


@servicos_blueprint.route('/servicos/tags/criar', methods=['GET', 'POST'])
@admin_required
def servicos_tags_criar():
    #
    # Create a new service tag
    # GET: Show the form
    # POST: Create the tag
    #

    user = get_user_object(session['user'])
    servicos = db.get_servicos()

    if request.method == 'GET':
        return render_template('servicos_tags_criar.html', user=user,
                               servicos_active='active',
                               servicos=servicos)

    else:
        criar_tag(request.form)

        return redirect(url_for('servicos.servicos_tags'))


@servicos_blueprint.route('/servicos/tags/editar/<tag_id>', methods=['GET', 'POST'])
@admin_required
def servicos_tags_editar(tag_id):
    #
    # Edit a service tag
    # GET: Show the form
    # POST: Update the tag
    #

    user = get_user_object(session['user'])
    servicos = db.get_servicos()

    if request.method == 'GET':
        # Get tag
        tag = db.get_tag(tag_id)

        # Get servicos that are mapped to this tag
        servicos_selecionados = [s.to_json()
                                 for s in db.get_servicos_by_tag(tag_id)]

        return render_template('servicos_tags_editar.html', user=user,
                               servicos_active='active',
                               servicos=servicos,
                               tag=tag,
                               servicos_selecionados=servicos_selecionados)

    else:
        editar_tag(request.form, tag_id)

        return redirect(url_for('servicos.servicos_tags'))


@servicos_blueprint.route('/servicos/pesquisar', methods=['POST'])
@limiter.limit('60/minute')
def pesquisar_servico():
    #
    #  Search for a service
    #
    search_term = request.form['service_name']

    servicos = pesquisa_servicos(search_term)

    # Sort servicos by name
    servicos = sorted(servicos, key=lambda s: s['name']) if servicos else None

    # Get Atributos from Servicos
    servicos_with_atributes = get_servicos_with_atributos(
        servicos) if servicos else None

    return json.dumps(servicos_with_atributes), 200


@servicos_blueprint.route('/servicos/criar', methods=['GET', 'POST'])
@gestor_required
def criar_servico():
    #
    # Create a new service
    # GET: Show the form
    # POST: Create the service
    #

    if request.method == 'POST':

        adicionar_servico(request.form)

        return redirect(url_for('servicos.servicos'))

    else:
        user = get_user_object(session['user'])

        return render_template('criar-servico.html', user=user, servicos_active='active')


@servicos_blueprint.route('/servicos/entregar', methods=['GET', 'POST'])
@funcionario_required
def entregar_servico():
    #
    # Deliver a service
    # GET: Show the form
    # POST: Deliver the service
    #

    user = get_user_object(session['user'])
    if request.method == 'GET':
        servicos = db.get_servicos()
        clientes = db.get_clientes()

        return render_template('entrega-servico.html',  servicos=servicos,
                               entregar_servico_active='active',
                               user=user,
                               clientes=clientes)

    else:
        adicionar_servico_entregue(request.form, user.id)

        return redirect(url_for('servicos.meus_servicos')) if not is_gestor(user) else redirect(url_for('servicos.servicos_entregues'))


@servicos_blueprint.route('/servicos/<int:serv_id>', methods=['GET', 'POST'])
@gestor_required
def editar_serv(serv_id):
    #
    # Edit a service
    # GET: Show edit form
    # POST: Edit service
    #

    servico = db.get_servico(serv_id)

    if not servico:
        return abort(404)

    if request.method == 'GET':

        user = get_user_object(session['user'])

        return render_template('editar-servico.html',   user=user,
                               servico=servico,
                               servicos_active='active')

    if request.method == 'POST':
        try:
            editar_servico(request.form, servico)

            return redirect(url_for('servicos.servicos'))

        except Exception as e:
            return abort(400, request.form)


@servicos_blueprint.route('/servicos/excluir', methods=['DELETE'])
@gestor_required
def excluir_serv():
    #
    # Delete a service
    #

    try:
        servico_id = int(request.form['servico'])

        excluir_servico(servico_id)

        return json.dumps({'status': 'ok'}), 200

    except Exception as e:
        print(e)
        return json.dumps({'status': 'error'}), 400


@servicos_blueprint.route('/servicos-entregues/invalidar', methods=['POST'])
@gestor_required
def invalidar_serv():
    #
    # Invalidate a delivered service
    #

    try:
        servico_id = int(request.form['servico'])
        invalidar_servico(servico_id)

        return json.dumps({'status': 'ok'}), 200

    except:
        return json.dumps({'status': 'error'}), 400


@servicos_blueprint.route('/servicos-entregues')
@gestor_required
def servicos_entregues():
    #
    # Show delivered services
    #

    user = get_user_object(session['user'])

    func_id = request.args.get('funcionario', None)

    servicos_entregues = get_servicos_entregues(func_id)

    servicos_dict = {}
    servicos = db.get_servicos()

    if servicos:
        servicos_dict = dict((s.id, s.name) for s in servicos)

    funcionarios = db.get_all_funcionarios()

    funcionario_dict = dict((f.id, f.name) for f in funcionarios)

    return render_template('servicos-entregues.html',       user=user,
                           servicos_entregues_active="active",
                           servicos=servicos_entregues,
                           funcionarios_dict=funcionario_dict,
                           funcionarios=funcionarios,
                           servicos_dict=servicos_dict)


@servicos_blueprint.route('/servicos-entregues/<int:serv_id>', methods=['GET', 'POST'])
@gestor_required
def servico_entregue(serv_id):
    #
    # Show a delivered service
    # GET: Show the service
    # POST: Edit the service
    #

    servico_entregue = db.get_servico_entregue(serv_id)

    if servico_entregue:

        servico = db.get_servico(servico_entregue.service_id)

        atributo = db.get_atributo_from_serv(servico_entregue.id)

        if request.method == 'GET':

            user = get_user_object(session['user'])
            if user.id == servico_entregue.user_id:
                return redirect(url_for('servicos.servicos_entregues'))

            cliente = db.select('Clientes', 'id', '=',
                                servico_entregue.cliente_id)[0]
            funcionario = db.get_funcionario(servico_entregue.user_id)

            if servico_entregue:
                return render_template('aprovar-servico.html', user=user,
                                       servico_entregue=servico_entregue,
                                       servico=servico,
                                       servicos_entregues_active="active",
                                       atributo=atributo,
                                       cliente=cliente,
                                       funcionario=funcionario)
        if request.method == 'POST':

            try:
                atualizar_servico_entregue(
                    request.form, servico_entregue, atributo, servico)

            except Exception as e:
                abort(400, e)

            return redirect(url_for('servicos.servicos_entregues'))

    else:
        return abort(404, 'Nenhum serviço encontrado')


@servicos_blueprint.route('/servicos-entregues/<int:serv_id>', methods=['DELETE'])
@funcionario_required
def excluir_servico_entregue(serv_id):
    #
    # Delete a delivered service
    #

    user = get_user_object(session['user'])
    servico_id = int(serv_id)

    servico_entregue = db.get_servico_entregue(servico_id)

    if is_func(user) and servico_entregue.status != 'Pendente':
        return json.dumps({'error': 'Serviço já foi verificado'}), 400
    elif is_func(user) and servico_entregue.user_id != user.id:
        return json.dumps({'error': 'Serviço não foi entregue por você'}), 400
    else:
        db.remove_data('ServicosEntregues', servico_id)

    return json.dumps({'status': 'ok'}), 200


@servicos_blueprint.route('/meus-servicos')
@funcionario_required
def meus_servicos():
    #
    # Show delivered services for current user
    #

    user = get_user_object(session['user'])

    servicos_atribuidos = db.get_servicos_atribuidos_funcionario(user.id)

    if servicos_atribuidos:
        servicos_atribuidos.reverse()

    servicos_dict = {}
    servicos = db.get_servicos()
    if servicos:
        servicos_dict = dict((s.id, s.name) for s in servicos)

    clientes = dict((c['id'], c['name'])
                    for c in db.get_table_data('Clientes'))

    return render_template('meus-servicos.html',    user=user,
                           meus_servicos_active='active',
                           servicos=servicos_atribuidos,
                           servicos_dict=servicos_dict,
                           clientes=clientes)


@servicos_blueprint.route('/meus-servicos/<int:serv_id>', methods=['GET', 'POST'])
@funcionario_required
def editar_meu_serv(serv_id):
    #
    # Show or edit a delivered service for current user
    # GET: Show the service
    # POST: Edit the service
    #

    user = get_user_object(session['user'])
    servico_entregue = db.get_servico_entregue(serv_id)
    if servico_entregue and servico_entregue.user_id == user.id:

        servico = db.get_servico(servico_entregue.service_id)
        atributo = db.get_atributo_from_serv(servico_entregue.id)

        if request.method == 'GET':

            if user.id != servico_entregue.user_id:
                return redirect(url_for('servicos.meus_servicos'))

            clientes = db.get_table_data('Clientes')
            funcionario = db.get_funcionario(servico_entregue.user_id)
            atb = db.get_atributo_from_serv(serv_id)
            if servico_entregue:
                return render_template('editar-meu-servico.html', user=user,
                                       servico_entregue=servico_entregue,
                                       servico=servico,
                                       atb=atb,
                                       meus_servicos_active="active",
                                       atributo=atributo,
                                       clientes=clientes,
                                       funcionario=funcionario)

        if request.method == 'POST':

            try:
                editar_meu_servico(request.form, servico_entregue)

            except Exception as e:
                print(e)
                abort(400)
            return redirect(url_for('servicos.meus_servicos'))
    else:
        return abort(404, 'Nenhum serviço encontrado')
