import numpy as np
from . import db

def adiciona_cargo(form):
    nome = form['nome']
    
    funcs_string = form.getlist('funcionarios')
    funcs_ids = [int(f) for f in funcs_string]
    desc = form['descricao']

    data = {
        'nome' : nome,
        'descricao' : desc
    }
    
    db.insert_data('cargos', data)
    id = db.select('cargos', 'nome', '=', nome)[0]['id']

    update_funcs_cargo(funcs_ids, id)
    
def update_cargo(form, cargo_id, funcionarios_do_cargo):
    
    nome = form['nome']
    
    funcs_string = form.getlist('funcionarios')
    try:
        funcs = [int(f) for f in funcs_string]
        
        desc = form['descricao']
        
        data = {
            'nome' : nome,
            'descricao' : desc
        }

        db.update_data('cargos', cargo_id, data)    
    
        update_funcs_cargo(funcs, cargo_id, funcionarios_do_cargo)
    
    except:
        return
    
def update_funcs_cargo(funcs_ids, cargo_id, funcionarios_do_cargo=[]):
    sem_cargo_id = db.select('cargos', 'nome', '=', 'Sem Cargo')[0]['id']

    for fid in funcs_ids:
        if fid in funcionarios_do_cargo:
            funcionarios_do_cargo.remove(fid)
            
        funcionario = db.get_funcionario(fid)
        funcionario.cargo = cargo_id
        db.update_data('users', fid, funcionario.to_json())
    
    for fid in funcionarios_do_cargo:
        funcionario = db.get_funcionario(fid)
        funcionario.cargo = sem_cargo_id
        db.update_data('users', fid, funcionario.to_json())

def excluir_cargo(cargo_id):
    
    funcionarios = db.select('users', 'cargo', '=', cargo_id)
    if funcionarios:
        for funcionario in funcionarios:
            funcionario['cargo'] = 0
            db.update_data('users', funcionario['id'], funcionario)

    db.remove_data('cargos', cargo_id)
