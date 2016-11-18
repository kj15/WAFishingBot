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
			    
                //search
                $('#search').attr('placeholder', data.name);

			    //show top
			    rankSlider.slider('setValue', data.rank);
			    rankSlider.slider('setAttribute', 'max', data.total);

                //size
                sizeSlider.slider('setAttribute', 'max', data.maxSize);
                sizeSlider.slider('setAttribute', 'min', data.minSize);
                sizeSlider.slider('setValue', [data.minSize,data.maxSize]);

                //size
                altSlider.slider('setAttribute', 'max', data.maxAlt);
                altSlider.slider('setAttribute', 'min', data.minAlt);
                altSlider.slider('setValue', [data.minAlt,data.maxAlt]);

                //select options
                function addSelectOptions(s) {
                    var select = $('#' + s);
                    var list = data[s + 'List'].split(',');
                    function addOption(o) {
                        if(o == data[s]) { select.append("<option selected value=" + o + ">" + o + "</option>");}
                        else { select.append("<option value=" + o + ">" + o + "</option>");}
                    }
                    addOption('All');
                    $.each(list, function(i,v) {
                        addOption(v);
                    });
                 }

                 //county
                 addSelectOptions('county');

                 //fish
                 addSelectOptions('fish');
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