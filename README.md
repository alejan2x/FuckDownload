# FuckDownload
You can download playlist from Spotifty and Youtube.
it will generate a folder with tracks of mp3's

if you can download playlist of Spotify you going to visit:
https://developer.spotify.com/dashboard/login
and create you client, token, because this tool use REST-API
to get playlist data. 
                    
Spotify controller is based in the proyect Hades 
https://github.com/norbeyandresg/hades.git

with YouTube , you can download:
    - playlist (is mode public)
    - track from txt file
    - mix youtube playlist (is neccesary use chromedriver)
    - simple track
 
## Prerequisites
requires an installation of FFmpeg. Download for [Windows](https://www.wikihow.com/Install-FFmpeg-on-Windows), and for [UNIX](https://www.ffmpeg.org/download.html).
 
## Spotify API
You need to create an App on the [Spotify Developers Dashboard](https://developer.spotify.com/dashboard/applications) and setup your `CLIENT_ID` and `CLIENT_SECRET`variables to connect to the Spotify API. In order to list and download your own playlists you also need to setup your `USER_ID` in your variables.

## Chromedriver
download chromedriver from [ChromeDriver](https://chromedriver.chromium.org/downloads) can be:
windows/linux

``` shell
pip install -r requirements.txt
```

## Usage to spotify
Just go to your playlist, click on share and copy the Playlist URI. 
To use the shell interface run

``` shell
python cli.py -s --pl_uri "<url playlist>" --dst "C:\path\to\download"
```

## Usage to youtube
Just go to your playlist, click on share and copy the Track URI or PlayList URI. 
To use the shell interface run

``` shell
download a track
python cli.py -y --track_uri "<url track>" --dst "C:\path\to\download"
```

``` shell
download playlist
python cli.py -y --pl_uri "<url ply list valid>" --dst "C:\path\to\download"
```

``` shell
download mix youtube playlist with selenium
python cli.py -y --selenium --chromedriver_path "C:\chrome\driver\path" "<url_mix_youtube_playlist>" --dst "C:\path\to\download"
```

``` shell
download from file
python cli.py -y --pl_file "<C:\path\to\read\file.txt>" --dst "C:\path\to\download"
```


