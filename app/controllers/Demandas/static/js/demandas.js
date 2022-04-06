function abrirDemanda(demandaUrl) {
        window.open(demandaUrl, '_blank').focus();
}

function marcarComoVerificada(demanda_id, csrf_token) {
        verifiedRequest(demanda_id, csrf_token, true);
}

function marcarComoNaoVerificada(demanda_id, csrf_token) {
        verifiedRequest(demanda_id, csrf_token, false);

}

function verifiedRequest(demanda_id, csrf_token, status){
        $.ajax({
                url: '/demandas/change-status',
                type: 'POST',
                beforeSend: function (request) {
                        request.setRequestHeader("X-CSRFToken", csrf_token);
                },
                data: {
                        demanda_id: demanda_id,
                        status: status
                },
                success: function (data) {
                        location.reload();
                }
        });
}

let searchParams = new URLSearchParams(window.location.search);

if(searchParams.has('status')){
        stats = searchParams.getAll('status');
        console.log(stats)
        if(stats.includes('verificada'))
                document.getElementById('verificada').checked = true;
        if(stats.includes('pendente'))
                document.getElementById('pendente').checked = true;
}


if(searchParams.has('mes')){
        mes = searchParams.get('mes');
    
        document.getElementById('month-picker').value = mes
    }
    

function editar(demanda_id){
        window.location.href = '/demanda/' + demanda_id;
}