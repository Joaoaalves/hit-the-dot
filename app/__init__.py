from flask import Flask, render_template, session, redirect, url_for
import logging
from flask_ipban import IpBan
from flask_mail import Mail
from flask_wtf import CSRFProtect
import os, sys
from apscheduler.schedulers.background import BackgroundScheduler

from app.models.database import Database

# Rotina do verificador de turnos
rotina_turnos = BackgroundScheduler(daemon=True)

# App
if not 'instance_path' in os.environ:
    instance_path = os.getcwd() + '/app/protected/'
else:
    instance_path = os.environ['instance_path']
app = Flask(__name__, instance_path=instance_path)

# Firebase Admin Config
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'config/firebase.json'

# Mail
mail = Mail()

# CSRF Protection
csrf = CSRFProtect(app)

# Users
users = list()
invalid_sessions = list()

# Logs
#logging.basicConfig(filename='debug.log', level=logging.INFO)
#logging.disable(logging.DEBUG)
#  logging.disable(logging.INFO)


# IP Ban
#ip_ban = IpBan(ban_count=5)
#ip_ban.init_app(app)


try:

    # Setup DB
    db = Database()
    
    # Key Flask
    with open('config/flask.key', 'r') as f:
        app.secret_key = f.readline()

    
except Exception as e:
    print(e)

    exit()

def create_app():
    # App configs
    app.config.from_object("config")
    
    from app.rotinas import check_turnos
    
    # from app.rotinas import contabiliza_turnos_semana
    # from app.rotinas import contabiliza_turnos_mes
    
    # Scheduler Diária Turno para fechar turnos abertos
    rotina_turnos.add_job(check_turnos, 'cron', hour=23, minute=59)
    
    rotina_turnos.start()

    # Mail configs
    with open('config/mail_creds.txt', 'r') as f:
        app.config['MAIL_USERNAME'] = f.readline()[:-1] # Removes \n char
        app.config['MAIL_PASSWORD'] = f.readline()

    mail.init_app(app)

    from app.controllers.Main.routes import main
    app.register_blueprint(main) 

    from app.controllers.Login.routes import login
    app.register_blueprint(login)

    from app.controllers.BaterPonto.routes import bater_ponto
    app.register_blueprint(bater_ponto)

    from app.controllers.Turnos.routes import turnos_blueprint
    app.register_blueprint(turnos_blueprint)

    from app.controllers.Admin.routes import admin_blueprint
    app.register_blueprint(admin_blueprint)
    
    from app.controllers.Feriados.routes import feriado_blueprint
    app.register_blueprint(feriado_blueprint)
    
    from app.controllers.Perfil.routes import perfil_blueprint
    app.register_blueprint(perfil_blueprint)
    
    from app.controllers.Cargos.routes import cargos_blueprint
    app.register_blueprint(cargos_blueprint)
    
    from app.controllers.Painel.routes import painel_blueprint
    app.register_blueprint(painel_blueprint)
    
    from app.controllers.Protected.routes import protected
    app.register_blueprint(protected)
    
    from app.controllers.Tarefas.routes import tarefas_blueprint
    app.register_blueprint(tarefas_blueprint)
    
    from app.controllers.Ferias.routes import ferias_blueprint
    app.register_blueprint(ferias_blueprint)
    
    from app.controllers.Faltas.routes import faltas_blueprint
    app.register_blueprint(faltas_blueprint)
    
    @app.errorhandler(404)
    @app.errorhandler(500)
    def page_not_found(e):
        if 'user' in session:
            user = session['user']
            return render_template('404.html', user=user, error=e), 404
        return redirect(url_for('login.log_in'))

    @app.errorhandler(401)
    def permission_error(e):
        return redirect(url_for('login.log_in'))
    
    @app.errorhandler(400)
    def unknown_error(e):
        if 'user' in session:
            user = session['user']
            return render_template('404.html', user=user, error=e), 404
        return redirect(url_for('login.log_in'))
    return app
