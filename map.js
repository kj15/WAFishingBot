var markers = [];
var infoWindowContent = [];
var infoWindow = new google.maps.InfoWindow();
var map;
var lakes = [];

function initialize() {

  var start = new google.maps.LatLng(47.5569369,-122.7855197)
  var mapOptions = {
      zoom: 8,
      center: start,
      mapTypeId: google.maps.MapTypeId.ROADMAP
  }

  map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
  $.getJSON("lakes.json", function(json1) {
	 $.each(json1, function(key, value) {
		lakes.push(value);
	 });
	 plot();
   });
}


function plot() {

	$.each(lakes, function(key, data) {
        var latLng = new google.maps.LatLng(data.latitude, data.longitude); 
        // Creating a marker and putting it on the map
        var marker = new google.maps.Marker({
            position: latLng,
            map: map,
            title: data.name
        });
		markers.push(marker);
		var content = '<h2>' + data.name + '</h2><br/><p>' + data.alt + ' ft</p><br/><p>' + data.size + ' acres</p><br/><p>Last stocked: <bold>' + data.last_stocked_date + '</bold></p><br/><p>Last stocked amount: <bold>' + data.last_stocked_amt + '</bold></p>'
	    marker.addListener('click', function() {
          infoWindow.setContent(content)
		  infoWindow.open(map, marker);
        });
	  
    });
}
  
google.maps.event.addDomListener(window, 'load', initialize);



