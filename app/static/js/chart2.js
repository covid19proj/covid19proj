Highcharts.chart('bubble', {

    chart: {
      type: 'bubble',
      plotBorderWidth: 1,
      height: '100%',
      zoomType: 'xy'
    },
  
    title: {
      text: 'Total count depending on population and percentage of people older than 70'
    },
  
    xAxis: {
       title: {
      text: 'Population'
    },
  
      gridLineWidth: 1,
      accessibility: {
        rangeDescription: 'Range: 0 to 100.'
      }
    },
  
    yAxis: {
       title: {
      text: 'Percentage of people older than 70'
    },
  
      startOnTick: false,
      endOnTick: false,
      accessibility: {
        rangeDescription: 'Range: 0 to 100.'
      }
    },
  
    series: [{name: 'Total count',
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
  
