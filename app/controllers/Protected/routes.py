from . import *

protected = Blueprint("protected", __name__, url_prefix="/protected")

@protected.route("/<path:filename>")
@special_requirement
def protected_file(filename):
    #
    #    Look for the file in the protected folder, if exists, return it
    # 
    try:
        return flask.send_from_directory(
                        os.path.join(app.instance_path, ''), filename)

    except Exception as e:
        print(e)
        app.logger.warning(e)
        return 'Failed to load the image', 404