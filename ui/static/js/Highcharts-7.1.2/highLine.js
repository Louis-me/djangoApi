function highLine(id,h_title,h_yaxis_title,h_tooltip,h_series){
    $(id).highcharts({
//    chart: {
//            type: 'line'
//        },
        title: {
            text: h_title,
            x: -20 //center
        },
        subtitle: {
            text: "",
            x: -20
        },
        xAxis: {
//            labels: {
//                step: h_xaxis_setp
//            },
            categories: ""
        },
        yAxis: {
            title: {
                text: h_yaxis_title
            },
            plotLines: [{
                value: 0,
                width: 1,
                color: '#808080'
            }]
        },
        tooltip: {
            valueSuffix: h_tooltip
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'middle',
            borderWidth: 1
        },
        series: h_series
    });

}