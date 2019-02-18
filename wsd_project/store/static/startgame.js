/*
console.log("loading script");
$(document).ready(function() {
    'use strict';
    $(window).on('message', function(event) {
        if (event.origin !== "http://webcourse.cs.hut.fi/example_game.html"){
            console.log("received message from the iframe")
            console.log("origin")
            console.log(event.origin)
            console.log("data")
            console.log(event.data)
            console.log("source")
            console.log(event.source)
            return;
        }
    });
});
*/
/*HTMLIFrameElement.contentWindow (to reference an embedded <iframe> from its parent window)*/

// Following getCookie function, csrf safe method and ajax setup copiedfrom django specification  from https://docs.djangoproject.com/en/2.1/ref/csrf/
// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


$(document).ready(function() {
    window.addEventListener("message", receiveMessage, false);

    function receiveMessage(event){

        console.log("received message from the iframe")
        //find the source attribute of the iframe (for post message origin checks)
        var source = $("iframe").attr('src');

        //origin does not have the resource appended to it only the protocol and domain
        if (source.indexOf(event.origin) !== -1){
            console.log("correct origin");
            if(event.data.messageType == "SETTING"){
                console.log("settings received");
                // set iframe dimensions
                console.log("width");
                console.log(event.data.options.width);
                console.log("height");
                console.log(event.data.options.height);
                var frame = $("iframe");
                frame.attr("width", event.data.options.width);
                frame.attr("height", event.data.options.height);
            }
            else if(event.data.messageType == "SCORE"){
                console.log("score received");
                var score = event.data.score;
                //the url does not need to be specified - it is by default the address of the html that launches the script 
                $.ajax({
                    type: "POST",
                    data: {'messagetype' : "SCORE", 'score' : score},
                    });
                //make a ajax POST REQUEST to the view
            }
            else if(event.data.messageType == "SAVE"){
                //save the gamestate to the service
                console.log("save request received");
                var gamestate = JSON.stringify(event.data.gameState);
                $.ajax({
                    type: "POST",
                    data: {'messagetype' : "SAVE", 'gamestate' : gamestate},
                    });
            }
            else if(event.data.messageType == "LOAD_REQUEST"){
                console.log("load request received");
                $.ajax({
                    type: 'POST',
                    data: {'messagetype': "LOAD_REQUEST"},
                    dataType: 'json',
                    success: function(data){
                        console.log("success function triggered");
                        console.log(data);
                        //data is the jsonrespponse from the views
                        var loadstate = JSON.parse(data.state);
                        var responsemessage = { 
                            messageType: "LOAD",
                            gameState: loadstate,
                        };
                        //The window object of the spawned iframe
                        var targetwindow = event.source;
                        //send the loadstate to the iframe with messagetype as 'LOAD'
                        targetwindow.postMessage(responsemessage, source);
                    },
                });
                //request to load gamestate from service => respond with postmessage with message type as LOAD and data as the given data
            }
            else{
                console.log("message not identified");
                //should send an error postmessage to the game
            }
        }
        console.log("data");
        console.log(event.data);
    }
});

