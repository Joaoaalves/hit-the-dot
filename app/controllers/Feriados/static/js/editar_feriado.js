var myCalendar = new TavoCalendar('#my-calendar', {
    range_select: false,
    format: "DD-MM-YYYY",
    locale: 'pt-br',
    future_select: true,
    past_select: true,
    highligh_sunday: true,
    highlight_saturday: true
});

document.getElementById('sbt-btn').addEventListener("click", function(event){
    event.preventDefault();

    date = myCalendar.getSelected();
    if(date == undefined){
        alert('Selecione uma data');
        return;
    }

    input_nome = document.getElementsByName('name')[0];
    nome = input_nome.value;
    if(nome == ''){
        alert('Adicione um nome ao feriado!');
        return;
    }
    
    repeat = document.getElementById('repeat').checked;

    csrf_token = document.getElementsByName('csrf_token')[0].value;
    
    if(date != undefined && confirm("Deseja realmente salvar as informações?")){

        // Request Delete
        rqst = $.ajax({
            method : 'POST',
            beforeSend: function(request) {
                request.setRequestHeader("X-CSRFToken", csrf_token);
            },
            data : {
                name : nome,
                date : date,
                repeat : repeat
            },
            error : function(){
                alert('Ocorreu algum erro');
            }
        })
        
        // Request done
        rqst.done(function(){   
            window.location.href = '/feriados'
        });
    }
});