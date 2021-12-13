MAX_PERCENTAGE = 100;
SECOND = 1000;
MIN_IN_SEC = 3600;
function startTimer(progress, turno) {

    var time_in_seconds = (turno * MIN_IN_SEC);

    var percentage = 0;

    if(progress <= time_in_seconds){
        var loop = setInterval(
            function(){
                setTimer(parseInt(progress));
    
                percentage = parseInt(progress * 100 / time_in_seconds);
                config = [[percentage, 'rgba(25, 250, 204, 1)', 'rgba(25, 250, 204, 0.2)']]
                setProgressCircle(config);
                
                progress++;
    
                if(progress > time_in_seconds) {
                    clearInterval(loop);
                    document.getElementById('remaining-time').textContent = 'Finalizado!';
                }
            }, SECOND
        );
    }
    else{
        document.getElementById('remaining-time').textContent = 'Finalizado!';
        setProgressCircle([[MAX_PERCENTAGE, '#f8be00', 'rgba(0, 0, 0, 0.1)']]);
    }

}

function setTimer(progress){
    var label = document.getElementById('remaining-time');
    label.textContent = new Date(progress * 1000).toISOString().substr(11, 8);
}

function getDate(time){
    var today = new Date();
    var month = today.getMonth() + 1;

    var full_string = month + "/" + today.getDate() + "/" + today.getFullYear() + " " + time;
    return new Date(full_string)
}
