$(document).ready(function() {

  var selectedMarker;
  var markers = [];

  //- - - - - - - - - - - - - - - - - - - - - - - - - - - -Set up Map  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
  var map = L.map('map').setView([33.3059398, -111.6792469], 13);

  L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox.streets',
    accessToken: 'pk.eyJ1Ijoia2V2ZXJseSIsImEiOiJjaWtrY3J4MXgwYXlndWRtNmFvbjhjM252In0.QWdPrZOYKI9dd4KB6CHhDw'
  }).addTo(map);

  for (pi of pi_list){
    var marker = L.marker([pi.fields.latitude, pi.fields.longitude]).addTo(map);
    marker.on('click', function(e) {
      selectedMarker = this.getLatLng()

      $.getJSON('/ASUi3dea/get_pi_data', {lat: selectedMarker.lat, lng: selectedMarker.lng}, function(data, jqXHR){
        $("#inverters").empty()
        for(inverter of data){
          $("#inverters").append('<li><a href="/ASUi3dea/'+inverter.pk+'"><span>'+inverter.pk+'</span></a></li>')
        }
      });
    });
  };

  //- - - - - - - - - - - - - - - - - - - - - - - - - - - - Set up Controls - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
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
});
