Highcharts.chart('continent', {
    chart: {
      type: 'packedbubble',
      height: '100%'
    },
    title: {
      text: 'Continents'
    },
    tooltip: {
      useHTML: true,
      pointFormat: '<b>{point.name}:</b> {point.value}'
    },
    plotOptions: {
      packedbubble: {
        minSize: '15%',
        maxSize: '500%',
        zMin: 0,
        zMax: 10000000,
        layoutAlgorithm: {
          splitSeries: false,
          gravitationalConstant: 0.02
        },
        dataLabels: {
          enabled: true,
          format: '{point.name}',
          filter: {
            property: 'y',
            operator: '>',
            value: 250
          },
          style: {
            color: 'black',
            textOutline: 'none',
            fontWeight: 'normal'
          }
        }
      }
    },
  
    series: continentsData
  
  });
  
