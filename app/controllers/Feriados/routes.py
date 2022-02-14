from .utils import *
from . import *

feriado_blueprint = Blueprint('feriado', __name__,
                                template_folder='templates',
                                static_folder='static',
                                static_url_path='/Feriado/static',)

@feriado_blueprint.route('/feriados')
@funcionario_required
def feriados():
    user = get_user_object(session['user'])
    all_feriados = db.get_feriados()
    feriados = list()
    
    if 'mes' in request.args and request.args.get('mes') != '':
        try:
            ano, mes = request.args.get('mes').split('-')

            for f in all_feriados:
                if f.repete and f.mes == int(mes):
                    feriados.append(f)
                else:
                    if f.mes == int(mes) and f.ano == int(ano):
                        feriados.append(f)
        except:
            return abort(400, 'Mês inválido')
                    
    else:
        feriados = all_feriados
        
    return render_template('feriados.html', feriados=feriados, 
                                            user=user,
                                            feriados_active='active')

@feriado_blueprint.route('/editar-feriado/<int:feriado_id>', methods=['GET', 'POST'])
@admin_required
def editar_feriado(feriado_id):
    
    user = get_user_object(session['user'])
    feriado = db.get_feriado(feriado_id)

    if request.method == 'GET':
        
        return render_template('editar_feriado.html', user=user, 
                                                    feriado=feriado,
                                                    feriados_active='active')
    
    if request.method == 'POST':
        
        form = dict(request.form)
        
        edit_feriado(form, feriado)
        
        return redirect(url_for('feriado.feriados'))
    
    
@feriado_blueprint.route('/excluir-feriado', methods=['DELETE'])
@admin_required
def excluir_feriado():
    try:
        feriado_id = int(request.form['id'])
        
        db.remove_data('feriados', feriado_id)
        
        return '',200

    except:
        return '',400
    
    
@feriado_blueprint.route('/adicionar-feriado', methods=['GET', 'POST'])
@admin_required
def adicionar_feriado():
    user = get_user_object(session['user'])
    
    if request.method == 'GET':
        feriado_list = [f.get_html_date() for f in db.get_feriados()]
        return render_template('adicionar_feriado.html', user=user,
                                                        feriados=feriado_list,
                                                        feriados_active='active')
    
    if request.method == 'POST':
        
        form = dict(request.form)
        
        try:
            create_feriado(form)
        
        except Exception as e:
            
            return abort(400, e)
        
        return '', 200