function excluirServico(servico_id, csrf_token){
        if(confirm("Deseja realmente escluir o serviço?")){

                // Request Delete
                rqst = $.ajax({
                    url : '/servicos-atribuidos/excluir',
                    method : 'DELETE',
                    beforeSend: function(request) {
                        request.setRequestHeader("X-CSRFToken", csrf_token);
                    },
                        data : {
                                servico: servico_id
                        }
                })
                
                // Request done
                rqst.done(function(){   
                    location.reload();
                });
        }
}

function atualizarStatus(servico_id, csrf_token, status){
        if(confirm("Deseja realmente atualizar o status do serviço?")){

                // Request Delete
                rqst = $.ajax({
                    url : '/servicos-atribuidos/atualizar',
                    method : 'POST',
                    beforeSend: function(request) {
                        request.setRequestHeader("X-CSRFToken", csrf_token);
                    },
                        data : {
                                status: status,
                                servico: servico_id
                        }
                })
                
                // Request done
                rqst.done(function(){   
                    location.reload();
                });
        }
}

function verServico(url){
        window.open(url, '_blank').focus();
}