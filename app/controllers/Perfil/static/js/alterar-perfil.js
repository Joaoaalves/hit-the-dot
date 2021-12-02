function enviarAlteracaoSenha(email, csrf_token){
    if(confirm('Tem certeza que deseja receber um email para alteração de senha?')){
        // Request Delete
        rqst = $.ajax({
            url : '/alterar-senha',
            method : 'post',
            beforeSend: function(request) {
                request.setRequestHeader("X-CSRFToken", csrf_token);
            },
            data : {
                email : email
            }
        })
        
        // Request done
        rqst.done(function(){ 
            location = '/perfil';
            alert('Um email contendo as instruções para alteração de senha foi enviado para você!');  
        });
    }
}