from . import *
from .utils import *

admin_blueprint = Blueprint('admin', __name__,
                template_folder='templates',
                static_folder='static',
                static_url_path='/Admin/static')


@admin_blueprint.route('/listar-funcionarios')
@admin_required
def listar_funcionarios():

    try:
        user = get_user_object(session['user'])
        
        funcionarios = db.get_all_funcionarios()
        
        cargos = db.get_cargos()
        
        if request.args.get('cargo'):
            cargo_nome = request.args.get('cargo')
            for cargo in cargos:
                if cargo.name == cargo_nome:
                    funcionarios = filtra_funcionarios(funcionarios, lambda x: x.cargo == cargo.id)
    
        if funcionarios:
            return render_template('listar_funcionarios.html', funcionarios=funcionarios,
                                                                cargos=cargos,
                                                                user=user,
                                                                funcionarios_active='active')
        
    
        return render_template('listar_funcionarios.html', user=user,
                                                        funcionarios_active='active',
                                                        cargos=cargos)
    
    except Exception as e:
        
        return abort(400, e)

@admin_blueprint.route("/editar-funcionario/<int:func_id>", methods=['GET', 'POST'])
@admin_required
def editar_funcionario(func_id):
    user = get_user_object(session['user'])
    funcionario = db .get_funcionario(func_id)
    cargos = get_cargos()
    
    if funcionario:
        if request.method == 'GET':
            
            return render_template('editar_funcionario.html', user=user, 
                                                    funcionario=funcionario, 
                                                    cargos=cargos,
                                                     funcionarios_active='active')
        
        else:
            
            form = request.form
            update_func_info(form, funcionario)
            
            return redirect(url_for('admin.listar_funcionarios'))
    
    return abort(404, 'Funcionario não encontrado!')

@admin_blueprint.route("/excluir-usuario", methods=['DELETE'])
@admin_required
def excluir_usuario():
    #
    #Route to delete a user from system
    #
    
    func_id = int(flask.request.form['uid'])
    
    excluir_funcionario(func_id)
    
    return '', 200


    # return flask.abort(400, str(status))

@admin_blueprint.route('/funcionario/<int:func_id>', methods=['GET'])
@admin_required
def ver_funcionario(func_id):
    user = get_user_object(session['user'])
    
    funcionario = db.get_funcionario(func_id)

    cargo = db.get_cargo(funcionario.cargo)
        
    return render_template('funcionario.html', user=user,
                                                funcionario=funcionario,
                                                cargo=cargo,
                                                funcionarios_active='active')
    