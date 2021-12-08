function removerUsuarioFerias(func_id, csrf_token){
    if(confirm("Deseja realmente excluir as férias?")){
        
        // Request Delete
        rqst = $.ajax({
            url : window.location.pathname + '/remover-funcionario',
            method : 'delete',
            beforeSend: function(request) {
                request.setRequestHeader("X-CSRFToken", csrf_token);
            },
            data : {
                id : func_id
            },
            error: function (request, status, error) {
                alert(request.responseText);
            }
        })
        
        // Request done
        rqst.done(function(){   
            location.reload();
        });

    }
}