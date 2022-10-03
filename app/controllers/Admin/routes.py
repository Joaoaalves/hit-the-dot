from . import *
from .utils import *

admin_blueprint = Blueprint('admin', __name__,
                            template_folder='templates',
                            static_folder='static',
                            static_url_path='/Admin/static')


@admin_blueprint.route('/listar-funcionarios')
@admin_required
def listar_funcionarios():
    #
    # List all the funcionarios
    #

    try:
        user = get_user_object(session['user'])

        funcionarios = db.get_all_funcionarios()
        cargos = db.get_cargos()

        if request.args.get('cargo'):
            funcionarios = filtra_funcionario_por_cargo(
                funcionarios, request.args.get('cargo'))

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


@admin_blueprint.route("/editar-funcionario/<int:user_id>", methods=['GET', 'POST'])
@admin_required
def editar_funcionario(user_id):
    #
    # Edit a funcionario
    # GET: Return the funcionario edit page
    # POST: Update the funcionario
    #

    user = get_user_object(session['user'])
    funcionario = db.get_funcionario(user_id)
    cargos = db.get_cargos()

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


@admin_blueprint.route('/status-funcionario/<int:user_id>', methods=['POST'])
@admin_required
def status_funcionario(user_id):

    #
    # Change the funcionario status
    #

    funcionario = db.get_funcionario(user_id)
    if funcionario:
        funcionario.is_active = request.form['status'] == 'true'
        db.update_data('Users', funcionario.id, vars(funcionario))
        return '', 200

    return abort(404, 'Funcionario não encontrado!')


@admin_blueprint.route('/funcionario/<int:user_id>', methods=['GET'])
@admin_required
def ver_funcionario(user_id):
    #
    # Show funcionario
    #

    user = get_user_object(session['user'])

    funcionario = db.get_funcionario(user_id)

    cargo = db.get_cargo(funcionario.cargo)

    return render_template('funcionario.html', user=user,
                           funcionario=funcionario,
                           cargo=cargo,
                           funcionarios_active='active')
