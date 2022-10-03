function setProgressCircles(config) {

    var p_rings = document.querySelectorAll('.progress-ring');

    var counter = 0;

    p_rings.forEach((p_ring) => {

        var background_circle = p_ring.childNodes[1];
        var circle = p_ring.childNodes[3];
        var text_inside = p_ring.childNodes[5];

        var radius = circle.r.baseVal.value;
        var circumference = radius * 2 * Math.PI;

        circle.style.strokeDasharray = `${circumference} ${circumference}`;
        circle.style.strokeDashoffset = `${circumference}`;

        var [progress, color, color_background] = config[counter];

        circle.style.stroke = color;
        const offset = circumference - progress / 100 * circumference;

        circle.style.strokeDashoffset = offset;

        background_circle.style.stroke = color_background;

        if(!config[counter][3])
            text_inside.textContent = String(progress + '%');
        else
            text_inside.textContent = config[counter][3];
            
        counter++;
    });

}

function setProgressCircle(config) {
    p_ring = document.querySelector('.progress-ring');
    var [progress, color, color_background] = config[0];
    var background_circle = p_ring.childNodes[1];
    var circle = p_ring.childNodes[3];
    var text_inside = p_ring.childNodes[5];

    var radius = circle.r.baseVal.value;
    var circumference = radius * 2 * Math.PI;

    circle.style.strokeDasharray = `${circumference} ${circumference}`;
    circle.style.strokeDashoffset = `${circumference}`;

    circle.style.stroke = color;
    const offset = circumference - progress / 100 * circumference;

    circle.style.strokeDashoffset = offset;

    background_circle.style.stroke = color_background;

    text_inside.textContent = String(progress + '%');

}

// Recalculate on window resize
window.addEventListener('resize', function (event) {
    setProgressCircles(config);
}, true);

