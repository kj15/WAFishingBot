var map;

function initialize() {
    var lat = 47.5569369
    var long = -122.7855197
    var zoom = 17
    var isIE = navigator.userAgent.toLowerCase().indexOf('trident') > -1;

  var start = new google.maps.LatLng(lat,long)
  var mapOptions = {
      zoom: zoom,
      center: start,
      mapTypeId: google.maps.MapTypeId.TERRAIN
  }

  map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

}

google.maps.event.addDomListener(window, 'load', initialize);
