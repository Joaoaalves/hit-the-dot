from . import *

SUCCESS = 200
REDIRECTION = 302
NOT_PERMITED = 401
NOT_FOUND = 404
NOT_ALLOWED = 405

def test_get_servicos_entregues_by_estagiario(test_client):
    #
    # Test the get_servicos_entregues_by_estagiario function
    #

    with test_client.session_transaction() as sess:
        sess['user'] = estagiario
        
    #
    # Get the servicos entregues by estagiario
    #
    response = test_client.get('/meus-servicos')
    assert response.status_code == SUCCESS

def test_get_servicos_entregues_by_funcionario(test_client):
    #
    # Test the get_Servicos_entregues_by_funcionario function
    #

    with test_client.session_transaction() as sess:
        sess['user'] = funcionario
        
    #
    # Get the servicos entregues by funcionario
    #
    response = test_client.get('/meus-servicos')
    assert response.status_code == SUCCESS

def test_get_servicos_entregues_by_gestor(test_client):
    #
    # Test the get_servicos_entregues_by_gestor function
    #

    with test_client.session_transaction() as sess:
        sess['user'] = gestor
        
    #
    # Get the servicos entregues by gestor
    #
    response = test_client.get('/meus-servicos')
    assert response.status_code == SUCCESS

def test_criar_servico(test_client):
    #
    # Test creation of a service
    #

    with test_client.session_transaction() as sess:
        sess['user'] = admin

    response = test_client.post('/servicos/criar', data=dict(name='teste', tempo=60, valor=100))
    assert response.status_code == REDIRECTION

def test_estagiario_privileges_on_services(test_client):
    #
    # Test the estagiario_privileges_on_services function
    #

    with test_client.session_transaction() as sess:
        sess['user'] = estagiario
        
    #
    # Get the servicos entregues by estagiario
    #
    
    response = test_client.get('/servicos')
    assert response.status_code == NOT_PERMITED

    response = test_client.post('/servicos')
    assert response.status_code == NOT_ALLOWED

    response = test_client.post('/servicos/pesquisar', data=dict(service_name='teste'))
    assert response.status_code == SUCCESS

    response = test_client.get('servicos/pesquisar')
    assert response.status_code == NOT_ALLOWED

    response = test_client.get('/servicos/criar', data=dict(name='teste', tempo=60, valor=100))
    assert response.status_code == NOT_PERMITED

    response = test_client.post('/servicos/criar')
    assert response.status_code == NOT_PERMITED

    response = test_client.get('/servicos/entregar')
    assert response.status_code == SUCCESS

    response = test_client.post('/servicos/entregar', data=dict(servico=1, cliente=1, trello='https://trello.com/'))
    assert response.status_code == REDIRECTION

def test_funcionario_privileges_on_services(test_client):
    #
    # Test the funcionario_privileges_on_services function
    #

    with test_client.session_transaction() as sess:
        sess['user'] = funcionario
    
    response = test_client.get('/servicos')
    assert response.status_code == NOT_PERMITED

    response = test_client.post('/servicos')
    assert response.status_code == NOT_ALLOWED

    response = test_client.post('/servicos/pesquisar', data=dict(service_name='teste'))
    assert response.status_code == SUCCESS

    response = test_client.get('servicos/pesquisar')
    assert response.status_code == NOT_ALLOWED

    response = test_client.get('/servicos/criar', data=dict(name='teste', tempo=60, valor=100))
    assert response.status_code == NOT_PERMITED

    response = test_client.post('/servicos/criar')
    assert response.status_code == NOT_PERMITED

    response = test_client.get('/servicos/entregar')
    assert response.status_code == SUCCESS

    response = test_client.post('/servicos/entregar', data=dict(servico=1, cliente=1, trello='https://trello.com/'))
    assert response.status_code == REDIRECTION

def test_gestor_privileges_on_services(test_client):
    #
    # Test the gestor_privileges_on_services function
    #

    with test_client.session_transaction() as sess:
        sess['user'] = gestor
    
    response = test_client.get('/servicos')
    assert response.status_code == SUCCESS

    response = test_client.post('/servicos')
    assert response.status_code == NOT_ALLOWED

    response = test_client.post('/servicos/pesquisar', data=dict(service_name='teste'))
    assert response.status_code == SUCCESS

    response = test_client.get('servicos/pesquisar')
    assert response.status_code == NOT_ALLOWED

    response = test_client.get('/servicos/criar')
    assert response.status_code == SUCCESS

    response = test_client.post('/servicos/criar', data=dict(name='teste', tempo=60, valor=100))
    assert response.status_code == REDIRECTION

    response = test_client.get('/servicos/entregar')
    assert response.status_code == SUCCESS

    response = test_client.post('/servicos/entregar', data=dict(servico=1, cliente=1, trello='https://trello.com/'))
    assert response.status_code == REDIRECTION


def test_services(test_client):

    with test_client.session_transaction() as sess:
        sess['user'] = admin

    response = test_client.post('/servicos/criar', data=service)
    assert response.status_code == REDIRECTION

    response = test_client.get('/servicos')
    assert response.status_code == SUCCESS
    assert b'teste' in response.data

    response = test_client.post('/servicos/pesquisar', data=dict(service_name='teste'))
    assert response.status_code == SUCCESS

    response = test_client.get('servicos/pesquisar')
    assert response.status_code == NOT_ALLOWED

    response = test_client.get('/servicos-entregues')
    assert response.status_code == SUCCESS
