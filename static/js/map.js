function initMap() {

    // Specify center of map
    var myLatLng = {lat: 37.788723, lng: -122.411460};

    // Instantiate a map object and specify the DOM element for display.
    var map = new google.maps.Map(document.getElementById('map'), {
        center: myLatLng,
        zoom: 13,
    });

    // Retrieve the jsonified Python dictionary of restaurants with AJAX
    $.get('/home.json', function (restaurants) {
        var restaurant, marker;

        // Loop over each restaurant in dictionary
        for (var key in restaurants) {
          restaurant = restaurants[key];

          // Instantiate marker for each restaurant
          marker = new google.maps.Marker({
              position: new google.maps.LatLng(restaurant.lat, restaurant.lng),
              map: map,
              title: restaurant._name,
              icon: '/static/img/paw.png'
              });
        }
    });

    // Instantiate geocoder object
    var geocoder = new google.maps.Geocoder();

    // Call geocodeAddress when "Center map" button is clicked
    $('#submit').click(function() {
        geocodeAddress(geocoder, map);
    });

    // Recenter map on current location
    $('#current-location').click(function() {
        centerOnCurrentLocation();
    });
}


function geocodeAddress(geocoder, resultsMap) {
  
    // Get address value from form
    var address = document.getElementById('address').value;
    
    // Make request to Geocoding service with address and execute anonymous callback method
    geocoder.geocode({'address': address}, function(results, status) {
        if (status === google.maps.GeocoderStatus.OK) {
            // Request may return multiple results; center on LatLng of first in list
            resultsMap.setCenter(results[0].geometry.location);
            var marker = new google.maps.Marker({
                map: resultsMap,
                position: results[0].geometry.location
            });
        } else {
            alert('Centering on ' + address + ' was not successful for the following reason: ' + status);
        }
    });
}


function centerOnCurrentLocation() {
    // If geolocation allowed:
    if (navigator.geolocation) {
        // Execute anonymous functions after getting current position
        navigator.geolocation.getCurrentPosition(function(position) {
            var pos = {
              lat: position.coords.latitude,
              lng: position.coords.longitude
            };

            infoWindow.setPosition(pos);
            infoWindow.setContent('Location found.');
            map.setCenter(pos);
        }, function() {
            handleLocationError(true, infoWindow, map.getCenter());
        });
    } else {
        handleLocationError(false, infoWindow, map.getCenter());
    }
}

// Render map once window finishes loading
google.maps.event.addDomListener(window, 'load', initMap);