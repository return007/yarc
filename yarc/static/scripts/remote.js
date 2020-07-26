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
    showRemote(remoteIdx);

    // Play sound on key press of keyboard
    var audio = new Audio('../static/resources/keypress_sound.mp3');
    $('.key').on('click', function() {
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
}

// Initialize on script load.
init()