# yarc

## Yet Another Remote Control

Control your desktop / laptop via mobile phone.

### How to:

Running control server and connecting to it is very straightforward. You would
need to do the following:

```
$ [sudo] pip install yarc-server

$ yarc

Starting control server...

Remote server running...
Scan the below code to start using remote control.

*SNIP*

Or alternatively, write the following URL on your mobile browser:
    http://192.168.1.4:xxx?wsport=xxx

```

### Basic features:

Single remote will have the following features. One can switch between remotes
easily via UI.

 - Streaming mode

    - Play / pause actions
    - Change volume
    - Change brightness
    - Seek forward / backwards

 - Change window (Alt + Tab) - Also, let user be able to select it

 - QWERTY keyboard to allow writing text

 - Touchpad to control mouse

### Advanced features:

The remote will automatically be switched depending on the active window. For
example, in case the active window is Netflix and is playing some content,
the remote should automatically switch to movie mode.

 - Screencast from mobile to laptop, so that one can enjoy in a bigger screen

 - Allow adding shortcuts, for example, "Open Netflix" can be a shortcut, to
   open Netflix on a single tap. Now, the way people open netflix is different.
   Some may have a Netflix app installed on their device, while others may use
   browser. Thus, user should be able to create with predefined event blocks, like:

   `press(winleft) -> type("Netflix") -> press(enter)`

   OR

   `press(winleft) -> type("Chrome") -> type("Netflix") -> press(enter)`

 - Gaming mode

 - Information about all opened windows and ability to jump to a specific
   window / switch windows via mobile touch actions (like mobile's default
   way to show running apps)

 - Customize theme of the remotes. Plug and play themes from website.

 - Allow user's to create their own themes and use it.

 - Netflix / Prime customization - example: skip intro, etc.

 - The remote should work even when the devices are not in same network.
   For that, we need the yarc server to generate a QR code and the client
   app should connect to the device over the internet.

 - Listen to the audio from phone itself (Use-case: wired earphones can be
   plugged in to mobile but the video would continue to play on the screen)
