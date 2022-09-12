from datetime import datetime

estagiario = {
        'id': 1,
        'name': 'Estagiario',
        'email': 'estagiario@dbsweb.com.br',
        'role' : 'Estagiario',
        'cargo' : 1,
        'turno' : 6
}

funcionario = {
        'id': 2,
        'name': 'Funcionario',
        'email': 'funcionario@dbsweb.com.br',
        'role' : 'Funcionario',
        'cargo' : 2,
        'turno' : 8
}

gestor = {
        'id': 3,
        'name': 'Gestor',
        'email': 'gestor@dbsweb.com.br',
        'role' : 'Gestor',
        'cargo' : 3,
        'turno' : 8
}

admin = {
        'id': 4,
        'name': 'Admin',
        'email': 'admin@dbsweb.com.br',
        'role' : 'Admin',
        'cargo' : 4,
        'turno' : 0
}

service = {
        'name' : 'Teste',
        'tempo' : 60,
        'valor' : 100
}

servico_entregue = {
        'service_id' : 1,
        'user_id' : 1,
        'cliente_id' : 1,
        'link_trello' : 'https://trello.com/',
        'entrega' : datetime.now().date(),
        'prazo' : 1
}

atributo_servico = {
        'servico' : 1,
        'name' : 'Teste',
        'type' : 'text',
        'default_value' : 'Teste'
}

atributo_value = {
        'atributo' : 1,
        'servico_entregue' : 1,
        'value' : 'Teste'
}

cliente = {
        'name' : 'Teste',
}