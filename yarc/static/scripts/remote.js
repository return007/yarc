function switchRemote(n) {
    showRemote(remoteIdx += n);
}

function showRemote(n) {
    var i;
    var x = document.getElementsByClassName('remote-container');
    if(n > x.length)
        remoteIdx = 1;
    if(n < 1)
        remoteIdx = x.length
    for(i = 0; i < x.length; i++){
        x[i].style.display = 'none';
    }
    x[remoteIdx-1].style.display = 'block';
}

function init() {
    // Do all the intialization here
    remoteIdx = 1;
    X = null;
    Y = null;
    COMMAND_DELIMITER = '^_^';
    showRemote(remoteIdx);

    // Create websocket connection too
    var addr = window.location.hostname;
    var _getArgs = window.location.search.replace('?', '');
    var getArgs = {}
    for(var arg of _getArgs.split('&')){
        var _a = arg.split('=');
        var lhs = _a[0], rhs = _a[1];
        getArgs[lhs] = rhs
    }
    var wsport = getArgs['wsport']
    ws = new WebSocket(`ws://${addr}:${wsport}`);

    $('.key').on('click', function() {
        // Play sound on key press of keyboard
        var audio = new Audio('../static/resources/keypress_sound.mp3');
        audio.play();
    });

    $('.mouse-btn').on('click', function(event) {
        // Determine left or right mouse button click
        var target = event.target;
        var classNames = target.className.split(' ');
        var button = '';
        var audio = '';
        if(classNames.includes("left-mouse-btn")) {
            // Left mouse button was clicked!
            audio = new Audio('../static/resources/left-mouse-button-click.mp3');
            button = 'left';
        }
        else {
            // Right mouse button was clicked!
            audio = new Audio('../static/resources/right-mouse-button-click.mp3');
            button = 'right';
        }
        audio.play();
        var data = `CLICK${COMMAND_DELIMITER}${button}`;
        ws.send(data);
    });

    $('[buttonid]').on('click', function() {
        var buttonid = $(this).attr('buttonid');
        // Send the buttonid to the remote server
        $.ajax({
            type: 'post',
            url: '/keypress',
            data: JSON.stringify({buttonid: buttonid}),
            contentType: "application/json; charset=utf-8"
        });
    });

    $('.touchpad').on('touchstart', function(event) {
        X = event.touches[0].clientX;
        Y = event.touches[0].clientY;
    });
    $(".touchpad").on('touchmove', function(event) {
        var x = event.touches[0].clientX;
        var y = event.touches[0].clientY;
        if(X == null && Y == null) {
            // No previous touch happened.
            X = x;
            Y = y;
        }
        // Only send signal to move when there is a significant movement
        // The distance moved during ontouch is more than 10px
        var deltaX = parseInt(x-X);
        var deltaY = parseInt(y-Y);
        if(deltaX**2 + deltaY**2 >= 100) {
            // Send it via websocket
            // Command format is CMOVE^_^{deltaX},{deltaY}
            var data = `CMOVE${COMMAND_DELIMITER}${deltaX},${deltaY}`;
            ws.send(data);
            X = x;
            Y = y;
        }
    });
    $('.touchpad').on('touchend', function(event) {
        X = null;
        Y = null;
    });
}

// Initialize on script load.
init()