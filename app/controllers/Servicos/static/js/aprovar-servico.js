function abrirServico(url) {
        window.open(url, '_blank').focus();
}

document.getElementById('ver-servico').addEventListener("click", function (event) {
        event.preventDefault();
});