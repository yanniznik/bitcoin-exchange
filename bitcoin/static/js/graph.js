$(document).ready(function(){
  var points = new Array();  
  var labels = new Array();

  $.get('/historicaldata', function(data) {
    if (data) {
        db = JSON.parse(data)
        $.each(db, function(i, n){
            labels.push(i.slice(5));
            points.push(n);
        });
        new Chart(document.getElementById("historical_data"), {
            type: "line",
            data: {
                labels: labels,
                datasets: [{
                    label: "BTC Price",
                    data: points,
                    fill: false,
                    borderColor: "rgb(75, 192, 192)",
                    lineTension: 0.4
                }]
            },
            options: {
                layout: {
                    padding: {
                        left: 40,
                        right: 40,
                        top: 30,
                        bottom: 0
                    }
                },
                legend: {
                    display: false
                    
                },
                maintainAspectRatio: false,
                tooltips: {
                    enabled: true,
                    mode: 'index',
                    intersect: false,
                    TitlefontSize: 0,
                },
                responsive: true,
                scales: {
                    xAxes: [{
                        ticks: {
                            fontColor: "#cfd2f1",
                            fontSize: 16,
                            maxTicksLimit: 8,
                            maxRotation: 0,
                            minRotation: 0

                        },
                        gridLines: {
                            display: true,
                            drawBorder: true
                        }
                    }],
                    yAxes: [{
                        ticks: {
                            fontColor: "white",
                            fontSize: 16,
                            maxTicksLimit: 8,
                        },
                        gridLines: {

                            display: true,
                            drawBorder: true
                        }
                    }]
                }
            }
        }); 
    }
});

});




