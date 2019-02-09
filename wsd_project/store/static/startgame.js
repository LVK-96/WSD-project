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


$(document).ready(function() {
    window.addEventListener("message", receiveMessage, false);

    function receiveMessage(event){

        console.log("received message from the iframe")

        //origin does not have the resource appended to it only the protocol and domain
        if ("http://webcourse.cs.hut.fi/example_game.html".indexOf(event.origin) !== -1){
            console.log("correct origin")
            if(event.data.messageType == "SETTING"){
                console.log("settings received")
            }
            else if(event.data.messageType == "SCORE"){
                console.log("score received")
            }
            else if(event.data.messageType == "SAVE"){
                console.log("save request received")
            }
            else if(event.data.messageType == "LOAD_REQUEST"){
                console.log("load request received")
            }
            else{
                console.log("message not identified")
            }
        }
        console.log("origin")
        console.log(event.origin)
        console.log("data")
        console.log(event.data)
        console.log("source")
        console.log(event.source)
    }
});

