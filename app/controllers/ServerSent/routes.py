from . import *

server_sent = Blueprint('sse', __name__)

@server_sent.route('/listar-funcionarios/status')
def get_sessions():
    redis_con = redis.Redis(host='localhost', port=6379, db=0)

    @stream_with_context
    def generate():
        sessions = dict()
        
        try:
            session_ids = [session_id.decode('utf-8') for session_id in redis_con.keys('session:*')]
            for session_id in session_ids:
                
<<<<<<< HEAD
                uid = int(session_id.replace('session:', ''))
=======
                uid = session_id.replace('session:', '')
>>>>>>> d56c787985a3d6c5f15ec6cd8faafec76fe16aca

                sessions[uid] = redis_con.get(session_id).decode('utf-8')

        except Exception as e:
            print(e)

            
        _data = json.dumps(sessions)

        yield f"id: 1\ndata: {_data}\nevent: sessions\n\nretry: 10000\n\n"

    return Response(generate(), mimetype='text/event-stream')
