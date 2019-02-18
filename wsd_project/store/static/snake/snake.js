window.onload=function() {
    canv=document.getElementById("gc");
    context=canv.getContext("2d");
    document.addEventListener("keydown",keyPush);
    setInterval(game,1000/10);
}
score = 0;
px=py=10;
mapsize=20;
ax=ay=15;
xv=yv=0;
trail=[];
tail = 1;
speed = 10;
is_paused = false;

function game() {
    $("#restart").click( function () {
        location.reload();
    });

    $("#submit_score").click( function () {
        is_paused = True;
        var msg = {
          "messageType": "SCORE",
          "score": parseFloat($("#score").text())
        };
        window.parent.postMessage(msg, "*");
        is_paused = False;
      });

    $("#save").click( function () {
        var msg = {
          "messageType": "SAVE",
          "gameState": {
            "px": parseFloat($("#py").text()),
            "py": parseFloat($("#px").text()),
            "tail": parseFloat($("#tail").text()),
            "trail": toString(trail),
            "score": parseFloat($("#score").text())
          }
        };
        window.parent.postMessage(msg, "*");
      });
  
      $("#load").click( function () {
        var msg = {
          "messageType": "LOAD_REQUEST",
        };
        window.parent.postMessage(msg, "*");
      });

      window.addEventListener("message", function(evt) {
        if(evt.data.messageType === "LOAD") {
          py = evt.data.gameState.py;
          py = evt.data.gameState.px;
          tail = evt.data.gameState.tail;
          trail = str.split(evt.data.gameState.trail);
          points = evt.data.gameState.score;
          $("#score").text(points);
          updateItems();
        } else if (evt.data.messageType === "ERROR") {
          alert(evt.data.info);
        }
      });
    
    if (!is_paused) {
        px+=xv;
        py+=yv;
        
        if(px<0) {
            px= mapsize-1;
        }
        if(px>mapsize-1) {
            px= 0;
        }
        if(py<0) {
            py= mapsize-1;
        }
        if(py>mapsize-1) {
            py= 0;
        }
        
        context.fillStyle="navy";
        context.fillRect(0,0,canv.width,canv.height);
     
        context.fillStyle="orange";
        for(var i=0;i<trail.length;i++) {
            context.fillRect(trail[i].x*mapsize,trail[i].y*mapsize,mapsize-2,mapsize-2);
            if(trail[i].x==px && trail[i].y==py && trail.length > 2) {
                // lost game 
                var msg = {
                    "messageType": "SCORE",
                    "score": parseFloat($("#score").text())
                };
                console.log(msg);
                window.parent.postMessage(msg, "*");
                is_paused = true
            }            
        }
        
        trail.push({x:px,y:py});
        
        while(trail.length>tail) {
            trail.shift();
        }
     
        if(ax==px && ay==py) {
            if (tail < 15) {
                tail++;
            }
            score += 10;
            $("#score").text(score);
            ax=Math.floor(Math.random()*mapsize);
            ay=Math.floor(Math.random()*mapsize);
        }

        context.fillStyle="red";
        context.fillRect(ax*mapsize,ay*mapsize,mapsize-2,mapsize-2);
    }
}

function keyPush(event) {
    switch(event.keyCode) {
        case 37:
            xv=-1;yv=0;
            break;
        case 38:
            xv=0;yv=-1;
            break;
        case 39:
            xv=1;yv=0;
            break;
        case 40:
            xv=0;yv=1;
            break;
    }
}