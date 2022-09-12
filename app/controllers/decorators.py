from flask import redirect, url_for, session, abort, request
from functools import wraps
from app import app

from app.models.estagiario import Estagiario
from app.models.funcionario import Funcionario
from app.models.gestor import Gestor
from app.models.admin import Admin

EST_PRIVILEGE = 2
FUNC_PRIVILEGE = 3
GESTOR_PRIVILEGE = 4
ADMIN_PRIVILEGE = 5

def is_admin(user):
    #
    # Verify if the user is Admin
    #
    return user.get_privilege() == ADMIN_PRIVILEGE

def is_gestor(user):
    #
    # Verify if the user is logged in and is Gestor
    #

    return user.get_privilege() >= GESTOR_PRIVILEGE

def is_func(user):
    #
    # Verify if the user is Funcionario
    #
    return user.get_privilege() >= FUNC_PRIVILEGE

def is_estagiario(user):
    #
    # Verify if the user is Estagiario
    #
    return user.get_privilege() >= EST_PRIVILEGE

def get_user_object(user):
    #
    # Get the user object from the session
    #
    if user['role'] == 'Estagiario':
        return Estagiario(user)
    
    if user['role'] == 'Funcionario':
        return Funcionario(user)

    if user['role'] == 'Admin':
        return Admin(user)

    if user['role'] == 'Gestor':
        return Gestor(user)

    return None

def login_required(f):
    #
    #    Decorator that verifies if the user is logged in
    #
    @wraps(f)
    def verifica_login(*args, **kwargs):
        if not 'user' in session:
            return redirect(url_for('login.log_in'))
        
        return f(*args, **kwargs)
    
    return verifica_login

def funcionario_required(f):
    #
    #   Decorator that verify if the user is a funcionario
    #

    @wraps(f)
    @login_required
    def verifica_funcionario(*args, **kwargs):

        user = get_user_object(session['user'])

        if is_estagiario(user):
            return f(*args, **kwargs)

        else:
            return abort(401, "Você não tem permissão para acessar essa página")
        
    return verifica_funcionario

def gestor_required(f):
    #
    #   Decorator that verify if the user is a funcionario
    #

    @wraps(f)
    @login_required
    def verifica_funcionario(*args, **kwargs):

        user = get_user_object(session['user'])
        print(user)
        if is_gestor(user):
            return f(*args, **kwargs)

        else:
            return abort(401, "Você não tem permissão para acessar essa página")
        
    return verifica_funcionario

def special_requirement(f):
    #
    #   Decorator to check if user is allowed to access the file
    #   Only if the user is admin or is the owner of the file
    #

    @wraps(f)
    @login_required
    def wrap(*args, **kwargs):

        user = get_user_object(session['user'])

        if is_admin(user) or str(user.id) in kwargs['filename']:
            return f(*args, **kwargs)
        
        else:
            return redirect(url_for('main.index'))

    return wrap
            

def admin_required(f):
    #
    #   Decorator that verify if the user is an admin
    #

    @wraps(f)
    @login_required
    def verifica_admin(*args, **kwargs):
        
        user = get_user_object(session['user'])
        if is_admin(user):
            return f(*args, **kwargs)
        
        else:
            return abort(401, "Você não tem permissão para acessar essa página")


    return verifica_admin

def block_cross_site_requests(f = None):
    #
    #   Decorator that block cross site requests in GET routes
    #
    
    @wraps(f)

    def verifica_csrf(*args, **kwargs):
        origin = request.headers.get('Sec-Fetch-Site')

        if  origin != 'same-origin':
                return abort(400, "Cross Site Requests Are Not Allowed!")

        return f(*args, **kwargs)

    return verifica_csrf


# Transport these functions to jinja
app.jinja_env.globals.update(is_admin=is_admin)
app.jinja_env.globals.update(is_func=is_func)
app.jinja_env.globals.update(is_gestor=is_gestor)
app.jinja_env.globals.update(is_estagiario=is_estagiario)