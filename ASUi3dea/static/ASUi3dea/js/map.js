$(document).ready(function() {

  //- - - - - - - - - - - - - - - - - - - - - - - - - - - - Set State Data  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
//   if (typeof stateValues != "undefined"){
//   for (var curState in stateValues){
//     if (stateValues.hasOwnProperty(curState)){
//       for(state of statesData["features"]){
//         if (state["properties"]["name"] == curState){
//           state["properties"]["density"] = stateValues[curState]
//         }
//       }
//     }
//   }
// }
  //- - - - - - - - - - - - - - - - - - - - - - - - - - - -Drop Down  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  for (model of available_models){
    $("#data-types-dropdown").append('<li><a href="/ASUi3dea/authUser/choropleth/'+model+'"><span>'+model+'</span></a></li>')
  }

  //- - - - - - - - - - - - - - - - - - - - - - - - - - - -Set up Map  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  var selectedMarker;
  var markers = [];
  var map = L.map('map').setView([33.3059398, -111.6792469], 4);

  L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox.streets',
    accessToken: 'pk.eyJ1Ijoia2V2ZXJseSIsImEiOiJjaWtrY3J4MXgwYXlndWRtNmFvbjhjM252In0.QWdPrZOYKI9dd4KB6CHhDw'
  }).addTo(map);

  //L.geoJson(statesData).addTo(map);

  for (pi of pi_list){
    var marker = L.marker([pi.fields.latitude, pi.fields.longitude], {riseOnHover: true}).addTo(map);
    marker.on('click', function(e) {
      selectedMarker = this.getLatLng()

      $.getJSON('/ASUi3dea/get_pi_data', {lat: selectedMarker.lat, lng: selectedMarker.lng}, function(data, jqXHR){
        $("#inverters").empty()
        for(inverter of data){
          $("#inverters").append('<a href="/ASUi3dea/'+inverter.pk+'" class="list-group-item"><span>'+inverter.pk+'</span></a>')
        }
      });
    });
  };


  //- - - - - - - - - - - - - - - - - - - - - - - - - - - - Map choropleth Style - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  // function getColor(d) {
  //     return d > 1000 ? '#800026' :
  //            d > 500  ? '#BD0026' :
  //            d > 200  ? '#E31A1C' :
  //            d > 100  ? '#FC4E2A' :
  //            d > 50   ? '#FD8D3C' :
  //            d > 20   ? '#FEB24C' :
  //            d > 10   ? '#FED976' :
  //                       '#FFEDA0';
  // }
  //
  // function style(feature) {
  //   return {
  //       fillColor: getColor(feature.properties.density),
  //       weight: 2,
  //       opacity: 1,
  //       color: 'white',
  //       dashArray: '3',
  //       fillOpacity: 0.7
  //   };
  // }
  //
  // L.geoJson(statesData, {
  //   style: style,
  //   onEachFeature: function (feature, layer) {
  //       layer.bindPopup(feature.properties.description);
  //   }
  // }).addTo(map);
  //
  // //- - - - - - - - - - - - - - - - - - - - - - - - - - - - choropleth overing and clicking - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  // function highlightFeature(e) {
  //     var layer = e.target;
  //
  //     layer.setStyle({
  //         weight: 5,
  //         color: '#666',
  //         dashArray: '',
  //         fillOpacity: 0.7
  //     });
  //
  //     if (!L.Browser.ie && !L.Browser.opera) {
  //         layer.bringToFront();
  //     }
  //     info.update(layer.feature.properties);
  // }
  //
  // var geojson;
  // // ... our listeners
  // function resetHighlight(e) {
  //   geojson.resetStyle(e.target);
  //   info.update();
  // }
  // function zoomToFeature(e) {
  //     map.fitBounds(e.target.getBounds());
  // }
  // function onEachFeature(feature, layer) {
  //   layer.on({
  //       mouseover: highlightFeature,
  //       mouseout: resetHighlight,
  //       click: zoomToFeature
  //   });
  // }
  //
  // var info = L.control();
  //
  // info.onAdd = function (map) {
  //     this._div = L.DomUtil.create('div', 'info'); // create a div with a class "info"
  //     this.update();
  //     return this._div;
  // };
  //
  // // method that we will use to update the control based on feature properties passed
  // info.update = function (props) {
  //     this._div.innerHTML = '<h4>US Population Density</h4>' +  (props ?
  //         '<b>' + props.name + '</b><br />' + props.density + ' people / mi<sup>2</sup>'
  //         : 'Hover over a state');
  // };
  //
  // info.addTo(map);
  //
  // geojson = L.geoJson(statesData, {
  //     style: style,
  //     onEachFeature: onEachFeature
  // }).addTo(map);
  //
  // //- - - - - - - - - - - - - - - - - - - - - - - - - - - - choropleth Map Legend - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  //
  // var legend = L.control({position: 'bottomright'});
  //
  // legend.onAdd = function (map) {
  //
  //   var div = L.DomUtil.create('div', 'info legend'),
  //       grades = [0, 10, 20, 50, 100, 200, 500, 1000],
  //       labels = [];
  //
  //   // loop through our density intervals and generate a label with a colored square for each interval
  //   for (var i = 0; i < grades.length; i++) {
  //       div.innerHTML +=
  //           '<i style="background:' + getColor(grades[i] + 1) + '"></i> ' +
  //           grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '<br>' : '+');
  //   }
  //
  //   return div;
  // };
  //
  // legend.addTo(map);
  //- - - - - - - - - - - - - - - - - - - - - - - - - - - - Zooming - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
/*
  map.on('zoomend', function() {
      if (map.getZoom() === 13) {

          map.featureLayer.setFilter(function() { return true; });
      } else {
          //map.featureLayer.setFilter(function() { return false; });
      }
  });
  */

  //- - - - - - - - - - - - - - - - - - - - - - - - - - - - Set up Controls - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
/*
  $("[name='on_off']").bootstrapSwitch();

  var frm = $('#controlFrm')
  frm.submit(function () {
    try {
      var pk = selectedMarker['pk']
      $.ajax({
          type: frm.attr('method'),
          url: frm.attr('action'),
          data: frm.serialize() + '&pk=' + pk,
          success: function (data) {
            window.alert(data);
          },
          error: function(data) {
            window.alert('error')
          }
      });//end ajax
    }
    catch(err) {
        window.alert('Point not selected')
    }
    return false; //form won't resolve to new page
  })
  */
});
