Highcharts.chart('country', {
    chart: {
      height: '100%'
    },

    title: {
      text: 'Top 10 countries with highest total counts'
    },
  
    yAxis: {
      title: {
        text: 'Total count'
      }
    },
  
    xAxis: {
      title: {
        text: 'Day from the beginning of the outbreak in the country'
      }
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
