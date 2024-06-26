from . import *
from .utils import *

painel_blueprint = Blueprint('painel', __name__,
                             template_folder='templates',
                             static_folder='static',
                             static_url_path='/Painel/static')

@painel_blueprint.route('/painel')
@funcionario_required
def painel():
    #
    # Painel do funcionario
    #
    
    user = get_user_object(session['user'])
    start_date, end_date = get_start_end_date(request.args)
    
    if is_admin(user):
        if not 'funcionario' in request.args or request.args.get('funcionario') == '':
            return render_painel_admin(user, start_date, end_date)
        
        else:
            try:
                user_id = int(request.args.get('funcionario'))
                
                return render_filtered_painel_admin(start_date, end_date, user_id)
            
            # Func not found
            except Exception as e:
                if(type(e) == AttributeError):
                    return flask.abort(404, 'Funcionário não encontrado')

                return flask.abort(404, e)
    else:
        
        return render_painel_func(user,start_date, end_date)