function highColumn(id, title, yAxis_title,data) {

    Highcharts.chart(id, {
        chart: {
            type: 'column'
        },
        title: {
            text: title
        },
        credits: {
			enabled: false
		},
        subtitle: {
            text: ''
        },
        xAxis: {
//            categories:["测试1","测试2"],
            type: 'category',
            labels: {
                rotation: -45,
                style: {
                    fontSize: '13px',
                    fontFamily: 'Verdana, sans-serif'
                }
            }
        },
        yAxis: {
            min: 0,
            title: {
                text: yAxis_title
            }
        },
        legend: {
            enabled: false
        },
        tooltip: {
            pointFormat: '<b>{point.y:.0f} </b>'
        },
        series: [{
            //name: 'Population',
            // data:[["shanghai", 24.2],["shanghai", 24.2]]
            data: data,
            dataLabels: {
                enabled: true,
                rotation: -90,
                color: '#FFFFFF',
                align: 'right',
                format: '{point.y:.0f}', // one decimal
                y: 10, // 10 pixels down from the top
                style: {
                    fontSize: '13px',
                    fontFamily: 'Verdana, sans-serif'
                }
            }
        }]
    });
}