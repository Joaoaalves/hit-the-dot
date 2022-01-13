from . import *

server_sent = Blueprint('sse', __name__)

funcs_ids = [f.id for f in db.get_all_funcionarios()]

@server_sent.route('/listar-funcionarios/status')
def get_sessions():
    """
    redis_con = redis.Redis(host='localhost', port=6379, db=0)
    
    @stream_with_context
    def generate():
        sessions = dict()
        global func_ids

        for uid in funcs_ids:
            session = redis_con.get(f"session:{uid}")
            if type(session) == bytes:
                sessions[uid] = session.decode('utf-8')
            else:
                sessions[uid] = str(session)
        _data = json.dumps(sessions)

        yield f"id: 1\ndata: {_data}\nevent: sessions\n\nretry: 10000\n\n"
    """
    @stream_with_context
    def generate():
        data = {1298: "true", 2920: "true", 5206: "true", 3264: "true",5395: "true", 4681: "true", 5929: "true"}
        yield f'id: 1\ndata: {data}\nevent: sessions\n\nretry: 10000\n\n'

    return Response(generate(), mimetype='text/event-stream')
