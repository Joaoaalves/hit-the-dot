function excluirFerias(ferias_id, csrf_token){
    if(confirm("Deseja realmente excluir as férias?")){
        
        // Request Delete
        rqst = $.ajax({
            url : '/ferias/excluir',
            method : 'delete',
            beforeSend: function(request) {
                request.setRequestHeader("X-CSRFToken", csrf_token);
            },
            data : {
                id : ferias_id
            },
            error: function (request, status, error) {
                alert(request.responseText);
            }
        })
        
        // Request done
        rqst.done(function(){   
            window.location='/ferias';
        });

    }
}