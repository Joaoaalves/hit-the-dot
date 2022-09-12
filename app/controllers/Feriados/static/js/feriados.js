function excluirFeriado(feriado_id, csrf_token){
    if(confirm("Deseja realmente excluir o feriado?")){

        // Request Delete
        rqst = $.ajax({
            url : '/excluir-feriado',
            type : 'DELETE',
            beforeSend: function(request) {
                request.setRequestHeader("X-CSRFToken", csrf_token);
            },
            data : {
                id : feriado_id
            },
            success: function(){
                location.reload();
            }
        })
        
    }
}

function editarFeriado(feriado_id){
    window.location.href = '/editar-feriado/' + feriado_id;
}

function getUrlParam(paramName) {
    var match = window.location.search.match("[?&]" + paramName + "(?:&|$|=([^&]*))");
    return match ? (match[1] ? decodeURIComponent(match[1]) : "") : null;
}

$('.monthPicker').val(getUrlParam('mes'));
