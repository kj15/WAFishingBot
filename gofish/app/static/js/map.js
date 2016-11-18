'use strict';

//Globals
var map;
var sizeSlider = $('#size').slider({});
var altSlider = $('#altitude').slider({});
var rankSlider = $('#rank').slider({});

//Pre-load
setQueryDefaults();

    function setQueryDefaults() {
        $.ajax({
			url: "/api/query/defaults",
			type: "GET",
			dataType: "html",
			success: function (data) {
			    data = JSON.parse(data);
			    console.log(data);
			    //show top
			    var rank = $('#rank');
			    rankSlider.slider('setValue', data.rank);
			    rankSlider.slider('setAttribute', 'max', data.total);

                //county options
                var county = $('#county');
                var countyList = data.countyList.split(',');
                function addCountyOption(c) {
                    if(c == data.county) { county.append("<option selected value=" + c + ">" + c + "</option>");}
                    else { county.append("<option value=" + c + ">" + c + "</option>");}
                }
                addCountyOption('All');
                $.each(countyList, function(i,v) {
                    addCountyOption(v);
                });
			},
			error: function (data) {
				console.log("Failure");
			}
		});
    }


function initialize() {
    var lat = 47.5846913
    var long = -121.4482443
    var zoom = 8
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

$(document).ready(function() {
    var focusOutIDs = [
        '#map-canvas',
    ]

    //sliders();
    bindings();


    function sliders() {
        sizeSlider = $('#size').slider({});
        altSlider = $('#altitude').slider({});
        rankSlider = $('#rank').slider({});
//        $('#size').on('slide', function(event) {
//            $('#size-val').text(event.value);
//        });
    }

    function bindings() {
        //Navbar growth on search focus
        $('#main-nav input').on('focus', function(){
            if(!$('#navbar-lower').hasClass('collapse in')) {
                $('#collapse').trigger('click');
            }
        });

        //Navbar shrink on search focusout
        $(function() {
            $(focusOutIDs.join(' ')).on('click', function(event) {
                //not collapsed
                if($('#navbar-lower').hasClass('collapse in')) {
                    $('#collapse').trigger('click');
                }

            });
        })

    }

})