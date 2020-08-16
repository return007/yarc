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
    showRemote(remoteIdx);

    $('.key').on('click', function() {
        // Play sound on key press of keyboard
        var audio = new Audio('../static/resources/keypress_sound.mp3');
        audio.play();
    });

    $('.left-mouse-btn').on('click', function() {
        // Play sound on key press of keyboard
        var audio = new Audio('../static/resources/left-mouse-button-click.mp3');
        audio.play();
    });

    $('.right-mouse-btn').on('click', function() {
        // Play sound on key press of keyboard
        var audio = new Audio('../static/resources/right-mouse-button-click.mp3');
        audio.play();
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
        if(!(X == x && Y == y)) {
            $.ajax({
                type: 'post',
                url: '/mousemove',
                data: JSON.stringify({delta_x: x-X, delta_y: y-Y}),
                contentType: "application/json; charset=utf-8"
            });
        }
    });
    $('.touchpad').on('touchend', function(event) {
        X = null;
        Y = null;
    });
}

// Initialize on script load.
init()