var chart_ranking = document.getElementById('chartRanking').getContext('2d');
var myRankingChart = new Chart(chart_ranking, {
    type: 'bar',
    data: {
        labels: Object.keys(funcionarios),
        datasets: [{
            label: 'Horas Trabalhadas',
            data: Object.values(funcionarios),
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)'
            ],
            borderWidth: 1,
            barThickness: 10,
            borderRadius: 10
        }]
    },
    options: {
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
                    display: false
                }
            },
            x: {    
                grid: {
                    display: false
                }
            }            

        }
    }
});


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
                ticks: {
                    display: false
                },
                grid: {
                    display: false
                }
            },
            x: {
                grid: {
                    display: false
                }
            }            

        }
    }
});