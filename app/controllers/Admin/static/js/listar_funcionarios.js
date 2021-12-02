function excluirFuncionario(user_id, csrf_token){
    if(confirm("Deseja realmente excluir o usuário?")){
        
        // Request Delete
        rqst = $.ajax({
            url : '/excluir-usuario',
            method : 'delete',
            beforeSend: function(request) {
                request.setRequestHeader("X-CSRFToken", csrf_token);
            },
            data : {
                uid : user_id
            }
        })
        
        // Request done
        rqst.done(function(){   
            location.reload();
        });
    }

}

function editarFuncionario(user_id){
    window.location.href = '/editar-funcionario/' + user_id;
}

$(document).ready(function() {
    // Construct URL object using current browser URL
    var url = new URL(document.location);
  
    // Get query parameters object
    var params = url.searchParams;
  
    // Get value of paper
    var cargo = params.get('cargo')
    
    if(cargo){
        // Set it as the dropdown value
        $("#cargo-select").val(cargo);
    }
});