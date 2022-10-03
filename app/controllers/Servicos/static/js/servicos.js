function excluirServico(id, csrf_token){
        if(confirm('Você realmente deseja excluir o serviço?')){
            $.ajax({
                url: 'servicos/excluir',
                type: 'DELETE',
                beforeSend: function(request) {
                        request.setRequestHeader("X-CSRFToken", csrf_token);
                },
                data: {
                    servico : id
                },
                statusCode: {
                    200: (response) => {
                        window.location.href = 'servicos';
                    },
                    400: (response) => {
                        alert('Erro ao excluir serviço!');
                    }
                }
            });

        }
}