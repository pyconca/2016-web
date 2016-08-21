/*jslint browser: true */
/*global  L,jQuery,ga */

function trackOutboundLinkClicks(link, event) {
    'use strict';

    var href = link.attr('href'),
        noProtocol = href.replace(/http[s]?:\/\//, '');

    ga('send', 'event', {
        eventCategory: 'Outbound Link',
        eventAction: 'click',
        eventLabel: noProtocol
    });
}

function displayMap() {
    'use strict';

    var venueMap = L.map('js-venue-map', {
        center: [43.65534, -79.38287],
        zoom: 14,
        scrollWheelZoom: false
    });

    L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="http://openstreetmap.org"> OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
        maxZoom: 18,
        id: 'myles.163k2c22',
        accessToken: 'pk.eyJ1IjoibXlsZXMiLCJhIjoiY2lzM2p0YzN2MDVjdzJzbzBsc2c1NHZ1OSJ9.k7R24jfN4E8iNh7mlJoK7w'
    }).addTo(venueMap);

    L.Icon.Default.imagePath = "/static/images/leaflet";

    var marker = L.marker([43.65534, -79.38287]).addTo(venueMap);
}

jQuery(window).resize(function() {
    var nav = document.getElementById("js-navigation-menu");

    if (jQuery(nav).length > 0) {
        var windowWidth = jQuery(window).width();
        var moreLeftSideToPageLeftSide = jQuery(nav).offset().left;
        var moreLeftSideToPageRightSide = windowWidth - moreLeftSideToPageLeftSide;

        if (moreLeftSideToPageRightSide < 330) {
            jQuery("#js-navigation-menu").removeClass("navigation__list--fly-out-right");
            jQuery("#js-navigation-menu").addClass("navigation__list--fly-out-left");
        }
        
        if (moreLeftSideToPageRightSide > 330) {
            jQuery("#js-navigation-menu").removeClass("navigation__list--fly-out-left");
            jQuery("#js-navigation-menu").addClass("navigation__list--fly-out-right");
        }
    }
});

jQuery(document).ready(function () {
    'use strict';

    var navToggle = jQuery("#js-navigation-button").unbind()
    jQuery("#js-navigation-menu").removeClass("show");

    navToggle.on("click", function (e) {
        e.preventDefault();

        jQuery("#js-navigation-menu").slideToggle(function () {
            if (jQuery("#js-navigation-menu").is(":hidden")) {
                jQuery("#js-navigation-menu").removeAttr("style");
            }
        });
    });

    var query = 'a:not([href*="' + document.domain + '"])';

    jQuery(query).mousedown(function (event) {
        trackOutboundLinkClicks(jQuery(this), event);
    });

    if (jQuery('.js-venue-map')) {
        displayMap();
    }
});
