$(document).ready(function() {

  //- - - - - - - - - - - - - - - - - - - - - - - - - - - -Drop Down  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  // for (model of available_models){
  //   $("#data-types-dropdown").append('<li><a href="/ASUi3dea/authUser/choropleth/'+model+'"><span>'+model+'</span></a></li>')
  // }

  //- - - - - - - - - - - - - - - - - - - - - - - - - - - -Set up Map  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  var selectedMarker;
  var map = L.map('map').setView([34.3059398, -111.6792469], 7);

  var redIcon = L.icon({
    iconUrl: "/static/ASUi3dea/media/redMarker.png",
    shadowUrl: "/static/ASUi3dea/media/shadow.png",

    iconSize:     [24, 40], // size of the icon
    shadowSize:   [31, 35], // size of the shadow
    iconAnchor:   [12, 40], // point of the icon which will correspond to marker's location
    shadowAnchor: [10, 35],  // the same for the shadow

});

  L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox.streets',
    accessToken: 'pk.eyJ1Ijoia2V2ZXJseSIsImEiOiJjaWtrY3J4MXgwYXlndWRtNmFvbjhjM252In0.QWdPrZOYKI9dd4KB6CHhDw'
  }).addTo(map);

  var markers = L.markerClusterGroup({ spiderfyOnMaxZoom: false, showCoverageOnHover: true, zoomToBoundsOnClick: true, animate: true });
  var oneOpacityMarkers = []

  //L.geoJson(statesData).addTo(map);

  // - - - - - - - - - - - - - - - - - - - - - - - - - - - - Groups - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  for (group of groups){
    $("#groups").append(createGroup(group.name))

      for (i in group.inverters){
        var currentInv = group.inverters[i]
        $('#'+group.name+'').children("ul").append('<a class="list-group-item">'+currentInv.inverterName+' </a>')
      }

      $('#'+group.name+'').on('show.bs.collapse', function () {

      })
  }

  function addToGroup(event){
    var currentInverters = []

    $("#inverters").children().each(function(index){
      var thisText = $( this ).text()
      currentInverters.push(thisText)
    })

    $.post('/ASUi3dea/add_to_group/', {'group': event.data.name, 'inverters[]': currentInverters, 'csrfmiddlewaretoken': csrfToken})
  }

  $("#groups").append('<button class="list-group-item btn btn-secondary" id="create-group-button"> Create Group </button>')

  function createGroup(groupName){
    $("#group-dropdown").append(`<li><a id="`+groupName+`-drop"href="#">`+groupName+`</a></li>`)
    $("#"+groupName+"-drop").on('click', {name: groupName}, addToGroup);

    return `<div class="panel panel-default" id="navigator" >
          <div class="panel-heading">
          <h4 class="panel-title">
            <a data-toggle="collapse" href="#`+groupName+`">`+groupName+`</a>
          </h4>
        </div>
        <div id="`+groupName+`" class="panel-collapse collapse">
          <ul class="list-group nav nav-pills nav-stacked" style="padding: 5px;">

          </ul>
        </div>
      </div>`
  }

  $("#create-group-button").on('click', function(e){
    var secondElement = $("#create-group-button");
    var newIndex = secondElement.index() + 1
    $(secondElement).before(createGroup("testname" + newIndex));
  });

  // - - - - - - - - - - - - - - - - - - - - - - - - -  - Marker Selection - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  map.on('boxzoomend', function(e) {
    deselectMarkers()
    var layers = markers._featureGroup._layers
    for (var i in layers) {
      if (e.target.getBounds().contains(layers[i]._latlng)) {
        if (layers[i]._markers !== undefined){//this means it is a cluster, so we do a selctMarker for each marker in cluster
          for (child of layers[i].getAllChildMarkers()){
            selectMarker(child)
          }
        }else{
          selectMarker(layers[i])
        }

      }
    }
  });

  for (pi of pi_list){
    var marker = L.marker([pi.fields.latitude, pi.fields.longitude],  {riseOnHover: true, opacity: 0.5, icon: redIcon});
    marker.on('click', function(e) {
      map.setView(this._latlng)
      deselectMarkers()
      selectMarker(this)
    });
    selectMarker(marker)
    markers.addLayer(marker)
  };

  map.addLayer(markers)

  function deselectMarkers(){
    $("#inverters").empty()
    for (var i in oneOpacityMarkers){
      markers.removeLayer(oneOpacityMarkers[i])
      oneOpacityMarkers[i].options.opacity = 0.5
      oneOpacityMarkers[i].options.zIndexOffset = 1.0
      markers.addLayer(oneOpacityMarkers[i])
    }
    oneOpacityMarkers = []
  }

  function selectMarker(m){
    //add to right list
    $.getJSON('/ASUi3dea/get_pi_data', {lat: m._latlng.lat, lng: m._latlng.lng}, function(data, jqXHR){
      for(inverter of data){
        $("#inverters").prepend('<a href="/ASUi3dea/'+inverter.pk+'" class="list-group-item">'+inverter.fields.custom_name+'</a>')
      }
    });
    markers.removeLayer(m)
    m.options.opacity = 1.0
    m.options.zIndexOffset = 1000
    markers.addLayer(m)
    oneOpacityMarkers.push(m)
  }
});
