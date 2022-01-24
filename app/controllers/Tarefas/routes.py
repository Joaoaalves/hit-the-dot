from app.controllers.decorators import is_admin
from . import *

tarefas_blueprint = Blueprint('tarefas', __name__,
                                        template_folder='templates',
                                        static_folder='static',
                                        static_url_path='/Tarefas/static')

@tarefas_blueprint.route('/listar-tarefas')
@funcionario_required
def tarefas():
    
    user = get_user_object(session['user'])
    
    if is_admin(user):
        relatorios = db.get_all_relatorios()
        
        funcionarios = db.get_all_funcionarios()
        
        func_dict = {funcionario.id : funcionario.name for funcionario in funcionarios}
        
        return render_template('tarefas.html', user=user,
                                            relatorios=relatorios,
                                            func_dict=func_dict)
    else:
        relatorios = db.get_all_relatorios(user.id)
        
    return render_template('tarefas.html', user=user,
                                            relatorios=relatorios)
    

@tarefas_blueprint.route('/tarefa/<int:tarefa_id>')
@funcionario_required
def tarefa(tarefa_id):
    
    user = get_user_object(session['user'])
    
    relatorio = db.get_relatorio(tarefa_id)
    
    if relatorio:
        
        if is_admin(user) or tarefa.func_id == user.id:
            funcionario = db.get_funcionario(relatorio.func_id)
            return render_template('tarefa.html', user=user,
                                                relatorio=relatorio,
                                                funcionario=funcionario)
            
        else:
            
            return abort(401, 'Você não tem permissão para acessar esta página!')
        
    return abort(404, 'Tarefa com este id não foi encontrada!')


# @tarefas_blueprint.route('/criar-tarefa')
# @admin_required
# def criar_tarefa():
#     user = get_user_object(session['user'])
    
#     funcionarios = db.get_all_funcionarios()
    
