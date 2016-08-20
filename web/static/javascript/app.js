/*jslint browser: true */
/*global  $,ga */

function trackOutboundLinkClicks(link) {
    'use strict';
    
    var href = link.attr('href'),
        noProtocol = href.replace(/http[s]?:\/\//, '');
    
    ga('send', 'event', {
        eventCategory: 'Outbound Link',
        eventAction: 'click',
        eventLabel: noProtocol
    });
}

jQuery(document).ready(function () {
    'use strict';

    var query = 'a:not([href*="' + document.domain + '"])';

    jQuery(query).mousedown(function (event) {
        trackOutboundLinkClicks(jQuery(this));
    });

    var venue_map = L.map('js-venue-map', {
        center: [43.65534, -79.38287],
        zoom: 14,
        scrollWheelZoom: false
    });
 L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
        maxZoom: 18,
        id: 'myles.163k2c22',
        accessToken: 'pk.eyJ1IjoibXlsZXMiLCJhIjoiY2lzM2p0YzN2MDVjdzJzbzBsc2c1NHZ1OSJ9.k7R24jfN4E8iNh7mlJoK7w'
    }).addTo(venue_map);

    L.Icon.Default.imagePath = "/static/images/leaflet";

    var marker = L.marker([43.65534, -79.38287]).addTo(venue_map);
});
