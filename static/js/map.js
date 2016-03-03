"use strict";

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

  // Color heart red when restaurant is favorited
  $('.favorite-btn').click(colorHeart);

  // Instantiate geocoder object
  var geocoder = new google.maps.Geocoder();

  // Call geocodeCity when "Center map" button is clicked
  $('#city').change(function() {
    geocodeCity(geocoder, map);
  });

  var locationInfoWindow = new google.maps.InfoWindow({
  });

  // Recenter map on current location
  $('#current-location').click(function() {
    centerOnGeolocation(locationInfoWindow, map);
  });
}


function addRestaurantMarkers(map) {
  var markers = [];

  // Instantiate info windows
  var infoWindow = new google.maps.InfoWindow();

  // Retrieve the jsonified Python dictionary of restaurants with AJAX
  $.get('/home.json', function (restaurants_dict) {

    var restaurants = restaurants_dict["restaurants"];

    // Looping over each restaurant in dictionary,
    // make marker, push marker to markers array,
    // define content of info window and bind to marker.
    for (var i = 0; i < restaurants.length; i++) {
      var restaurant = restaurants[i];
      var marker = makeMarker(restaurant, map);
      markers.push(marker);
      var html = makeInfoWindow(restaurant);
      bindInfoWindow(marker, map, infoWindow, html, restaurant);
    }

    // Show all markers of a particular category
    var show = function (category) {

      // Loop over each restaurant in dictionary
      for (var i = 0; i < restaurants.length; i++) {
        var restaurant = restaurants[i];
        if (restaurant.category == category) {
          markers[i].setVisible(true);
        }
      }
    };

    // Hide all markers of a particular category
    var hide = function (category) {
      // Loop over each restaurant in dictionary
      for (var i = 0; i < restaurants.length; i++) {
        var restaurant = restaurants[i];
        if (restaurant.category == category) {
          markers[i].setVisible(false);
        }
      }
    };
    
    $(".category").change(function () {
      var cat = $(this).attr("value");
      if ($(this).is(":checked")) {
        show(cat);
      } else {
        hide(cat);
      }
    });

    $("#selectAll").click(function() {
      var all = $(this);
      $('input:checkbox').each(function() {
        $(this).prop("checked", all.prop("checked"));
        $(this).change();
      });
    });
  });
}


// Instantiate marker for each restaurant
function makeMarker(restaurant, map) {
  var temp_marker = new google.maps.Marker({
  position: new google.maps.LatLng(restaurant.lat, restaurant.lng),
  map: map,
  title: restaurant._name,
  icon: '/static/img/paw.png',
  visible: true,
  });
  return temp_marker;
}


// Define the content of the infoWindow for each restaurant
function makeInfoWindow(restaurant) {
  var temp_html = (
    '<div class="window-content">' +
      '<h3><b>' + restaurant._name + '</b></h3>' +
      '<img src="' + restaurant.yelpImgUrl + '" alt="' + restaurant._name +
        '" style="width:150px;"><br>' +
      '<p><b>Address: </b>' + restaurant.address + '</p>' +
      '<p><b>Phone Number: </b>' + restaurant.phone + '</p>' +
      '<p><b>Yelp Rating: </b><img src="' + restaurant.yelpRatingImg +
        '" alt="' + restaurant.yelpRating + '">' +
        ' (' + restaurant.reviewCount + ' reviews) </p>' +
      '<a href="' + restaurant.yelpUrl +
        '"> <img src="/static/img/yelp_review_btn_red.png" alt="' +
        restaurant._name + '" style="width:125px;"></a>' +
      '<p><button id="' + restaurant.db_id + '" class="favorite-btn" value="' +
          restaurant.favorite + '">' + '&hearts; Favorite</button></p>' +
      '<a href="/restaurants/' + restaurant.db_id + '">Review ' + restaurant._name + '</a>' +
    '</div>'
  );
  return temp_html;
}


// Processes restaurant info windows
function bindInfoWindow(marker, map, infoWindow, html, restaurant) {
  google.maps.event.addListener(marker, 'click', function () {
    infoWindow.close();
    infoWindow.setContent(html);
    infoWindow.open(map, marker);
    checkFavorites(marker, restaurant.db_id, restaurant.favorite);
    $('.favorite-btn').click(colorHeart);
  });
}


function checkFavorites(marker, id, isFavorited) {
  if (isFavorited === true) {
    $('#' + id).css('color', 'red');
  }
}


// Color heart red when favorited
function colorHeart(evt) {
  var id = this.id;
    if ($('#' + id).css('color') === "rgb(255, 0, 0)") {
      $('#' + id).css('color', 'black');
      console.log("not anymore...");
    } else {
      $('#' + id).css('color', 'red');
      console.log("now it's red!");
    }
}


// Processes geocode
function geocodeCity(geocoder, resultsMap) {

  // Get address value from form
  var city = document.getElementById('city').value;
  
  // Make request to Geocoding service with city and execute anonymous callback method
  geocoder.geocode({'address': city}, function(results, status) {
    if (status === google.maps.GeocoderStatus.OK) {
      // Request may return multiple results; center on LatLng of first in list
      resultsMap.setCenter(results[0].geometry.location);
      var cityInfoWindow = new google.maps.InfoWindow({
        content: city,
        position: results[0].geometry.location,
      });
      cityInfoWindow.open(resultsMap);
    } else {
      alert('Centering on ' + city + ' was not successful for the following reason: ' + status);
    }
  });
}


// Centers on geolocation
function centerOnGeolocation(locationInfoWindow, map) {

  // Execute anonymous functions after getting current position
  navigator.geolocation.getCurrentPosition(function(position) {
    var pos = {
      lat: position.coords.latitude,
      lng: position.coords.longitude
    };

    locationInfoWindow.setPosition(pos);
    locationInfoWindow.setContent('Current location.');
    locationInfoWindow.setMap(map);
    locationInfoWindow.open(map);
    map.setCenter(pos);
  }, function(error) {
    alert('Error: ' + error.message);
  });
}
