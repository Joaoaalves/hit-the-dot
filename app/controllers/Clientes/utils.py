from app.controllers.Login.utils import get_secure_file
from . import app
import os

def save_logo_cliente(cliente_id):
    image = get_secure_file('logo', 'image')
    if image:
        image.save(os.path.join(app.config['CLIENTES_LOGO_FOLDER'] ,  str(cliente_id) + ".jpg"))