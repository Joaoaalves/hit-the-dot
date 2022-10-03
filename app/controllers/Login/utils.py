from . import users, flask, invalid_sessions, app, PasswordPolicy, PasswordStats
from . import re, db, random, request, Popen, os, get_user_object, session

import phonenumbers


policy = PasswordPolicy.from_names(
    length=8,  # min length: 8
    uppercase=1,  # need min. 1 uppercase letters
    numbers=1,  # need min. 1 digits
    special=1,  # need min. 1 special characters
    nonletters=1,  # need min. 1 non-letter characters (digits, specials, anything)
)

email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

def clear_session():
    #
    #    Clear the session and the invalid_sessions list
    #
    current_user = get_user_object(session['user'])
        
    for i in range(len(users)):
        if users[i].id == current_user.id:
            users.pop(i)
            break    
        
    invalid_sessions.append(current_user.id)

    flask.session.clear()

    app.logger.warning(f"{current_user['name']} logged out ({flask.request.remote_addr})")

def weak_password(password):
    #
    #   Verify if the password is strong enough
    #

    stats = PasswordStats(password)
    password_strength = stats.strength()

    if policy.test(password) != []:
        raise Exception("Não cumpriu os requisitos de senha")
    
    elif password_strength < 0.4:
        raise Exception("Senha fraca, tente aumentar o tamanho e adicionar caracteres especiais")

def verify_entrys(nome, email, password, pass_confirm, image):
    #
    #   Verify if the signup entrys are valid
    #
    if image == None:
        raise Exception("Envie uma imagem válida! (JPG ou PNG)")
        
    if  len(nome) < 8:
        raise Exception("Nome muito curto!")

    if not re.match(email_regex, email):
        raise Exception("Este não é um email válido!")

    if pass_confirm != password:
        raise Exception("Confirmação de senha INCORRETA!")

    weak_password(password)


def cadastrar(form):
    #
    #  Create a new user
    #
    role = 'Funcionario'
    email = form['email']
    nome = form['name']
    password = form['password']
    password_confirm = form['password-confirm']
    turno = int(form['turno'])
    dias_trabalho = int(form['dias_trabalho'])
    cargo_id = int(form['cargo'])
    
    if 'celular' in form and is_a_valid_phone(form['celular']):
        celular = international_phone(form['celular'])
        
    else:
        celular = None
        
    image = get_secure_file("profile_image", 'image')
    
    
    # Throw exceptions on fails
    verify_entrys(nome, email, password, password_confirm, image)
    
    user_data = {
        'email' : email,
        'name' : nome,
        'password' : password,
        'role' : role,
        'cargo' : cargo_id,
        'dias_trabalho' : dias_trabalho,
        'turno' : int(turno),
        'celular' : celular,
        'is_active' : True
    }
    
    if create_user( user_data, image):    
        return
    
    raise Exception('Falha ao criar conta')

def create_user(data, image):
    #
    # Create user on db and save the profile image on protected/ folder
    #

    if db.create_user(data):
        user = db.select('Users', 'email', '=', data['email'])[0]
        save_profile_image(image, user['id'])
        return True
    
    return False
def get_secure_file(filename, type):
    #
    #    Verify if the file is really an image to prevent the upload of malicious files
    #    (Just a simple check, a more complex one should be implemented)
    #

    image_format = ['image/jpg', 'image/png', 'image/jpeg']
    permited_ext = ['png', 'jpg', 'jpeg']

    f = request.files[filename]
    
    name = f.filename

    file_extension = name[-3:]
    
    try:
        if type == 'image' and file_extension in permited_ext:
            if f.content_type in image_format:
                return f

        return None
        
    except:
        return None
    
def save_profile_image(image, user_id):
    #
    #   Save the profile image on protected/ folder
    #

    os.makedirs("app/protected/" + str(user_id), exist_ok=True)
    image.save(os.path.join(app.config['PROFILE_UPLOAD_FOLDER'] + str(user_id),  "profile.jpg"))

def is_a_valid_phone(number):
    phone = phonenumbers.parse(number, region='BR')
    return phonenumbers.is_valid_number(phone)

def international_phone(number):
    phone = phonenumbers.parse(number, region='BR')
    return phonenumbers.format_number(phone, phonenumbers.PhoneNumberFormat.INTERNATIONAL)

def national_phone(number):
    phone = phonenumbers.parse(number, region='BR')
    return phonenumbers.format_number(phone, phonenumbers.PhoneNumberFormat.NATIONAL)

app.jinja_env.globals.update(national_phone=national_phone)
app.jinja_env.globals.update(international_phone=international_phone)