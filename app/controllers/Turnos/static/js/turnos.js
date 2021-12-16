function abrirTurno(user_id, date) {

    var params = { date: date, user_id: user_id };
    let str = jQuery.param(params);


    window.location.href = '/turno?' + str;
}

function editarTurno(user_id, date) {
    var params = { date: date, user_id: user_id };
    let str = jQuery.param(params);

    window.location.href='/editar-turno?' + str;
}

function excluirTurno(user_id, date, csrf_token){
    if (confirm('Deseja excluir o turno?')) {

        // Request Delete
        rqst = $.ajax({
            url : '/excluir-turno',
            method : 'delete',
            beforeSend: function(request) {
                request.setRequestHeader("X-CSRFToken", csrf_token);
            },
            data : {
                user_id : user_id,
                date : date
            }
        })
        
        rqst.done(function(){   
            location.reload();
        });
    }
}

function clearTable(table, table_fields){
    
    static_size = table_fields;
    for(var i = 0; i < static_size; i++){
        table.deleteRow(1);
    }
}

function sortTable(table, column){
    switching = true;
    /* Make a loop that will continue until
    no switching has been done: */
    while (switching) {
      // Start by saying: no switching is done:
      switching = false;
      rows = table.rows;

      shouldSwitch = false;
      /* Loop through all table rows (except the
      first, which contains table headers): */
      for (i = 1; i < (rows.length - 1); i++) {
        // Start by saying there should be no switching:
        shouldSwitch = false;
        /* Get the two elements you want to compare,
        one from current row and one from the next: */
        x = rows[i].getElementsByTagName("th")[column];
        y = rows[i + 1].getElementsByTagName("th")[column];
        // Check if the two rows should switch place:
        if (column == 0 ){
            if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
            // If so, mark as a switch and break the loop:
            shouldSwitch = true;
            break;
            }
        }
        if (column == 1){
            if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                // If so, mark as a switch and break the loop:
                shouldSwitch = true;
                break;
                }
        }
      }
      if (shouldSwitch) {
        /* If a switch has been marked, make the switch
        and mark that a switch has been done: */
        rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
        switching = true;
      }
    }
}

function ordenarPor(field){
    table = document.getElementById('turnos-table');

    if(field == 'data')
        sortTable(table, 0);

    else if(field == 'funcionario')
        sortTable(table, 1);
}

document.getElementById('data').addEventListener('click', function(){
    ordenarPor('data');
});

document.getElementById('funcionario').addEventListener('click', function(){
    ordenarPor('funcionario');
})