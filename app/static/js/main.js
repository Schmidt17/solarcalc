document.addEventListener('DOMContentLoaded', function() {
     var tab_elems = document.querySelectorAll('.tabs');
     var tab_instance = M.Tabs.init(tab_elems);

     var datepicker_elems = document.querySelectorAll('.datepicker');
     var datepicker_instances = M.Datepicker.init(datepicker_elems, {autoClose: true});
});

var currentCoords = [];
function setCurrentCoords(newCoords) {
    currentCoords = newCoords;

    let formElt = document.getElementById("coordinates");
    formElt.value = JSON.stringify(currentCoords);
}

const ddCoords = [13.737262, 51.050407];
setCurrentCoords(ddCoords);
var view = new ol.View({
    center: ol.proj.fromLonLat(ddCoords),
    zoom: 12
});

var tileLayer = new ol.layer.Tile({source: new ol.source.OSM()});
var markerLayer = new ol.layer.Vector({
    source: new ol.source.Vector(),
});

var map = new ol.Map({
    target: 'map',
    layers: [tileLayer, markerLayer],
    view: view
});

var search = new ol.control.SearchNominatim({  // geocoding service by OpenStreetMap Nominatim
    lan: 'de',  // the language to use
    position: true,  // search with position as priority
    collapsed: false,  // whether to initially collapse the search input field
    typing: -1,  // the delay in ms before search gets triggered after each keystroke. The value -1 will disable autocomplete, which is required by the OSM Nominatim Usage Policy (https://operations.osmfoundation.org/policies/nominatim/)
    noCollapse: true  // if this is true, the search bar is collapsed when removing the focus from it
});
map.addControl(search);

search.on('select', function(e) {
    // set the new coordinates as the current coordinates
    setCurrentCoords(ol.proj.toLonLat(e.coordinate))

    search.collapse();  // collapse the search widget for a better view of the map

    clearMarkers();
    addMarker(e.coordinate);
    
    map.getView().animate({
        center: e.coordinate,
        zoom: Math.max(map.getView().getZoom(), 12)
    });
});

function clearMarkers() {
    markerLayer.getSource().clear();
}

function addMarker(coordinates) {
    var iconFeature = new ol.Feature({
        geometry: new ol.geom.Point(coordinates)
    });

    var iconStyle = new ol.style.Style({
        image: new ol.style.Icon({
            src: 'static/img/sun-icon.png',
            anchor: [0.5, 0.5],
            anchorXUnits: 'fraction',
            anchorYUnits: 'fraction',
            opacity: 0.9
        })
    });
    iconFeature.setStyle(iconStyle);

    markerLayer.getSource().addFeature(iconFeature);
}
