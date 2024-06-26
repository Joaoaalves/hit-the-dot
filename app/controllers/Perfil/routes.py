from . import *
from .utils import *

perfil_blueprint = Blueprint('perfil', __name__,
                             template_folder='templates',
                             static_folder='static',
                             static_url_path='Perfil/static',
                             url_prefix='/perfil')

@perfil_blueprint.route('/')
@funcionario_required
def perfil():
    #
    # Perfil do funcionario
    #

    user = get_user_object(session['user'])
    if is_admin(user):
        return render_template('perfil-admin.html', user=user)
    
    else:
        funcionario = db.get_funcionario(user.id)
        
        turnos = [t for t in db.get_turnos() if t.user_id == user.id]
        funcionario.set_turnos(turnos)
        
        cargo = db.get_cargo(funcionario.cargo)

        return render_template('perfil.html', user=user,
                                                cargo=cargo)
            

@perfil_blueprint.route('/editar', methods=['GET', 'POST'])
@funcionario_required
def editar_perfil():
    #
    # Editar perfil do funcionario
    # GET: Return the funcionario edit page
    # POST: Update the funcionario
    #
    
    user = Funcionario(session['user'])
    
    if request.method == 'GET':
        cargos = db.get_cargos()
        
        return render_template('editar_perfil.html', user=user,
                                                    cargos=cargos)

    else:
        
        editar_perfil(request.form, user)
        
        return redirect(url_for('perfil.perfil'))