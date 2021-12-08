from firebase_admin import initialize_app
from . import *
from .utils import *

bater_ponto = Blueprint('bater_ponto', __name__,
                        template_folder='templates',
                        static_folder='static',
                        static_url_path='/BaterPonto/static/',
                        url_prefix='/bater-ponto')


@bater_ponto.route("/", methods=['GET', 'POST'])
@funcionario_required
def baterponto():
    
    user = get_user_object(session['user'])
    
    now = datetime.now()
    date = f"{now.day:02d}/{now.month:02d}/{now.year:04d}"
    # Shift
    turno = db.get_turno(date, user.id)

    if request.method == 'GET':
        
        if turno:
            print(vars(turno))
            return render_template('bater_ponto.html', 
                                                        turno_funcionario=user.turno,
                                                        turno=turno,
                                                        user=user,
                                                        bater_ponto_active='active')
            
        return render_template('bater_ponto.html',  current_status='clocked_out',
                                                    user=user,
                                                    bater_ponto_active='active')

    else:
        form = request.form
        status = form['status']
        
        if db.add_new_shift_status_on_firestore(status, user.id):   
            return redirect(url_for('bater_ponto.baterponto'))
    
        return flask.abort(400, 'Você ja bateu seu ponto!')
