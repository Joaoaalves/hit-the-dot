from . import app, request, db, Servico, datetime, ServicoEntregue
import os


def save_logo_cliente(image, cliente_id):

    image.save(os.path.join(
        app.config['CLIENTES_LOGO_FOLDER'],  str(cliente_id) + ".jpg"))


def criar_tag(form):
    tag = request.form['tag']
    servicos_selecionados = request.form.getlist('servicos')

    tag_id = db.insert_data('TagServicos', {'tag': tag})
    if servicos_selecionados:
        for servico in servicos_selecionados:
            db.insert_data('TagServicos_Maps', {
                           'servico': servico, 'tag': tag_id})


def editar_tag(form, tag_id):
    tag = form['tag']
    servicos_selecionados = request.form.getlist('servicos')

    # Update tag
    db.update_data('TagServicos', tag_id, {'tag': tag})

    # Remove old tag map info
    tag_map = db.select('TagServicos_Maps', 'tag', '=', tag_id)
    if tag_map:
        for tm in tag_map:
            db.remove_data('TagServicos_Maps', tm['id'])

    # Add new tag map info
    for servico in servicos_selecionados:
        db.insert_data('TagServicos_Maps', {'servico': servico, 'tag': tag_id})


def excluir_tag(tag_id):
    db.remove_data('TagServico', tag_id)
    tag_map = db.select('TagServicos_Maps', 'tag', '==', tag_id)
    for tm in tag_map:
        db.remove_data('TagServicos_Maps', tm['id'])


def pesquisa_servicos(search_term):
    # Get servicos that match the search term
    servicos = db.select('Servicos', 'name', 'LIKE', f'%{search_term}%')
    servicos_ids = [s['id'] for s in servicos]

    # Get tags that match the search term
    tags = db.select('TagServicos', 'tag', 'LIKE', f'%{search_term}%')

    # Get servicos that are mapped to the tags that match the search term
    tags_servicos = []
    for tag in tags:
        tags_servicos.extend([s['servico'] for s in db.select(
            'TagServicos_Maps', 'tag', '=', tag['id'])])

    for sid in set(tags_servicos):
        if sid not in servicos_ids:
            servicos.append(db.select('Servicos', 'id', '=', sid)[0])

    return servicos


def get_servicos_with_atributos(servicos):
    # Get atb values for each servico
    for serv in servicos:
        atb = db.select('AtributosServicos', 'servico', '=', serv['id'])
        if atb:
            serv['atributo'] = atb[0]
    return servicos


def adicionar_servico(form):
    servico = Servico(form)
    servico_id = db.insert_data('Servicos', servico.to_json())

    # Insert atributo
    if 'has_atb' in form:
        atb_name = form['atb_name']
        atb_type = form['atb_type']

        if atb_type == 'text':
            atb_default = form['atb_default']
        else:
            try:
                atb_default = int(form['atb_default'])
            except:
                atb_default = 0

        db.insert_data('AtributosServicos', {
                       'name': atb_name, 'servico': servico_id, 'type': atb_type, 'default_value': atb_default})


def adicionar_servico_entregue(form, user_id):
    insertion_id = db.insert_data('ServicosEntregues', {
        'service_id': form['servico'],
        'user_id': user_id,
        'status': 'Pendente',
        'cliente_id': form['cliente'],
        'link_trello': form['trello'],
        'descricao': form['descricao'],
        'entrega': datetime.now().date()
    })

    if 'atributo' in form:

        db.insert_data('AtributosValues', {
            'value': form['atributo'],
            'servico_entregue': insertion_id,
            'atributo': form['atb_id']
        })


def editar_servico(form, servico):

    servico.name = form['name']
    servico.tempo = form['tempo']
    servico.valor = form['valor']

    db.update_data('Servicos', servico.id, servico.to_json())


def excluir_servico(servico_id):
    servicos_entregues = [ServicoEntregue(servico) for servico in db.select(
        'ServicosEntregues', 'service_id', '=', servico_id)]
    for serv in servicos_entregues:
        db.remove_data('ServicosEntregues', serv.id)

    db.remove_data('Servicos', servico_id)


def invalidar_servico(servico_id):
    servico = db.get_servico_entregue(servico_id)
    servico.status = 'Pendente'

    db.update_data('ServicosEntregues', servico_id, servico.to_json())


def get_servicos_entregues(user_id):
    try:
        if user_id:
            servicos_atribuidos = db.get_servicos_atribuidos_funcionario(
                int(user_id))
        else:
            servicos_atribuidos = db.get_servicos_atribuidos()

        if servicos_atribuidos:
            servicos_atribuidos.reverse()

    except Exception as e:

        servicos_atribuidos = None
    return servicos_atribuidos


def atualizar_servico_entregue(form, servico_entregue, atributo, servico):
    if 'status' in form and form['status'] == 'Pendente':

        servico_entregue.status = 'Pendente'

        db.update_data('ServicosEntregues',
                       servico_entregue.id, servico_entregue.to_json())

        return '', 200

    servico_entregue.prazo = float(form['prazo'])
    quantidade = int(
        atributo.value) if atributo and atributo.type != 'text' else 1

    servico_entregue.valor = servico.valor * servico_entregue.prazo * quantidade

    servico_entregue.status = 'Verificado'

    db.update_data('ServicosEntregues',
                   servico_entregue.id, servico_entregue.to_json())


def editar_meu_servico(form, servico_entregue):
    servico_entregue.cliente_id = int(form['cliente_id'])
    servico_entregue.descricao = form['descricao']
    servico_entregue.service_id = int(form['service_id'])
    servico_entregue.link_trello = form['link_trello']

    db.update_data('ServicosEntregues',
                   servico_entregue.id, servico_entregue.to_json())
