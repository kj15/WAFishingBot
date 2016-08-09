function initialize() {

  var start = new google.maps.LatLng(47.5569369,-122.7855197)
  var mapOptions = {
      zoom: 8,
      center: start,
      mapTypeId: google.maps.MapTypeId.ROADMAP
  }

  var map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

  var markers = [];
  var infoWindowContent = [];
  var infoWindow = new google.maps.InfoWindow(), marker, i;
  
  $.getJSON("lakes.json", function(json1) {
    $.each(json1, function(key, data) {
        var latLng = new google.maps.LatLng(data.latitude, data.longitude); 
        // Creating a marker and putting it on the map
        var marker = new google.maps.Marker({
            position: latLng,
            map: map,
            title: data.name
        });
		markers.push(marker);
		infoWindowContent.push(data.stocking_info);
    });
	
	for(i = 0; i < markers.length; i++) {
      var marker = new google.maps.Marker({
          position: new google.maps.LatLng(markers[i][1],markers[i][2]), 
          map: map,
          title: markers[i][0],
          //icon: new google.maps.MarkerImage("http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|" + markers[i][3], new google.maps.Size(21, 34), new google.maps.Point(0,0), new google.maps.Point(10, 34))
      });
      google.maps.event.addListener(marker, 'click', (function(marker, i) {
        return function() {
          infoWindow.setContent(infoWindowContent[i]);
          infoWindow.open(map, marker);
        }
      })(marker, i));
    }
   });
}
  /*
  getFileFromServer("lakes.csv", function(text) {

    if (text === null)
      return

    rows = text.split("\n");
    var headers= rows[0].split("\t");

    markers = [];
    infoWindowContent = [];

    for(i = 1; i < rows.length; i++) {
      // row 0: ID of sample (title) 44563383.3.txt
      // row 13: coordinates
      //
	  
      var cols = rows[i].split(",");
      if(cols.length == 1)
        continue;

      var lat = cols[4]
      var lon = cols[6]

      var contentString = "<b>" + cols[0] + "</b><br>";
      for(j = 1; j < cols.length; j++) {
        if(cols[j] != "NA" && cols[j] != "na")
        contentString = contentString + headers[j] + ":" + cols[j] + "<br>";
      }
      
      switch(cols[2]) {
        case "water":
          color = "80D0FF"
          break;
        case "soil":
          color = "D0B060"
          break;
        default:
          color = "E0E0E0"
      }

      markers.push([cols[0], lat, lon, color])
      infoWindowContent.push(contentString);
    }


    var infoWindow = new google.maps.InfoWindow(), marker, i;

    for(i = 0; i < markers.length; i++) {
      var marker = new google.maps.Marker({
          position: new google.maps.LatLng(markers[i][1],markers[i][2]), 
          map: map,
          title: markers[i][0],
          icon: new google.maps.MarkerImage("http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=%E2%80%A2|" + markers[i][3], new google.maps.Size(21, 34), new google.maps.Point(0,0), new google.maps.Point(10, 34))
      });
      google.maps.event.addListener(marker, 'click', (function(marker, i) {
        return function() {
          infoWindow.setContent(infoWindowContent[i]);
          infoWindow.open(map, marker);
        }
      })(marker, i));
    }

 });

}*/

google.maps.event.addDomListener(window, 'load', initialize);



