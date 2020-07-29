Highcharts.chart('gdp', {
  chart: {
    height: '50%',
    zoomType: 'xy'
  },
  title: {
    text: 'GDP per capita vs Count per million'
  },
  xAxis: [{
    categories: gdpData['countries'],
    crosshair: true
  }],
  yAxis: [{ // Primary yAxis
    labels: {
      format: '{value}$',
      style: {
        color: Highcharts.getOptions().colors[1]
      }
    },
    title: {
      text: 'GDP per capita',
      style: {
        color: Highcharts.getOptions().colors[1]
      }
    }
  }, { // Secondary yAxis
    title: {
      text: 'Count per million',
      style: {
        color: Highcharts.getOptions().colors[0]
      }
    },
    labels: {
      format: '{value}',
      style: {
        color: Highcharts.getOptions().colors[0]
      }
    },
    opposite: true
  }],
  tooltip: {
    shared: true
  },
  legend: {
    layout: 'vertical',
    align: 'left',
    x: 120,
    verticalAlign: 'top',
    y: 100,
    floating: true,
    backgroundColor:
      Highcharts.defaultOptions.legend.backgroundColor || // theme
      'rgba(255,255,255,0.25)'
  },
  series: [{
    name: 'Count per million',
    type: 'line',
    yAxis: 1,
    data: gdpData['rates'],
    tooltip: {
      valueSuffix: ' count per million'
    }

  }, {
    name: 'GDP per capita',
    type: 'line',
    data: gdpData['gdps'],
    tooltip: {
      valueSuffix: '$'
    }
  }]
});
