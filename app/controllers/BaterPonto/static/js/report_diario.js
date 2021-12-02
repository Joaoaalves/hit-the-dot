function adicionar_campo(){
    var input = document.createElement("input");

    input.setAttribute('type', 'text');
    input.setAttribute('placeholder', 'Task')
    input.setAttribute('name', 'task');
    input.setAttribute('class', 'task form-control form-control-sm');
    input.required = true;

    parent = document.getElementById('tasks');
    parent.appendChild(input);
}

function remover_campo(){
    var inputs = document.getElementsByClassName('task');
    
    if(inputs.length > 1){
        last_input = inputs[inputs.length - 1];

        last_input.remove();
    }
}

function getSelectField(categorias){
    var select_category = document.createElement('select');
    categorias.forEach(categoria => {
        var c = document.createElement('option');
        c.setAttribute('value', categoria);
        c.appendChild(document.createTextNode(categoria));
        select_category.appendChild(c);
    });

    return select_category;
}

function getTaskInputField(){
    var task_desc = document.createElement('input');
    task_desc.setAttribute('name', 'descricao');
    task_desc.setAttribute('class', 'task form-control form-control-sm');
    task_desc.setAttribute('placeholder', 'Descrição da Tarefa');
    return task_desc;
}

function getTaskButton(){
    var button_finalizar = document.createElement('button');
    button_finalizar.setAttribute('onclick', 'finalizar_tarefa()');
    button_finalizar.setAttribute('class', 'btn btn-warning');
    button_finalizar.appendChild(document.createTextNode('Finalizar Tarefa'));
    return button_finalizar;
}

function iniciar_tarefa(categorias){
    tasks_container = document.getElementById('tasks');
    
    // Get all structures
    var task_category = getSelectField(categorias);
    var task_desc = getTaskInputField();
    var button_finalizar = getTaskButton();
    
    // Master Container
    var new_task_container = document.createElement('div');
    new_task_container.setAttribute('class', 'task-container');

    // Inputs Container
    var inputs_container = document.createElement('div');
    inputs_container.setAttribute('class', 'inputs-container');

    // Add all inputs to inputs container
    inputs_container.appendChild(task_desc);
    inputs_container.appendChild(task_category);

    // Add Inputs Container and Finish Task Button
    new_task_container.appendChild(inputs_container);
    new_task_container.appendChild(button_finalizar);

    // Append all structures
    tasks_container.appendChild(new_task_container);
}