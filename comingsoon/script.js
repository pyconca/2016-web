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
});
