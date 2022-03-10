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