from . import *

servicos_blueprint = Blueprint('servicos', 
                                __name__,
                                template_folder='templates',
                                static_folder='static',
                                static_url_path='/Servicos/static')


@servicos_blueprint.route('/servicos')
@admin_required
def servicos():
        user = get_user_object(session['user'])
        
        servicos = db.get_servicos()

        return render_template('servicos.html', user=user, 
                                                servicos_active='active',
                                                servicos=servicos)

@servicos_blueprint.route('/servicos/tags')
@admin_required
def servicos_tags():
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
        tag_id = request.form['tag']
        db.remove_data('TagServico', tag_id)
        tag_map = db.select('TagServico_Map', 'tag', '==', tag_id)
        for tm in tag_map:
                db.remove_data('TagServico_Map', tm['id'])
        
        return '',200

@servicos_blueprint.route('/servicos/tags/criar', methods=['GET', 'POST'])
@admin_required
def servicos_tags_criar():
        user = get_user_object(session['user'])
        servicos = db.get_servicos()

        if request.method == 'GET':
                return render_template('servicos_tags_criar.html', user=user, 
                                                servicos_active='active',
                                                servicos=servicos)

        else:
                tag = request.form['tag']
                servicos_selecionados = request.form.getlist('servicos')
                
                tag_id = db.insert_data('TagServico', {'tag': tag})
                if servicos_selecionados:
                        for servico in servicos_selecionados:
                                db.insert_data('TagServico_Map', {'servico': servico, 'tag': tag_id})
                        
                return redirect(url_for('servicos.servicos_tags'))

@servicos_blueprint.route('/servicos/tags/editar/<tag_id>', methods=['GET', 'POST'])
@admin_required
def servicos_tags_editar(tag_id):
        user = get_user_object(session['user'])
        servicos = db.get_servicos()

        if request.method == 'GET':
                # Get tag
                tag = db.get_tag(tag_id)

                # Get servicos that are mapped to this tag
                servicos_selecionados = [s.to_json() for s in db.get_servicos_by_tag(tag_id)]
                
                return render_template('servicos_tags_editar.html', user=user, 
                                                servicos_active='active',
                                                servicos=servicos,
                                                tag=tag,
                                                servicos_selecionados=servicos_selecionados)

        else:
                
                tag = request.form['tag']
                servicos_selecionados = request.form.getlist('servicos')
                
                # Update tag
                db.update_data('TagServico', tag_id, {'tag': tag})

                # Remove old tag map info
                tag_map = db.select('TagServico_Map', 'tag', '=', tag_id)
                if tag_map:
                        for tm in tag_map:
                                db.remove_data('TagServico_Map', tm['id'])

                # Add new tag map info
                for servico in servicos_selecionados:
                        db.insert_data('TagServico_Map', {'servico': servico, 'tag': tag_id})
                        
                return redirect(url_for('servicos.servicos_tags'))

        

@servicos_blueprint.route('/servicos/pesquisar', methods=['POST'])
@limiter.limit('60/minute')
def pesquisar_servico():
        serv_name = request.form['service_name']

        # Get servicos that match the search term
        servs = db.select('Servico', 'name', 'LIKE', f'%{serv_name}%')
        
        # Get tags that match the search term
        tags = db.select('TagServico', 'tag', 'LIKE', f'%{serv_name}%')

        # Get servicos that are mapped to the tags that match the search term
        for tag in tags:
                servs_id = [ s['servico'] for s in db.select('TagServico_Map', 'tag', '=', tag['id'])]

                servs += db.select('Servico', 'id', 'IN', str(servs_id).replace('[', '(').replace(']', ')'))

        # Sort servicos by name
        servs = sorted(servs, key= lambda s:s['name'])
        
        # Get atb values for each servico
        for serv in servs:
                atb = db.select('AtributoServico', 'servico', '=', serv['id'])
                if atb:
                        serv['atributo'] = atb[0]
                        
        return json.dumps(servs), 200


@servicos_blueprint.route('/servicos/criar', methods=['GET', 'POST'])
@gestor_required
def adicionar_servico():

        if request.method == 'POST':

                form = request.form

                servico = Servico(form)
                servico_id = db.insert_data('Servico', servico.to_json())

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

                        db.insert_data('AtributoServico', {'name': atb_name, 'servico': servico_id, 'type': atb_type, 'default_value': atb_default})
                
                return redirect(url_for('servicos.servicos'))

        user = get_user_object(session['user'])
        
        return render_template('criar-servico.html', user=user, servicos_active='active')


@servicos_blueprint.route('/servicos/entregar', methods=['GET', 'POST'])
@funcionario_required
def entregar_servico():
        user = get_user_object(session['user'])
        if request.method == 'GET':
                servicos = db.get_servicos()
                clientes = db.get_clientes()
                
                return render_template('entrega-servico.html',  servicos=servicos,
                                                                entregar_servico_active='active',
                                                                user=user,
                                                                clientes=clientes)

        else:
                form = request.form

                insertion_id = db.insert_data('ServicoEntregue', {
                        'service_id' : form['servico'],
                        'user_id' : user.id,
                        'status' : 'Pendente',
                        'cliente_id' : form['cliente'],
                        'link_trello' : form['trello'],
                        'descricao' : form['descricao'],
                        'entrega' : datetime.now().date()
                })

                if 'atributo' in form:

                        db.insert_data('AtributoValue', {
                                'value' :form['atributo'],
                                'servico_entregue' : insertion_id,
                                'atributo' : form['atb_id']
                        })


                return redirect(url_for('servicos.meus_servicos')) if not is_gestor(user) else redirect(url_for('servicos.servicos_entregues'))

