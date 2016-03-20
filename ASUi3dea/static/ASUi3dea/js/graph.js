
$(document).ready(function() {
  var margin = {top: 20, right: 20, bottom: 30, left: 50},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

  //var parseDate = d3.time.format("%Y-%m-%d").parse; // for dates like "2014-01-01"
  var parseDate = d3.time.format("%Y-%m-%dT%H:%M:%S.%LZ").parse;  // for dates like "2014-01-01T00:00:00Z"

  var x = d3.time.scale()
    .range([0, width]);

  var y = d3.scale.linear()
    .range([height, 0]);

  var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");

  var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left");

  var line = d3.svg.line()
    .x(function(d) { return x(d.timeStamp); })
    .y(function(d) { return y(d.data_value); });

  var svg = d3.select("body").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
});

function draw_line_graph(data){
  svg.selectAll("*").remove()
  var parseDate = d3.time.format("%Y-%m-%dT%H:%M:%S.%LZ").parse;
  data.forEach(function(d) {
    d.timeStamp = parseDate(d[0]);
    d.data_value = d[1];
  });
  x.domain(d3.extent(data, function(d) { return d.timeStamp; }));
  y.domain(d3.extent(data, function(d) { return d.data_value; }));

  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);

  svg.append("g")
      .attr("class", "y axis")
      .call(yAxis)
    .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text("");

  svg.append("path")
      .datum(data)
      .attr("class", "line")
      .attr("d", line);
}