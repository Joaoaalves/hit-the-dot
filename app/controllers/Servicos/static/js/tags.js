function excluirTag(csrf_token, tag_id){
        if(confirm("Deseja realmente excluir esta tag?")){
            $.ajax({
                url: "/servicos/tags/excluir/",
                type: "DELETE",
                beforeSend: function(request) {
                        request.setRequestHeader("X-CSRFToken", csrf_token);
                },
                data: {
                        tag: tag_id
                },
                success: function(data){
                        location.reload();
                }
            });
        }

}