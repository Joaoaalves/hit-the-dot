function excluirCategoria(cat_id, csrf_token){
        if(confirm("Deseja realmente excluir a categoria?")){

                // Request Delete
                rqst = $.ajax({
                    url : '/servicos/excluir-categoria',
                    method : 'DELETE',
                    beforeSend: function(request) {
                        request.setRequestHeader("X-CSRFToken", csrf_token);
                    },
                        data : {
                                cat_id : cat_id
                        }
                })
                
                // Request done
                rqst.done(function(){   
                    location.reload();
                });
        }
}