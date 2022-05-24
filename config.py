DEBUG = True
# File Uploads
UPLOAD_EXTENSIONS = ['.jpg', '.png'] # Formatos permitidos
MAX_CONTENT_LENGTH = 1024 * 1024 * 8 # Tamanho maximo de 8MB

# Path of Profile Pictures Folder
PROFILE_UPLOAD_FOLDER = 'app/protected/'


# Fill with recaptcha keys
RECAPTCHA_SITE_KEY = ''
RECAPTCHA_SECRET_KEY = ''

# Anti XSS Configs
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE='Strict'


# Mail Config
MAIL_SERVER = 'smtp.gmail.com'
MAIL_USE_SSL = True
MAIL_PORT = 465
MAIL_DEBUG = True

BROKER_URL = 'redis://localhost:6379'
RESULT_BACKEND = 'redis://localhost:6379'     