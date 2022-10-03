from . import *
from .utils import *

push_blueprint = Blueprint('push', __name__, url_prefix='/api')

@push_blueprint.route('/push-subscriptions', methods=['POST'])
def create_subscription():
        #
        # Create a new push subscription
        #
        
        user = session['user']['id']
        data = request.get_json()['subscription_json']
        db.insert_push_endpoint(data, user)
        return {
                        'status' : "success"
                }, 200