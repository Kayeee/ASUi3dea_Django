// Load the Visualization API and the corechart package.
google.charts.load('current', {'packages':['corechart', 'line']});

// Set a callback to run when the Google Visualization API is loaded.
google.charts.setOnLoadCallback(drawAllGraphs);

var lineOptions = {
    'hAxis': {
          format: 'M/d/yy',
          gridlines: {count: 15}
     },
    'vAxis': {
          gridlines: {color: 'none'},
          minValue: 0
     },
     'explorer': {},
     // 'series': {
     //   1: {curveType: 'function'}
     // },
     'width':550,
     'height':500
   };


function drawAllGraphs(){
  drawPowerLine();
  drawCurrentLine();
  drawVoltageLine();
  drawEfficiencyArea();
  drawEnergyChart();
  drawTemperatureChart();
}


function drawPowerLine() {
     var jsonData = $.ajax({
         url: powerURL,
         dataType: "json",
         async: false
         }).responseText;
     var dataObj = JSON.parse(jsonData)

     // Create our data table out of JSON data loaded from server.
     var data = new google.visualization.DataTable();
     data.addColumn('datetime', 'Date');
     data.addColumn('number', 'Input Power');
     data.addColumn('number', 'Grid Power');

     for (i = 0; i< dataObj["InputPower"].length ; i++){
       data.addRow([formatDate(dataObj["InputPower"][i][0]), dataObj["InputPower"][i][1], dataObj["GridPower"][i][1]])
     }

     lineOptions['title'] = "Power (W)"


     // Instantiate and draw our chart, passing in some options.
     var chart = new google.visualization.LineChart(document.getElementById('current-line'));
     chart.draw(data, lineOptions);
}


function drawCurrentLine(){
  var jsonData = $.ajax({
      url: currentURL,
      dataType: "json",
      async: false
      }).responseText;
  var dataObj = JSON.parse(jsonData)

  // Create our data table out of JSON data loaded from server.
  var data = new google.visualization.DataTable();
  data.addColumn('datetime', 'Date');
  data.addColumn('number', 'Input Current');
  data.addColumn('number', 'Grid Current');

  for (i = 0; i< dataObj["InputCurrent"].length ; i++){
    data.addRow([formatDate(dataObj["InputCurrent"][i][0]), dataObj["InputCurrent"][i][1], dataObj["GridCurrent"][i][1]])
  }

  lineOptions['title'] = "Current (A)"

  // Instantiate and draw our chart, passing in some options.
  var chart = new google.visualization.LineChart(document.getElementById('power-line'));
  chart.draw(data, lineOptions);
}


function drawVoltageLine(){
  var jsonData = $.ajax({
      url: voltageURL,
      dataType: "json",
      async: false
      }).responseText;
  var dataObj = JSON.parse(jsonData)

  // Create our data table out of JSON data loaded from server.
  var data = new google.visualization.DataTable();
  data.addColumn('datetime', 'Date');
  data.addColumn('number', 'Input Voltage');
  data.addColumn('number', 'Grid Voltage');

  for (i = 0; i< dataObj["InputVoltage"].length ; i++){
    data.addRow([formatDate(dataObj["InputVoltage"][i][0]), dataObj["InputVoltage"][i][1], dataObj["GridVoltage"][i][1]])
  }

  lineOptions['title'] = "Voltage (V)"

  // Instantiate and draw our chart, passing in some options.
  var chart = new google.visualization.LineChart(document.getElementById('voltage-line'));
  chart.draw(data, lineOptions);
}


function drawEfficiencyArea(){
  var jsonData = $.ajax({
      url: efficiencyURL,
      dataType: "json",
      async: false
      }).responseText;
  var dataObj = JSON.parse(jsonData)

  // Create our data table out of JSON data loaded from server.
  var data = new google.visualization.DataTable();
  data.addColumn('datetime', 'Date');
  data.addColumn('number', 'Efficiency');

  for (i = 0; i< dataObj["ConversionEfficiency"].length ; i++){
    data.addRow([formatDate(dataObj["ConversionEfficiency"][i][0]), dataObj["ConversionEfficiency"][i][1]])
  }

  lineOptions['title'] = "DC/AC Conversion Efficiency"

  // Instantiate and draw our chart, passing in some options.
  var chart = new google.visualization.AreaChart(document.getElementById('efficiency-area'));
  chart.draw(data, lineOptions);
}


function drawEnergyChart(){
  var jsonData = $.ajax({
      url: energyURL,
      dataType: "json",
      async: false
      }).responseText;
  var dataObj = JSON.parse(jsonData)

  // Create our data table out of JSON data loaded from server.
  var data = new google.visualization.DataTable();
  data.addColumn('datetime', 'Date');
  data.addColumn('number', 'Daily (kWh)');
  data.addColumn('number', 'Weekly (kWh)');

  for (i = 0; i< dataObj["CumulatedEnergy"].length ; i++){
    data.addRow([formatDate(dataObj["CumulatedEnergy"][i][0]), dataObj["CumulatedEnergy"][i][1], dataObj["CumulatedEnergy"][i][2]])
  }

  var tempOptions = Object.assign({}, lineOptions);
  tempOptions['title'] = "Total Energy"
  tempOptions['seriesType'] = 'bars',
  tempOptions['series'] = {1: {type: 'steppedArea'}}

  // Instantiate and draw our chart, passing in some options.
  var chart = new google.visualization.ComboChart(document.getElementById('energy-chart'));
  chart.draw(data, tempOptions);
}


function drawTemperatureChart(){
  var jsonData = $.ajax({
      url: temperatureURL,
      dataType: "json",
      async: false
      }).responseText;
  var dataObj = JSON.parse(jsonData)

  // Create our data table out of JSON data loaded from server.
  var data = new google.visualization.DataTable();
  data.addColumn('datetime', 'Date');
  data.addColumn('number', 'Temp (C)');

  for (i = 0; i< dataObj["InverterTemperature"].length ; i++){
    data.addRow([formatDate(dataObj["InverterTemperature"][i][0]), dataObj["InverterTemperature"][i][1]])
  }

  lineOptions['title'] = "Inverter Temperature"

  // Instantiate and draw our chart, passing in some options.
  var chart = new google.visualization.LineChart(document.getElementById('temperature-chart'));
  chart.draw(data, lineOptions);
}


//'2016-08-04T23:46:01.828Z' -> '2016-08-04 23:46:01'
function formatDate(date){
  var stripped = date.replace(/\..*$/, ' ').replace(/T/, ' ');
  var newDate = new Date(stripped)
  return newDate
}