@servicos_blueprint.route('/servicos/<int:serv_id>', methods=['GET', 'POST'])
@gestor_required
def editar_servico(serv_id):
        servico = db.get_servico(serv_id)
        
        if not servico:
                return abort(404)

        if request.method == 'GET':

                user = get_user_object(session['user'])
                
                return render_template('editar-servico.html',   user=user,
                                                                servico=servico,
                                                                servicos_active='active')
                
        if request.method == 'POST':
                form = request.form
                
                servico.name = form['name']
                servico.tempo = form['tempo']
                servico.valor = form['valor']

                db.update_data('Servico', servico.id, servico.to_json())

                return redirect(url_for('servicos.servicos'))

@servicos_blueprint.route('/servicos/excluir', methods=['DELETE'])
@gestor_required
def excluir_servico():
        try:
                servico_id = int(request.form['servico'])

                servicos_entregues = [ServicoEntregue(servico) for servico in db.select('ServicoEntregue', 'service_id', '=', servico_id)]
                for serv in servicos_entregues:
                        db.remove_data('ServicoEntregue', serv.id)

                db.remove_data('Servico', servico_id)

                return json.dumps({'status': 'ok'}), 200

        except Exception as e:
                print(e)
                return json.dumps({'status': 'error'}), 400

@servicos_blueprint.route('/servicos-entregues/invalidar', methods=['POST'])
@gestor_required
def invalidar_servico():
        try:
                servico_id = int(request.form['servico'])
                
                servico = db.get_servico_entregue(servico_id)
                servico.status = 'Pendente'

                db.update_data('ServicoEntregue', servico_id, servico.to_json())

                return json.dumps({'status': 'ok'}), 200

        except:
                return json.dumps({'status': 'error'}), 400


@servicos_blueprint.route('/servicos-entregues')
@gestor_required
def servicos_entregues():

        user = get_user_object(session['user'])

        try:
                if 'funcionario' in request.args:
                                func_id = request.args['funcionario']
                                servicos = db.get_servicos_atribuidos_funcionario(int(func_id))
                else:
                        servicos = db.get_servicos_atribuidos()

                if servicos:
                        servicos.reverse()

        except Exception as e:

                servicos = None

        servicos_dict = dict((s.id, s.name) for s in db.get_servicos())

        funcionarios = db.get_all_funcionarios()

        funcionario_dict = dict((f.id, f.name) for f in funcionarios)

        return render_template('servicos-entregues.html',       user=user,
                                                                servicos_entregues_active="active",
                                                                servicos=servicos,
                                                                funcionarios_dict=funcionario_dict,
                                                                funcionarios=funcionarios,
                                                                servicos_dict=servicos_dict)


@servicos_blueprint.route('/servicos-entregues/<int:serv_id>', methods=['GET', 'POST'])
@gestor_required
def servico_entregue(serv_id):

        servico_entregue = db.get_servico_entregue(serv_id)
        if servico_entregue:
                servico = db.get_servico(servico_entregue.service_id)
                
                atributo = db.get_atributo_from_serv(servico_entregue.id) 

                if request.method == 'GET':
                        user = get_user_object(session['user'])
                        if user.id == servico_entregue.user_id:
                                return redirect(url_for('servicos.servicos_entregues'))
                        cliente = db.select('cliente', 'id', '=', servico_entregue.cliente_id)[0]
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
                        form = request.form

                        if 'status' in form and form['status'] == 'Pendente':

                                servico_entregue.status = 'Pendente'

                                db.update_data('ServicoEntregue', servico_entregue.id, servico_entregue.to_json())

                                return '', 200

                        try:    
                        
                                servico_entregue.prazo = float(form['prazo'])
                                quantidade = int(atributo.value) if atributo else 1

                                servico_entregue.valor = servico.valor * servico_entregue.prazo * quantidade

                                servico_entregue.status = 'Verificado'
                        
                                db.update_data('ServicoEntregue', servico_entregue.id, servico_entregue.to_json())
                        
                        except Exception as e:
                                print(e)
                                abort(400)
                        
                        return redirect(url_for('servicos.servicos_entregues'))

        else:
                        return abort(404, 'Nenhum serviço encontrado')

@servicos_blueprint.route('/servicos-entregues/<int:serv_id>', methods=['DELETE'])
@funcionario_required
def excluir_servico_entregue(serv_id):
        user = get_user_object(session['user'])
        servico_id = int(serv_id)

        servico_entregue = db.get_servico_entregue(servico_id)
        if is_func(user) and servico_entregue.status != 'Pendente':
                return json.dumps({'error': 'Serviço já foi verificado'}), 400
        elif is_func(user) and servico_entregue.user_id != user.id:
                return json.dumps({'error': 'Serviço não foi entregue por você'}), 400
        else:
                db.remove_data('ServicoEntregue', servico_id)

        return json.dumps({'status': 'ok'}), 200
        

@servicos_blueprint.route('/meus-servicos')
@funcionario_required
def meus_servicos():
        user = get_user_object(session['user'])

        servicos = db.get_servicos_atribuidos_funcionario(user.id)
        if servicos:
                servicos.reverse()
        
        servicos_dict = dict((s.id, s.name) for s in db.get_servicos())

        clientes = dict((c['id'],c['name']) for c in db.get_table_data('cliente'))

        return render_template('meus-servicos.html',    user=user,
                                                        meus_servicos_active='active',
                                                        servicos=servicos,
                                                        servicos_dict=servicos_dict,
                                                        clientes=clientes)