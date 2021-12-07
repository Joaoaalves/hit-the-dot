var chart_relatorio = document.getElementById('chartRelatorio').getContext('2d');

const labels = Object.keys(week_hours);
const data = Object.values(week_hours);

var myRelatorioChart = new Chart(chart_relatorio, {
    type: 'line',
    data: {
        labels: labels,
        datasets: [{
            data: data,
            fill: false,
            borderColor: '#f8be00',
            tension: 0.4,
            pointBorderColor: '#f8be00',
            pointBackgroundColor: '#f8be00',
            pointRadius: 5
        }]
    },
    options: {
        tooltips: {
            mode: 'label',
            position: "nearest",
            label: 'mylabel',
            callbacks: {
                label: function(tooltipItem, data) {
                    return   data.datasets[tooltipItem.datasetIndex].label+ " "  + number_format2(tooltipItem.yLabel.toString(), 2, ',', '.') ; }, },
        },
        responsive: true, 
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: false
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                ticks: {
                    display: false
                },
                grid: {
                    display: false,
                    drawBorder: false
                }
            },
            x: {
                grid: {
                    display: false,
                    drawBorder: false
                }
            }            

        }
    }
});