import numpy as np
from . import db

def get_cargo_id():
    ids = db.get_all_rows_from_firestore('Cargos', 'id')
    
    return int(np.amax(ids)) + 1


def adiciona_cargo(form):
    nome = form['nome']
    
    funcs_string = form.getlist('funcionarios')
    funcs_ids = [int(f) for f in funcs_string]
    
    desc = form['descricao']
    
    id = get_cargo_id()
    
    data = {
        'nome' : nome,
        'id' : id,
        'descricao' : desc
    }
    
    db.add_data_on_firestore('Cargos', data)
    
    update_funcs_cargo(funcs_ids, id)
    
def update_cargo(form, cargo_id, funcionarios_do_cargo):
    
    nome = form['nome']
    
    funcs_string = form.getlist('funcionarios')
    try:
        funcs = [int(f) for f in funcs_string]
        
        desc = form['descricao']
        
        data = {
            'nome' : nome,
            'funcionarios' : funcs,
            'id' : cargo_id,
            'descricao' : desc
        }
        
        db.update_info('Cargos', data, key='id', value=cargo_id)
        
        update_funcs_cargo(funcs, cargo_id, funcionarios_do_cargo)
    
    except:
        
        return
    
def update_funcs_cargo(funcs_ids, cargo_id, funcionarios_do_cargo):
    for f in funcs_ids:
        if f in funcionarios_do_cargo:
            funcionarios_do_cargo.remove(f)
            
        funcionario = db.get_funcionario(f)
        funcionario.cargo = cargo_id
        db.update_info('Users', vars(funcionario), key='id', value=f)
    
    for f in funcionarios_do_cargo:
        funcionario = db.get_funcionario(f)
        funcionario.cargo = 0
        db.update_info('Users', vars(funcionario), key='id', value=f)

def excluir_cargo(cargo_id):
    
    cargo = db.get_cargo(cargo_id)
    funcionarios = db.get_rows_from_firestore('Users', 'cargo', '==', cargo.id)
    if funcionarios:
        for funcionario in funcionarios:
            funcionario['cargo'] = 0
            db.update_info('Users', funcionario, key='id', value=funcionario['id'])

    db.remove_data_from_firestore('Cargos', 'id', cargo_id)
    

def clear_funcionarios(funcs):
    for f in funcs:
        funcionario = db.get_user('id', f)
        
        funcionario.cargo = "default"
        
        db.update_info('Users', vars(funcionario), key='id',value=f)