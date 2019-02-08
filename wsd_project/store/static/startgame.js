
console.log("loading script");
$(document).ready(function() {
    'use strict';
    $(window).on('message', function(evt) {
        console.log("say something");
    });
});
  