from crypt import methods
from multiprocessing.sharedctypes import Value

from app.controllers.decorators import is_admin
from . import *

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