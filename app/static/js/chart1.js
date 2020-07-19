Highcharts.chart('country', {

    title: {
      text: 'Countries with most cases'
    },
  
    yAxis: {
      title: {
        text: 'Cases'
      }
    },
  
    xAxis: {
    },
  
    legend: {
      layout: 'vertical',
      align: 'right',
      verticalAlign: 'middle'
    },
  
    plotOptions: {
      series: {
        label: {
          connectorAllowed: false
        }
      }
    },
  
    series: countryData,
  
    responsive: {
      rules: [{
        condition: {
          maxWidth: 500
        },
        chartOptions: {
          legend: {
            layout: 'horizontal',
            align: 'center',
            verticalAlign: 'bottom'
          }
        }
      }]
    }
  
  });