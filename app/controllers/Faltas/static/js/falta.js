function abonarFalta(falta_id, csrf_token){
    if(confirm("Deseja realmente abonar a falta?")){
        
        // Request Delete
        rqst = $.ajax({
            url : '/abonar-falta',
            method : 'POST',
            beforeSend: function(request) {
                request.setRequestHeader("X-CSRFToken", csrf_token);
            },
            data : {
                falta_id : falta_id
            }
        })
        
        // Request done
        rqst.done(function(){   
            window.location.href = '/faltas';
        });
    }
}