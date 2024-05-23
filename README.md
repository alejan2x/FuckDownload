# FuckDownload
You can download playlist from Spotifty and Youtube.
it will generate a folder with tracks of mp3's

if you can download playlist of Spotify you going to visit:
https://developer.spotify.com/dashboard/login
and create you client, token, because this tool use REST-API
to get playlist data.

Create token
    - URL Spotify token via api : https://accounts.spotify.com/api/token
    - Basic Auth :  client_id:token_id
    - body: x-www-form-urlencoded
    - key: grant_type key_value: client_credentials
                   
Get track list via api:
    - https://api.spotify.com/v1/playlists/<id_playlist_personal>
    - Bearer Auth : previusly generated in the before stept
                    
Spotify controller is based in the proyect Hades 
https://github.com/norbeyandresg/hades.git

with YouTube , you can download:
    - playlist (is mode public)
    - track from txt file
    - mix youtube playlist (is neccesary use chromedriver)
    - simple track

## cipher libray error in pytube 11.0.2
edit the file Python38\Lib\site-packages\pytube\cypher.py
`update the line for this`: var_regex = re.compile(r"^\$*\w+\W")
 
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
To use the shell interface run. You must edit `cli.py` and set the values of lines `41,42,43`
for the `token , user_id, user of spotify`

``` shell
python cli.py -s --pl_uri "<url playlist>" --dst "C:\path\to\download"
ex:: python cli.py -s --pl_uri "https://open.spotify.com/playlist/1ISS7NJiClZjglJfZHuux3" --dst "C:\Users\roque\Downloads"
```

## Usage to youtube
Just go to your playlist, click on share and copy the Track URI or PlayList URI. 
To use the shell interface run

``` shell
download a track
python cli.py -y --track_uri "<url track>" --dst "C:\path\to\download"
ex:: python cli.py -y --track_uri "https://www.youtube.com/watch?v=gGdGFtwCNBE" --dst "C:\Users\roque\Downloads"
```

``` shell
download playlist
python cli.py -y --pl_uri "<url ply list valid>" --dst "C:\path\to\download"
ex:: python cli.py -y --pl_uri "https://www.youtube.com/playlist?list=PLeMi01xRAJp5VsU26WsUjZZJmouazRLr-" --dst "C:\Users\roque\Downloads"
```

``` shell
download mix youtube playlist with selenium
python cli.py -y --selenium --chromedriver_path "C:\chrome\driver\path" "<url_mix_youtube_playlist>" --dst "C:\path\to\download"
ex:: python cli.py -y --selenium --chromedriver_path "C:\Users\roque\Downloads\chromedriver\chromedriver.exe" "https://www.youtube.com/watch?v=gGdGFtwCNBE&list=RDMM&index=1" --dst "C:\Users\roque\Downloads"
```

``` shell
download from file
python cli.py -y --pl_file "<C:\path\to\read\file.txt>" --dst "C:\path\to\download"
ex:: python cli.py -y --pl_file "C:\Users\roque\Downloads\song.txt" --dst "C:\Users\roque\Downloads"
```


