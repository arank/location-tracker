/*Created by Aran Khanna (with some help from the interwebz), All Rights Reserved*/

L.mapbox.accessToken = 'pk.eyJ1IjoiYXJhbmtoYW5uYSIsImEiOiJEdDJreGxjIn0.Y3-LSV20SRRZOzs_6nSFjA';
// Set scene to default home
var map = L.mapbox.map('map', 'arankhanna.lnl5mal6')
 .setView([42.381982, -71.124694], 12);

var layers = document.getElementById('menu-ui');

// Always add the home layer
var home_layer = L.mapbox.featureLayer({
    type: 'Feature',
    geometry: {
        type: 'Point',
        // coordinates here are in longitude, latitude order because
        coordinates: [
          -71.124694,
          42.381982 
        ]
    },
    properties: {
        title: 'My Home',
        description: 'My base for various mischief',
        'marker-size': 'large',
        'marker-color': '#dd1818',
        'marker-symbol': 'building'
    }
}); 
addLayer(home_layer, 'home', [42.381982, -71.124694], 2);

// Try to pull last location, if it succeeds add the layer
$.ajax({
   type: "GET",
   url: 'http://ec2-52-11-173-4.us-west-2.compute.amazonaws.com/location-tracker',
   dataType: 'text',
   success: function (data) {
      data_obj = JSON.parse(data);
      var date =  new Date(data_obj['time']);
      var travel_layer = L.mapbox.featureLayer({
         type: 'Feature',
         geometry: {
            type: 'Point',
            // coordinates here are in longitude, latitude order because
            coordinates: [
              data_obj['approx-long'],
              data_obj['approx-lat']
            ]
         },
         properties: {
            title: 'Aran\'s Last Recorded Position - '+ date.toGMTString(),
            description: data_obj['location'],
            'marker-size': 'large',
            'marker-color': '#dd1818',
            'marker-symbol': 'rocket'
         }
      });
      addLayer(travel_layer, 'current', [data_obj['approx-lat'], data_obj['approx-long']], 1);
   }
});

function addLayer(layer, name, coords, zIndex) {
    layer
        .setZIndex(zIndex)
        .addTo(map);

    // Create a simple layer switcher that
    // toggles layers on and off.
    var link = document.createElement('a');
        link.href = '#';
        link.className = 'active';
        link.id = name;
        link.innerHTML = name;

    link.onclick = function(e) {
         e.preventDefault();
         e.stopPropagation();
         map.addLayer(layer);
         this.className = 'active';
         map.setView(coords, 15);
    };

    layers.appendChild(link);
}