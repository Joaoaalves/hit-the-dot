function requestUpdateStatus(status, csrf_token) {
    if (confirm("Deseja realmente atualizar seu status?")) {

        // Request Delete
        rqst = $.ajax({
            url: '/bater-ponto/',
            method: 'POST',
            beforeSend: function (request) {
                request.setRequestHeader("X-CSRFToken", csrf_token);
            },
            data: {status : status}
        })

        rqst.done(function () {
            location.reload();
        });
    }
}

Date.prototype.addHours = function (h) {
    this.setHours(this.getHours() + h);
    return this;
}

function setClock(dateString, turno) {

    var dateParts = dateString.split("/");
    var final_date_string = dateParts[1] + " " + dateParts[0] + " " + dateParts[2]

    var start = new Date(final_date_string);

    var end = new Date(start);
    end.addHours(turno);

    var max = 6;
    var digits = 1;
    var timespan = countdown(start, end, countdown.HOURS | countdown.MINUTES | countdown.SECONDS, max, digits);
    console.log(timespan.toHTML())
}

function checkCompletedFields() {
    tasks = document.getElementsByName('task');

    completed = true;
    tasks.forEach(task => {
        if (!task.value) {
            completed = false;
            return;
        }
    });

    return completed;
}

function hms(seconds) {
    return [3600, 60]
      .reduceRight(
        (p, b) => r => [Math.floor(r / b)].concat(p(r % b)),
        r => [r]
      )(seconds)
      .map(a => a.toString().padStart(2, '0'))
      .join(':');
  }
  