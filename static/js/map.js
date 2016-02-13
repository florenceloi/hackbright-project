// Renders map populated with restaurants,
// allows centering on geocoding and current location
function initMap() {

    // Specify center of map
    var myLatLng = {lat: 37.788723, lng: -122.411460};

    // Instantiate a map object and specify the DOM element for display.
    var map = new google.maps.Map(document.getElementById('map'), {
        center: myLatLng,
        zoom: 13,
    });
    
    // Add restaurant markers
    addRestaurantMarkers(map);

    // Call geocodeAddress when "Center map" button is clicked
    $('#specified-location').submit(function() {
        geocodeAddress(map);
    });

    var locationInfoWindow = new google.maps.InfoWindow({
        map: map,
        animation: google.maps.Animation.DROP
    });
    locationInfoWindow.close();

    // Recenter map on current location
    $('#current-location').click(function() {
        centerOnGeolocation(locationInfoWindow, map);
        locationInfoWindow.open(map);
    });
}


function addRestaurantMarkers(map) {
    // Instantiate info windows
    var infoWindow = new google.maps.InfoWindow();

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

          // Define the content of the infoWindow
          html = (
              '<div class="window-content">' +
                  '<img src="' + restaurant.yelpImgUrl + '" alt="' + restaurant._name + '" style="width:150px;">' +
                  '<p><b>Restaurant: </b>' + restaurant._name + '</p>' +
                  '<p><b>Address: </b>' + restaurant.address + '</p>' +
                  '<p><b>Phone Number: </b>' + restaurant.phone + '</p>' +
                  '<p><b>Yelp Rating: </b><img src="' + restaurant.yelpRatingImg + '" alt="' + restaurant.yelpRating + '">' +
                  ' (' + restaurant.reviewCount + ' reviews) </p>' + '<a href="' + restaurant.yelp_url '" <img src="' + restaurant.yelpImgUrl + '" alt="' + restaurant._name + '" style="width:150px;">' +
              '</div>');

          // Inside the loop we call bindInfoWindow passing it the marker,
          // map, infoWindow and contentString
          bindInfoWindow(marker, map, infoWindow, html);
        }
    });
}


// Processes restaurant info windows
function bindInfoWindow(marker, map, infoWindow, html) {
    google.maps.event.addListener(marker, 'click', function () {
        infoWindow.close();
        infoWindow.setContent(html);
        infoWindow.open(map, marker);
    });
}


// Processes geocode
function geocodeAddress(resultsMap) {

    // Get address value from form
    var address = document.getElementById('address').value;
    console.log('works');
    
    // Instantiate geocoder object
    var geocoder = new google.maps.Geocoder();

    // Make request to Geocoding service with address and execute anonymous callback method
    geocoder.geocode({'address': address}, function(results, status) {
        if (status === google.maps.GeocoderStatus.OK) {
            // Request may return multiple results; center on LatLng of first in list
            resultsMap.setCenter(results[0].geometry.location);
            var marker = new google.maps.Marker({
                map: resultsMap,
                position: results[0].geometry.location
            });
            console.log('works');
        } else {
            alert('Centering on ' + address + ' was not successful for the following reason: ' + status);
        }
    });
}


// Centers on geolocation
function centerOnGeolocation(locationInfoWindow, map) {

    // If geolocation allowed:
    if (navigator.geolocation) {
        // Execute anonymous functions after getting current position
        navigator.geolocation.getCurrentPosition(function(position) {
            var pos = {
              lat: position.coords.latitude,
              lng: position.coords.longitude
            };

            locationInfoWindow.setPosition(pos);
            locationInfoWindow.setContent('Current location.');
            map.setCenter(pos);
        }, function() {
            handleLocationError(true, locationInfoWindow, map.getCenter());
        });
    } else {
        handleLocationError(false, locationInfoWindow, map.getCenter());
    }
}


// Handles centering on current location error
function handleLocationError(browserHasGeolocation, locationInfoWindow, pos) {
  locationInfoWindow.setPosition(pos);
  locationInfoWindow.setContent(browserHasGeolocation ?
                        'Error: The Geolocation service failed.' :
                        'Error: Your browser doesn\'t support geolocation.');
}

