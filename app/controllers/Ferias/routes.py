from . import *

ferias_blueprint = Blueprint('ferias', __name__,
                             template_folder='templates',
                             static_folder='static',
                             static_url_path='/Ferias/static',
                             url_prefix='/ferias')

@ferias_blueprint.route('/')
@funcionario_required
def ferias():
    user = get_user_object(session['user'])
    
    return render_template('ferias.html', ferias_active='active', user=user)


@ferias_blueprint.route('/adicionar', methods=['GET', 'POST'])
@admin_required
def adicionar():
    user = get_user_object(session['user'])
    
    if request.method == 'GET':
        return render_template('adicionar-ferias.html', ferias_active='active', user=user)
    
    else:
        form = request.form
        return redirect(url_for('ferias.ferias'))
    
@ferias_blueprint.route('/editar', methods=['GET', 'POST'])
@admin_required
def editar():
    user = get_user_object()
    
    if request.method == 'GET':
        
        return render_template("editar-ferias.html", ferias_active='active', user=user)
    
    else:
        form = request.form
        return redirect(url_for('ferias.ferias'))
    

@ferias_blueprint.route('/excluir', methods=['DELETE'])
@admin_required
def excluir():
    
    form = request.form
    
    return '', 200