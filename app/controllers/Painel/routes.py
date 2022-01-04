from . import *
from .utils import *

painel_blueprint = Blueprint('painel', __name__,
                             template_folder='templates',
                             static_folder='static',
                             static_url_path='/Painel/static')

@painel_blueprint.route('/painel')
@funcionario_required
def painel():
    user = get_user_object(session['user'])
    if 'range' in request.args and request.args.get('range') != '':
        try:
            
            s_date, e_date = request.args.get('range').split(' - ')
            start_date = datetime.strptime(s_date, '%d/%m/%Y')
            end_date = datetime.strptime(e_date, '%d/%m/%Y')
            
            if start_date > end_date:
                raise Exception('Date Range inválido')
            
        except Exception as e:
            now = datetime.now()
            start_date = datetime(year=now.year, month=now.month, day=1)
            end_date = datetime(year=now.year, month=now.month, day=now.day - 1)
                    
    else:
        
        now = datetime.now()
        start_date = datetime(year=now.year, month=now.month, day=1)
        end_date = datetime(year=now.year, month=now.month, day=now.day - 1)
        
    if is_admin(user):
        if not 'funcionario' in request.args or request.args.get('funcionario') == '':
            return render_painel_admin(user, start_date, end_date)
        
        else:
            try:
                func_id = int(request.args.get('funcionario'))
                return render_filtered_painel_admin(user, start_date, end_date, func_id)
            
            except Exception as e:
                return flask.abort(404, e)
    else:
        turnos = db.get_turnos_timedelta(user.id,start_date, end_date)
        user.set_turnos(turnos)
        return render_painel_func(user,start_date, end_date)