function abrirTurno(user_id, date) {

    var params = {
        date: date,
        user_id: user_id
    };
    let str = jQuery.param(params);


    window.location.href = '/turno?' + str;
}

function editarTurno(user_id, date) {
    var params = {
        date: date,
        user_id: user_id
    };
    let str = jQuery.param(params);

    window.location.href = '/editar-turno?' + str;
}

function excluirTurno(turno_id, csrf_token) {
    if (confirm('Deseja excluir o turno?')) {

        // Request Delete
        rqst = $.ajax({
            url: '/excluir-turno',
            method: 'delete',
            beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", csrf_token);
            },
            data: {
                turno_id: turno_id
            }
        })

        rqst.done(function () {
            location.reload();
        });
    }
}

function clearTable(table, table_fields) {

    static_size = table_fields;
    for (var i = 0; i < static_size; i++) {
        table.deleteRow(1);
    }
}

