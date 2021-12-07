function add_filters(){
    month = document.getElementById('month-picker').value;

    try{
        funcionario = document.getElementById('funcionario').value;
        window.location.href = '?funcionario=' + funcionario + '&range=' + month;
    }catch(e){
        window.location.href = '?range=' + month;
    }
}


$('input[name="daterange"]').on('apply.daterangepicker',function(ev, picker){
    add_filters();
});

$('form #funcionario').on('change', function(){
    add_filters();
})

let searchParams = new URLSearchParams(window.location.search)

if(searchParams.has('mes')){
    mes = searchParams.get('mes');

    document.getElementById('month-picker').value = mes
}

if(searchParams.has('funcionario')){
    funcionario = searchParams.get('funcionario');

    document.getElementById('funcionario').value = funcionario;
}
