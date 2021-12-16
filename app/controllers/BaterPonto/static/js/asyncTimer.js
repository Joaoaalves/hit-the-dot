MAX_PERCENTAGE = 100;
SECOND = 1000;
MIN_IN_SEC = 3600;
function startTimer(progress, turno) {

    var time_in_seconds = (turno * MIN_IN_SEC);

    var percentage = 0;

        var loop = setInterval(
            function(){
                
                percentage = parseInt(progress * 100 / time_in_seconds);
                if(percentage > 100){
                    percentage = 100;
                    setTimer(parseInt(time_in_seconds));
                    setExtraTimer(parseInt(progress - time_in_seconds));
                }else{
                    setTimer(parseInt(progress));
                }
                

                config = [[percentage, 'rgba(25, 250, 204, 1)', 'rgba(25, 250, 204, 0.2)']]
                setProgressCircle(config);
        
                progress++;
            }, SECOND
        );


}

function setTimer(progress){
    var label = document.getElementById('remaining-time');
    label.textContent = 'Turno: ' + new Date(progress * 1000).toISOString().substr(11, 8);
}

function setExtraTimer(progress){
    var label = document.getElementById('extra-time');
    label.textContent = 'Tempo Extra: ' + new Date(progress * 1000).toISOString().substr(11, 8);
}

function getDate(time){
    var today = new Date();
    var month = today.getMonth() + 1;

    var full_string = month + "/" + today.getDate() + "/" + today.getFullYear() + " " + time;
    return new Date(full_string)
}
