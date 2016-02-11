function initMap() {

    // Specify center of map
    var myLatLng = {lat: 37.788723, lng: -122.411460};

    // Create a map object and specify the DOM element for display.
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
}

google.maps.event.addDomListener(window, 'load', initMap);