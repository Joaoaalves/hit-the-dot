from flask.helpers import url_for
from . import *

main = Blueprint("main", __name__,
                template_folder="templates",
                static_folder="static",
                static_url_path="/Main/static/")

@main.route("/")
def index():
    #
    # Home Page
    #

    if 'user' in session:
        return flask.redirect(url_for('painel.painel'))
    else:
        return flask.redirect(url_for('login.log_in'))