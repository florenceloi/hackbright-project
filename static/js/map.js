function initMap() {

    // Specify where the map is centered
    var myLatLng = {lat: 72, lng: -140};

    // Create a map object and specify the DOM element for display.
    // center and zoom are required.
    var map = new google.maps.Map(document.getElementById('map'), {
        center: myLatLng,
        zoom: 5,
    });

}

google.maps.event.addDomListener(window, 'load', initMap);