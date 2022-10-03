function statusFuncionario(csrf_token, id, status) {
        if(confirm("Deseja realmente desativar o funcionário?")){

                // Request Delete
                rqst = $.ajax({
                    url : '/status-funcionario/' + id,
                    method : 'POST',
                    beforeSend: function(request) {
                        request.setRequestHeader("X-CSRFToken", csrf_token);
                    },
                        data : {
                                status: status
                        }
                })
                
                // Request done
                rqst.done(function(){   
                    location.reload();
                });
        }
        
}
