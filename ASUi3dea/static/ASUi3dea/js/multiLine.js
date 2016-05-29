
// var parseDate = d3.time.format("%Y-%m-%dT%H:%M:%S.%LZ").parse;
//
// var margin = {top: 10, right: 10, bottom: 100, left: 40},
//   width = 960 - margin.left - margin.right,
//   height = 500 - margin.top - margin.bottom;
//
// var vis = d3.select("#analytics").append("svg")
//     .attr("width", width + margin.left + margin.right)
//     .attr("height", height + margin.top + margin.bottom),
//     WIDTH = 1000,
//     HEIGHT = 500,
//     MARGINS = {
//         top: 20,
//         right: 20,
//         bottom: 20,
//         left: 50
//     },
//
// xScale = d3.time.scale().range([MARGINS.left, WIDTH - MARGINS.right]),
// yScale = d3.scale.linear().range([HEIGHT - MARGINS.top, MARGINS.bottom]).domain([0,100]),
//
// xAxis = d3.svg.axis()
//     .scale(xScale)
// yAxis = d3.svg.axis()
//     .scale(yScale)
//     .orient("left")
//
// var lineGen = d3.svg.line()
//     .x(function(d) {
//       var temp = xScale(d["timeStamp"])
//         return xScale(d.timeStamp);
//     })
//     .y(function(d) {
//         return yScale(d.data_value);
//     })
//     .interpolate("basis");
//
// function drawPowerGraph(data){
//
// data = data["ACPower"]
//           data.forEach(function(d) {
//               d.timeStamp = parseDate(d[0]);
//               d.data_value = d[1];
//           });
//
//           x.domain(d3.extent(data.map(function(d) { return d.timeStamp; })));
//           //y.domain([0, d3.max(data.map(function(d) { return d.data_value; }))]);
//
//   vis.append("svg:g")
//     .attr("class","axis")
//     .attr("transform", "translate(0," + (HEIGHT - MARGINS.bottom) + ")")
//     .call(xAxis);
//
//   vis.append("svg:g")
//       .attr("class", "axis")
//       .attr("transform", "translate(" + (MARGINS.left) + ",0)")
//       .call(yAxis);
//
//   vis.append('svg:path')
//       .attr('d', lineGen(data))
//       .attr('stroke', 'green')
//       .attr('stroke-width', 2)
//       .attr('fill', 'none');
//
//   // vis.append('svg:path')
//   //     .attr('d', lineGen(data["ACPower"]))
//   //     .attr('stroke', 'blue')
//   //     .attr('stroke-width', 2)
//   //     .attr('fill', 'none');
//
//
// }


var margin = {top: 20, right: 20, bottom: 30, left: 50},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

var parseDate = d3.time.format("%Y-%m-%dT%H:%M:%S.%LZ").parse;

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
    .x(function(d) { return x(d.date); })
    .y(function(d) { return y(d.close); });

var svg = d3.select("#analytics").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

function drawPowerGraph(data){

  svg.selectAll("g.y.axis").remove()
  svg.selectAll("g.y.axis").remove()

  data.forEach(function(d) {
    d.date = parseDate(d[0]);
    d.close = +d[1];
  });
  var start = d3.extent(data, function(d) { return d.date; })[0]
  twoMoreHours = d3.time.minute.offset(start, +20)

  x.domain([start, twoMoreHours])
  //y.domain(d3.extent(data, function(d) { return d.close; }));
  y.domain([0, 80])

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

  svg.append("path")
      .datum(data)
      .attr("class", "line")
      .attr("d", line)
      .style("stroke", getRandomColor())
}

function type(d) {
  d.date = formatDate.parse(d.date);
  d.close = +d.close;
  return d;
}
function getRandomColor() {
    var letters = '0123456789ABCDEF'.split('');
    var color = '#';
    for (var i = 0; i < 6; i++ ) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}
