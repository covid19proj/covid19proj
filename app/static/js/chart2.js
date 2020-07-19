Highcharts.chart('bubble', {

    chart: {
      type: 'bubble',
      plotBorderWidth: 1,
      zoomType: 'xy'
    },
  
    title: {
      text: 'Median Age'
    },
  
    xAxis: {
       title: {
      text: 'GPD per capita'
    },
  
      gridLineWidth: 1,
      accessibility: {
        rangeDescription: 'Range: 0 to 100.'
      }
    },
  
    yAxis: {
       title: {
      text: 'Total deaths depending on 2 metrics'
    },
  
      startOnTick: false,
      endOnTick: false,
      accessibility: {
        rangeDescription: 'Range: 0 to 100.'
      }
    },
  
    series: [{name: 'Total Deaths',
      data: bubbleData,
      marker: {
        fillColor: {
          radialGradient: { cx: 0.4, cy: 0.3, r: 0.7 },
          stops: [
            [0, 'rgba(255,255,255,0.5)'],
            [1, Highcharts.color(Highcharts.getOptions().colors[0]).setOpacity(0.5).get('rgba')]
          ]
        }
      }
    }]
  
  });
  