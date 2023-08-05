# Jellyfin MPV Shim

Jellyfin MPV Shim is a simple and lightweight Jellyfin client, with support for Windows
and Linux. Think of it as an open source Chromecast for Jellyfin. You can cast almost
anything from Jellyfin and it will Direct Play. Subtitles are fully supported, and
there are tools to manage them like no other Jellyfin client.

## Getting Started

If you are on Windows, simply [download the binary](https://github.com/iwalton3/jellyfin-mpv-shim/releases).
If you are using Linux, please see the [Linux Installation](https://github.com/iwalton3/jellyfin-mpv-shim/blob/master/README.md#linux-installation) section below.

To use the client, simply launch it and log into your Jellyfin server. You’ll need to enter the
URL to your server, for example `http://server_ip:8096` or `https://secure_domain`. Make sure to
include the subdirectory and port number if applicable. You can then cast your media
from another Jellyfin application.

The application runs with a notification icon by default. You can use this to edit the server settings,
view the application log, open the config folder, and open the application menu. Unlike Plex MPV Shim,
authorization tokens for your server are stored on your device, but you are able to cast to the player
regardless of location.

## Limitations

 - Music playback and Live TV are not supported.
 - The client can’t be shared seamlessly between multiple users on the same server. ([Link to issue.](https://features.jellyfin.org/posts/319/mark-device-as-shared))

## Advanced Features

### Menu

To open the menu, press **c** on your computer. Depending on what app you are
using to control Jellyfin, you may also be able to open the menu using that app.
The web application currently doesn't have the required buttons to do so.

The menu enables you to:
 - Adjust video transcoding quality.
 - Change the default transcoder settings.
 - Change subtitles or audio, while knowing the track names.
 - Change subtitles or audio for an entire series at once.
 - Mark the media as unwatched and quit.

On your computer, use the arrow keys, enter, and escape to navigate. On your phone, use
the arrow buttons, ok, back, and home to navigate. (The option for remote controls is
shown next to the name of the client when you select it from the cast menu.)

Please also note that the on-screen controller for MPV (if available) cannot change the
audio and subtitle track configurations for transcoded media. It also cannot load external
subtitles. You must either use the menu or the application you casted from.

### Keyboard Shortcuts

This program supports most of the [keyboard shortcuts from MPV](https://mpv.io/manual/stable/#interactive-control). The custom keyboard shortcuts are:

 - < > to skip episodes
 - q to close player
 - w to mark watched and skip
 - u to mark unwatched and quit
 - c to open the menu

Here are the notable MPV keyboard shortcuts:

 - space - Pause/Play
 - left/right - Seek by 5 seconds
 - up/down - Seek by 1 minute
 - s - Take a screenshot
 - S - Take a screenshot without subtitles
 - f - Toggle fullscreen
 - ,/. - Seek by individual frames
 - \[/\] - Change video speed by 10%
 - {/} - Change video speed by 50%
 - backspace - Reset speed
 - m - Mute
 - d - Enable/disable deinterlace
 - Ctrl+Shift+Left/Right - Adjust subtitle delay.

## Configuration

The configuration file is located in different places depending on your platform. When you
launch the program, the location of the config file will be printed. The locations are:
 - Windows - `%appdata%\jellyfin-mpv-shim\conf.json`
 - Linux - `~/.config/jellyfin-mpv-shim/conf.json`
 - Mac OSX - `Library/Application Support/jellyfin-mpv-shim/conf.json`
 - CygWin - `~/.config/jellyfin-mpv-shim/conf.json`

### Transcoding

You can adjust the basic transcoder settings via the menu.

- `always_transcode` - This will tell the client to always transcode. Default: `false`
    - This may be useful if you are using limited hardware that cannot handle advanced codecs.
- `transcode_h265` - Transcode HEVC videos. Default: `false`
- `transcode_hi10p` - Transcode 10 bit color videos. Default: `false`
- `remote_kbps` - Bandwidth to permit for remote streaming. Default: `10000`
- `local_kbps` - Bandwidth to permit for local streaming. Default: `2147483`
- `direct_paths` - Play media files directly from the SMB or NFS source. Default: `false`
    - `remote_direct_paths` - Apply this even when the server is detected as remote. Default: `false`

### Shell Command Triggers

You can execute shell commands on media state using the config file:

 - `media_ended_cmd` - When all media has played.
 - `pre_media_cmd` - Before the player displays. (Will wait for finish.)
 - `stop_cmd` - After stopping the player.
 - `idle_cmd` - After no activity for `idle_cmd_delay` seconds.

### Subtitle Visual Settings

All of these settings apply to direct play and are adjustable through the controlling app. Note that some may not work depending on the subtitle codec. Subtitle position and color are not available for transcodes.

 - `subtitle_size` - The size of the subtitles, in percent. Default: `100`
 - `subtitle_color` - The color of the subtitles, in hex. Default: `#FFFFFFFF`
 - `subtitle_position` - The position (top, bottom, middle). Default: `bottom`

### External MPV

The client now supports using an external copy of MPV, including one that is running prior to starting
the client. This may be useful if your distribution only provides MPV as a binary executable (instead
of as a shared library), or to connect to MPV-based GUI players. Please note that SMPlayer exhibits
strange behaviour when controlled in this manner.

- `mpv_ext` - Enable usage of the external player by default. Default: `false`
    - The external player may still be used by default if `libmpv1` is not available.
- `mpv_ext_path` - The path to the `mpv` binary to use. By default it uses the one in the PATH. Default: `null`
    - If you are using Windows, make sure to use two backslashes. Example: `C:\\path\\to\\mpv.exe`
- `mpv_ext_ipc` - The path to the socket to control MPV. Default: `null`
    - If unset, the socket is a randomly selected temp file.
    - On Windows, this is just a name for the socket, not a path like on Linux.
- `mpv_ext_start` - Start a managed copy of MPV with the client. Default: `true`
    - If not specified, the user must start MPV prior to launching the client.
    - MPV must be launched with `--input-ipc-server=[value of mpv_ext_ipc]`.

### Other Configuration Options

 - `player_name` - The name of the player that appears in the cast menu. Initially set from your hostname.
 - `client_uuid` - The identifier for the client. Set to a random value on first run.
 - `audio_output` - Currently has no effect. Default: `hdmi`
 - `fullscreen` - Fullscreen the player when starting playback. Default: `true`
 - `enable_gui` - Enable the system tray icon and GUI features. Default: `true`
 - `media_key_seek` - Use the media next/prev keys to seek instead of skip episodes. Default: `false`
 - `enable_osc` - Enable the MPV on-screen controller. Default: `true`
    - It may be useful to disable this if you are using an external player that already provides a user interface.
 - `use_web_seek` - Use the seek times set in Jellyfin web for arrow key seek. Default: `false`

### MPV Configuration

You can configure mpv directly using the `mpv.conf` file. (It is in the same folder as `conf.json`.)
This may be useful for customizing video upscaling, keyboard shortcuts, or controlling the application
via the mpv IPC server.

### Authorization

The `cred.json` file contains the authorization information. If you are having problems with the client,
such as the Now Playing not appearing or want to delete a server, you can delete this file and add the
servers again.

## Development

If you'd like to run the application without installing it, run `./run.py`.
The project is written entierly in Python 3. There are no closed-source
components in this project. It is fully hackable.

The project is dependent on `python-mpv`, `python-mpv-jsonipc`, and `jellyfin-apiclient-python`. If you are
using Windows and would like mpv to be maximize properly, `pywin32` is also needed. The GUI
component uses `pystray` and `tkinter`, but there is a fallback cli mode.

This project is based Plex MPV Shim, which is based on https://github.com/wnielson/omplex, which
is available under the terms of the MIT License. The project was ported to python3, modified to
use mpv as the player, and updated to allow all features of the remote control api for video playback.

The Jellyfin API client comes from [Jellyfin for Kodi](https://github.com/jellyfin/jellyfin-kodi/tree/master/jellyfin_kodi).
The API client was originally forked for this project and is now a [separate package](https://github.com/iwalton3/jellyfin-apiclient-python).

## Linux Installation

If you are on Linux, you can install via pip. You'll need [libmpv1](https://github.com/Kagami/mpv.js/blob/master/README.md#get-libmpv) or `mpv` installed.
```bash
sudo pip3 install --upgrade jellyfin-mpv-shim
```
If you would like the GUI and systray features, also install `pystray` and `tkinter`:
```bash
sudo pip3 install pystray
sudo apt install python3-tk
```

You can build mpv from source to get better codec support. Execute the following:
```bash
sudo pip3 install --upgrade python-mpv
sudo apt install autoconf automake libtool libharfbuzz-dev libfreetype6-dev libfontconfig1-dev libx11-dev libxrandr-dev libvdpau-dev libva-dev mesa-common-dev libegl1-mesa-dev yasm libasound2-dev libpulse-dev libuchardet-dev zlib1g-dev libfribidi-dev git libgnutls28-dev libgl1-mesa-dev libsdl2-dev cmake wget python g++ libluajit-5.1-dev
git clone https://github.com/mpv-player/mpv-build.git
cd mpv-build
echo --enable-libmpv-shared > mpv_options
./rebuild -j4
sudo ./install
sudo ldconfig
```

## Building on Windows

There is a prebuilt version for Windows in the releases section. When
following these directions, please take care to ensure both the python
and libmpv libraries are either 64 or 32 bit. (Don't mismatch them.)

1. Install [Python3](https://www.python.org/downloads/) with PATH enabled. Install [7zip](https://ninite.com/7zip/).
2. After installing python3, open `cmd` as admin and run `pip install --upgrade pyinstaller python-mpv jellyfin-apiclient-python pywin32 pystray`.
3. Download [libmpv](https://sourceforge.net/projects/mpv-player-windows/files/libmpv/).
4. Extract the `mpv-1.dll` from the file and move it to the `jellyfin-mpv-shim` folder.
5. Open a regular `cmd` prompt. Navigate to the `jellyfin-mpv-shim` folder.
6. Run `pyinstaller -wF --add-binary "mpv-1.dll;." --add-binary "jellyfin_mpv_shim\systray.png;." --icon media.ico run.py`.
