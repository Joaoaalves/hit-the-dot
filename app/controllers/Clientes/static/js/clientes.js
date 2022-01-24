function excluirCliente(cliente_id, csrf_token){
    if(confirm("Deseja realmente excluir o cliente?")){
        
        // Request Delete
        rqst = $.ajax({
            url : '/deletar-cliente',
            method : 'delete',
            beforeSend: function(request) {
                request.setRequestHeader("X-CSRFToken", csrf_token);
            },
            data : {
                uid : cliente_id
            }
        })
        
        // Request done
        rqst.done(function(){   
            location.reload();
        });
    }

}