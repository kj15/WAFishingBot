var markers = [];
var infoWindowContent = [];
var infoWindow = new google.maps.InfoWindow();
var map;

var lakes = [];

var filters = {
	search: "",
	county : "",
	min_size: 0,
	max_size: 0,
	min_alt: 0,
	max_alt: 0,
	top_rank: 0,
}

function initialize() {

  var start = new google.maps.LatLng(47.5569369,-122.7855197)
  var mapOptions = {
      zoom: 8,
      center: start,
      mapTypeId: google.maps.MapTypeId.ROADMAP
  }

  map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
  $.getJSON("ranked_lakes.json", function(json1) {
	 $.each(json1, function(key, value) {
		lakes.push(value);
	 });
	 plot();
	//sorting based on rank
	markers.sort(sortRank);
   });
}


function plot() {

	$.each(lakes, function(key, data) {
        var latLng = new google.maps.LatLng(data.latitude, data.longitude); 
        // Creating a marker and putting it on the map
        var marker = new google.maps.Marker({
            position: latLng,
            map: map,
            title: data.name,
			data: data
        });
		markers.push(marker);
		var content = '<div class="iwindow"><h2>' + data.name + '</h2><br/><p>' + data.alt + ' ft</p><br/><p>' + data.size + ' acres</p><br/><p>Last stocked: <bold>' + data.last_stocked_date + '</bold></p><br/><p>Last stocked amount: <bold>' + data.last_stocked_amt + '</bold></p><br/><p>Rank: ' + data.rank +'</p></div>'
	    marker.addListener('click', function() {
          infoWindow.setContent(content)
		  infoWindow.open(map, marker);
        });	  
    });
	
}

function sortRank(a, b) {
	if(a.data.rank < b.data.rank) return 1;
	if(a.data.rank > b.data.rank) return -1;
	return 0;
}

function filter() {
	var i = j = k = 0;
	$.each(markers, function(key, marker) {
		switch(true) {
			//rank
			case key >= parseInt(filters.top_rank):
				marker.setVisible(false);
				break;
		
			//name
			case filters.search != "" && marker.data.name.indexOf(filters.search) == -1:
				marker.setVisible(false);
				break;
		
			//county
			case filters.county_list != "" && filters.county_list + " County" != marker.data.county:
				i++;
				marker.setVisible(false);
				break;
				
			//size	
			case parseFloat(filters.min_size) > parseFloat(marker.data.size):
			case parseFloat(filters.max_size) < parseFloat(marker.data.size):
				j++;
				marker.setVisible(false);
				break;
			
			//altitude
			case parseInt(filters.min_alt) > parseInt(marker.data.alt):
			case parseInt(filters.max_alt) < parseInt(marker.data.alt):
				k++;
				marker.setVisible(false);
				break;
				
			default:
				marker.setVisible(true);
				break;
		}	
	});
	console.log(i);
	console.log(j);
	console.log(k);
}


google.maps.event.addDomListener(window, 'load', initialize);

$( document ).ready(function() {
    
	//bindings
	$("#submit").click(function(){
		filters.search = $("#lake_name").val();
		filters.county_list = $("#county_list").val();
		filters.min_size = $("#size_min").val();
		filters.max_size = $("#size_max").val();
		filters.min_alt = $("#height_min").val();
		filters.max_alt = $("#height_max").val();
		filters.top_rank = $("#top_rank").val();
		console.log(filters);
		filter();
	});
	
	$("#county_list").click(function(){
		$(this).removeAttr('value');
	});
	
});

