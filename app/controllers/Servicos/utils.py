from . import app
import os

def save_logo_cliente(image, cliente_id):

    image.save(os.path.join(app.config['CLIENTES_LOGO_FOLDER'] ,  str(cliente_id) + ".jpg"))