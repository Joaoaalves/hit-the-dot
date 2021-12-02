function excluir_cargo(cargo_id, csrf_token){
    if(confirm("Deseja realmente excluir o cargo?")){
        
        // Request Delete
        rqst = $.ajax({
            url : 'excluir',
            method : 'delete',
            beforeSend: function(request) {
                request.setRequestHeader("X-CSRFToken", csrf_token);
            },
            data : {
                cargo_id : cargo_id
            }
        })
        
        // Request done
        rqst.done(function(){   
            location.reload();
        });
    }
}