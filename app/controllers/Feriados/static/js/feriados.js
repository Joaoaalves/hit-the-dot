function excluirFeriado(feriado_id, csrf_token){
    if(confirm("Deseja realmente excluir o feriado?")){
        
        // Request Delete
        rqst = $.ajax({
            url : '/excluir-feriado',
            method : 'delete',
            beforeSend: function(request) {
                request.setRequestHeader("X-CSRFToken", csrf_token);
            },
            data : {
                id : feriado_id
            }
        })
        
        // Request done
        rqst.done(function(){   
            location.reload();
        });
    }
}

function editarFeriado(feriado_id){
    window.location.href = '/editar-feriado/' + feriado_id;
}

$(function() {
    month_input = document.getElementById('month');

    const urlParams = new URLSearchParams(window.location.search);
    const month_param = urlParams.get('month');

    if(month_param){
        month_input.value = month_param;
    }else{
        d = new Date();
        month_int = d.getMonth();
        month = month_int.toLocaleString('en-US', {
            minimumIntegerDigits: 2
        });

        month_input.value = d.getYear().toString() + '-' + month;
    }
});