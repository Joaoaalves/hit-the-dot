from app.controllers.Login.utils import get_secure_file
from . import app, db
import os

def save_logo_cliente(cliente_id):
    image = get_secure_file('logo', 'image')
    if image:
        image.save(os.path.join(app.config['CLIENTES_LOGO_FOLDER'] ,  str(cliente_id) + ".jpg"))

def create_cliente(form):
    # Create cliente
    name = form['name']
    
    db.insert_data('Clientes', {'name' : name})

    cliente_criado = db.select('Clientes', 'name', '=', name)[0]
    
    save_logo_cliente(cliente_criado['id'])