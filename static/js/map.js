// Sample data from Hackbright lecture. Repopulate with project information.

function initMap() {

  // Specify where the map is centered
  // Defining this variable outside of the map optios markers
  // it easier to dynamically change if you need to recenter
  var myLatLng = {lat: 37.788613, lng: -122.411431};

  // Create a map object and specify the DOM element for display.
  var map = new google.maps.Map(document.getElementById('map'), {
    center: myLatLng,
    // scrollwheel: false,
    zoom: 5,
    // zoomControl: true,
    // panControl: false,
    // streetViewControl: false,
    // styles: MAPSTYLES,
    // mapTypeId: google.maps.MapTypeId.TERRAIN
  });

  // --------------------------------------------------------------//
  // --------------------------------------------------------------//
  // If you want to create a StyledMapType to make a map type control
  // create it like this:

  // Create a new StyledMapType object, passing it the array of styles,
  // as well as the name to be displayed on the map type control.
  // var styledMap = new google.maps.StyledMapType(
  //     MAPSTYLES,
  //     {name: "Custom Style"}
  // );
  // You would then set 'styles' in the mapoptions to 'styledMap'

  // Associate the styled map with the MapTypeId and set it to display.
  // map.mapTypes.set('map_style', styledMap);
  // map.setMapTypeId('map_style');
  // --------------------------------------------------------------//
  // --------------------------------------------------------------//


  // // Define global infoWindow
  // // If you do this inside the loop where you retrieve the json,
  // // the windows do not automatically close when a new marker is clicked
  // // and you end up with a bunch of windows opened at the same time.
  // // What this does is create one infowindow and we replace the content
  // // inside for each marker.
  // var infoWindow = new google.maps.InfoWindow({
  //     width: 150
  // });

  // // Retrieving the information with AJAX
  // $.get('/bears.json', function (bears) {
  //     // Attach markers to each bear location in returned JSON
  //     // JSON looks like:
  //     // {
  //     //  "1": {
  //     //    "bearId": "1737",
  //     //    "birthYear": "1970",
  //     //    "capLat": "70.71139573",
  //     //    "capLong": "-147.8381939",
  //     //    "capYear": "2001",
  //     //    "collared": "true",
  //     //    "gender": "F"
  //     //   },...
  //     // }
  //     var bear, marker, html;

  //     for (var key in bears) {
  //         bear = bears[key];

  //         // Define the marker
  //         marker = new google.maps.Marker({
  //             position: new google.maps.LatLng(bear.capLat, bear.capLong),
  //             map: map,
  //             title: 'Bear ID: ' + bear.bearId,
  //             icon: '/static/img/polar.png'
  //         });

  //         // Define the content of the infoWindow
  //         html = (
  //             '<div class="window-content">' +
  //                 '<img src="/static/img/polarbear.jpg" alt="polarbear" style="width:150px;" class="thumbnail">' +
  //                 '<p><b>Bear gender: </b>' + bear.gender + '</p>' +
  //                 '<p><b>Bear birth year: </b>' + bear.birthYear + '</p>' +
  //                 '<p><b>Year captured: </b>' + bear.capYear + '</p>' +
  //                 '<p><b>Collared: </b>' + bear.collared + '</p>' +
  //                 '<p><b>Location: </b>' + marker.position + '</p>' +
  //             '</div>');

  //         // Inside the loop we call bindInfoWindow passing it the marker,
  //         // map, infoWindow and contentString
  //         bindInfoWindow(marker, map, infoWindow, html);
  //     }

  // });

//   // This function is outside the for loop.
//   // When a marker is clicked it closes any currently open infowindows
//   // Sets the content for the new marker with the content passed through
//   // then it open the infoWindow with the new content on the marker that's clicked
//   function bindInfoWindow(marker, map, infoWindow, html) {
//       google.maps.event.addListener(marker, 'click', function () {
//           infoWindow.close();
//           infoWindow.setContent(html);
//           infoWindow.open(map, marker);
//       });
//   }
}

google.maps.event.addDomListener(window, 'load', initMap);