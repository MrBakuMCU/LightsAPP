var chart;

function requestData() {
    $.ajax({
        url: '/live-data',
        success: function(point) {
            var series = chart.series[0],
                shift = series.data.length > 200; // shift if the series is
                                                 // longer than 20

            // add the point
            chart.series[0].addPoint(point, true, shift);

            // call it again after one second
            setTimeout(requestData, 700);
        },
        cache: false
    });
}

$(document).ready(function() {
    chart = new Highcharts.Chart({
        chart: {
            renderTo: 'data-container',
            defaultSeriesType: 'spline',
            events: {
                load: requestData
            }
        },
        title: {
            text: 'Tempure'
        },
        xAxis: {
            type: 'datetime',
            tickPixelInterval: 400,
            maxZoom: 20 * 1000
        },
        yAxis: {
            minPadding: 0.1,
            maxPadding: 0.1,
            title: {
                text: 'Value',
                margin: 20
            }
        },
        series: [{
            name: 'Temperure',
            data: []
        }, {
            name: 'Humidity',
            data: []
        }]
    });
});