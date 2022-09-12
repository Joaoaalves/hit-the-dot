function selecionarServico(index) {
        serv = resposta[index]
        document.getElementById('nome-servico').value = serv['name'];
        document.getElementById('servico').value = serv['id'];
        if (serv['atributo'] !== undefined) {
                atributo = serv['atributo']

                // Add input for atribute
                document.getElementById('service').insertAdjacentHTML('afterend',
                        `<div class="form-floating mb-3" id="atb-input"><input type="${atributo['type']}"` +
                        ` class="form-control" id="atb_value" name="atributo" placeholder="${atributo['name']}"` +
                        ` value="${atributo['default_value']}" required><label for="atributo">${atributo['name']}</label></div>`);
                document.getElementById('atb-input').insertAdjacentHTML('afterend',
                        `<input type="hidden" id="atb_id" name="atb_id" value="${atributo['id']}">`);
        } else {
                try {
                        document.getElementById('atb-input').remove();
                        document.getElementById('atb_id').remove();
                } catch (e) {}
        }
        bootstrap.Modal.getInstance(document.getElementById('servicosModal')).hide();
}

$(document).ready(function () {
        $('#select-serv').selectize({
                sortField: 'text'
        });
        $('#select-cliente').selectize({
                sortField: 'text'
        });
});

servicoPesquisa = document.getElementById('search-servico');
table_body = document.getElementById('servicos-pesquisados');
aviso = document.getElementById('aviso-search');

function debounce(func, timeout) {
        let timer;
        return (...args) => {
                clearTimeout(timer);
                timer = setTimeout(() => {
                        func.apply(this, args);
                }, timeout);
        };
}

$('#search-servico').keyup(debounce(function () {
        service_name = servicoPesquisa.value;
        table_body.innerHTML = "";
        rqst = $.ajax({
                url: '/servicos/pesquisar',
                method: 'POST',
                beforeSend: function (request) {
                        request.setRequestHeader("X-CSRFToken", csrf_token);
                },
                data: {
                        service_name: service_name
                },
                statusCode: {
                        200: (response) => {
                                try {
                                        aviso.textContent = '';
                                        resposta = JSON.parse(response);
                                        organizaServicos(resposta);
                                } catch (e) {
                                        console.log(e)
                                }
                        },
                        429: (response) => {
                                try {
                                        aviso.textContent = 'Tentativas máximas de busca excedidas!';
                                } catch (e) {
                                        console.log(e)
                                }
                        }

                }
        })
}, 500));

function organizaServicos(servicos) {

        servicos.forEach((servico, i) => {
                row = table_body.insertRow();

                serv_name = row.insertCell();
                serv_name.innerText = servico['name'];

                action = row.insertCell();
                action.innerHTML = "<button onclick='selecionarServico(" + i + ")' class='btn btn-success select_service'><i class='fas fa-plus'></i></button>";

        });
}


$("#servicosModal").on('shown.bs.modal', function () {
        $('#search-servico').focus();
});


input_servico = document.getElementById('nome-servico');
$('#form-servico').submit(function () {
        if (input_servico.value == '') {
                input_servico.focus();
                input_servico.classList.add('is-invalid');
                return false;
        }
        return true;
})

$("body").on("submit", "form", function () {
        $(this).submit(function () {
                return false;
        });
        return true;
});