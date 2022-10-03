from app.controllers.decorators import funcionario_required
from . import *
from .utils import *

login = Blueprint("login", __name__,
                template_folder="templates",
                static_folder="static",
                static_url_path="/Login/static")


@login.route("/login", methods=['GET', 'POST'])
def log_in():
    #
    # This function handles the login process
    # GET: returns the login page
    # POST: checks the credentials and redirects to the home page
    #
    if request.method == 'GET':
        if 'user' in session:
            return redirect(url_for('painel.painel'))

        return render_template("login.html")

    else:
        if recaptcha.verify():
            try:
        
                form = request.form
                email = form['email']
                senha = form['password']
                
                # Throw exception on login fail
                db.login(email, senha)
                
                # Get the user info from db on login success
                user = db.get_user_by_email(email)
                
                flask.session['user'] = user.to_json()
                flask.session['user']['role'] = user.__class__.__name__

                users.append(user)
                
            except Exception as e:
                app.logger.warning('Erro no login: ' + str(e))
                ip_ban.add()
                return  render_template(
                    'login.html',
                    erro='Email ou senha incorreto(s)!'
                ), 401
        else:
            ip_ban.add()
            return render_template('login.html',
                                   erro='Recaptcha inválido!'), 401
            

        return redirect(url_for('painel.painel'))


@login.route("/logout", methods=['GET'])
@login_required
def logout():
    #
    # Logout Route
    #
    try:

        
        clear_session()
        return redirect("/login")

    except Exception as e:
        
        app.logger.critical('Erro no logout: ' + str(e))
        return redirect("/login")

@login.route('/registrar', methods=['GET', 'POST'])
@admin_required
def registrar():
    #
    # Signup Route
    # GET: Show Signup Page
    # POST: Try to signup a new user
    #
    cargos = db.get_cargos()

    if request.method == 'GET':
        return render_template('signup.html',
                               cargos=cargos)

    else:

        form = request.form

        try:
            cadastrar(form)            
        
            return render_template('signup.html', success='Cadastrado com sucesso!')

        
        except Exception as e:
            app.logger.warning('Erro no registro: ' + str(e))
            return render_template('signup.html', error=e, cargos=cargos)
        
@login.route("/recuperar-senha", methods=['GET', 'POST'])
def recuperar_senha():
    #
    # Remembers the user's password by sending an email
    # POST: Sends an email with a link to reset the password.
    # GET: Show the reset password page.
    #
    
    if not 'user' in session:
    
        if request.method == 'GET':
            return render_template("recuperar_senha.html")

        else:

            try:
                email = request.form['email']
                db.auth.send_password_reset_email(email)

            except Exception as e:

                app.logger.warning('Erro recuperação de senha: ' + str(e))

            return flask.redirect("/login")
        
@login.route('/alterar-senha', methods=['POST'])
@funcionario_required
def alterar_senha():
    #
    # Change the user's password
    # POST: Change the user's password
    #
    if 'user' in session:
        try:
            email = request.form['email']
            db.auth.send_password_reset_email(email)
            
            return '',200
        except Exception as e:
            app.logger.warning('Erro de alteração de senha: ' + str(e))
            return '',200