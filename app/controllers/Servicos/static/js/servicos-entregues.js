function excluirServico(servico_id, csrf_token) {
        if (confirm("Deseja realmente excluir o serviço?")) {

                // Request Delete
                rqst = $.ajax({
                        url: '/servicos-entregues/' + servico_id,
                        method: 'DELETE',
                        beforeSend: function (request) {
                                request.setRequestHeader("X-CSRFToken", csrf_token);
                        }
                })

                // Request done
                rqst.done(function () {
                        location.reload();
                });
        }
}

function invalidarServico(servico_id, csrf_token) {

        // Request Post
        rqst = $.ajax({
                url: '/servicos-entregues/invalidar',
                method: 'POST',
                beforeSend: function (request) {
                        request.setRequestHeader("X-CSRFToken", csrf_token);
                },
                data: {
                        servico: servico_id
                }
        });

        // Request done
        rqst.done(function () {
                location.reload();
        });

}

function verificarServico(servico_id) {
        window.location = '/servicos-entregues/' + servico_id;
}



function verServico(url) {
        if (!url.includes('https://')) {
                url = 'https://' + url;
        }
        window.open(url, '_blank').focus();
}