import os
import sys
from pyfiglet import figlet_format
from spotify.spotify import controller_spotify
from youtube.yt import controller_youtube


DESCRIPTION = """
#######################################################################################
#    Author: Alejandro Hernandez Roque
#    e-mail: ggerti_tuigger@hotmail.com
#    Date:   July 31, 2022
#    Description:    You can download playlist from Spotifty and Youtube.
#                    it will generate a folder with tracks of mp3's
#
#                    if you can download playlist of Spotify you going to visit:
#                    https://developer.spotify.com/dashboard/login
#                    and create you client, token, because this tool use REST-API
#                    to get playlist data. 
#                    
#                    Create token
#                       - URL Spotify token via api : https://accounts.spotify.com/api/token
#                       - Basic Auth :  client_id:token_id
#                       - body: x-www-form-urlencoded
#                       - key: grant_type key_value: client_credentials
#                   
#                    Get track list via api:
#                       - https://api.spotify.com/v1/playlists/<id_playlist_personal>
#                       - Bearer Auth : previusly generated in the before stept
#
#                    
#                    Spotify controller is based in the proyect Hades 
#                    https://github.com/norbeyandresg/hades.git
#
#                    with YouTube , you can download:
#                        - playlist (is mode public)
#                        - track from txt file
#                        - mix youtube playlist (is neccesary use chromedriver)
#                        - simple track
#
#
#    Parameters:     read README.md
#######################################################################################
"""

if __name__ == "__main__":

    if "--spotify" in sys.argv or "-s" in sys.argv:

        if "--pl_uri" in sys.argv:

            client_api ="<>"
            token_api = "<>"
            user = "<>"
            
            pl_uri = sys.argv[sys.argv.index("--pl_uri") + 1]
            spoti = controller_spotify(client_api,token_api,user)
            # print(figlet_format("Spotify", font="doh"))
            spoti.download_tracks(pl_uri)
        
        else :
            print ("\033[1m\033[33m[Error] : use cli.py --help to help")
            sys.exit(1)
    
    if "--youtube" in sys.argv or "-y" in sys.argv:

        if "--track_uri" in sys.argv:
            track_uri = sys.argv[sys.argv.index("--track_uri") + 1]
            ytb = controller_youtube()
            # print(figlet_format("YouTube", font="doh"))
            ytb.download_track(track_uri)
        
        if "--pl_uri" in sys.argv:
            
            pl_uri = sys.argv[sys.argv.index("--pl_uri") + 1]
            ytb = controller_youtube()
            # print(figlet_format("YouTube", font="doh"))
            ytb.download_tracks(pl_uri)
        
        if "--selenium" in sys.argv:

            if sys.argv.index("--chromedriver_path") :

                chromedriver_path = sys.argv[sys.argv.index("--chromedriver_path") + 1]

                pl_uri = sys.argv[sys.argv.index("--chromedriver_path") + 2]
                ytb = controller_youtube()
                # print(figlet_format("YouTube", font="doh"))
                ytb.download_tracks_selenium(pl_uri,chromedriver_path)

            else :
                print (f"\033[1m\033[33m[Error] : set path chromedriver")
                sys.exit(1)

        if "--pl_file" in sys.argv:
            
            pl_file = sys.argv[sys.argv.index("--pl_file") + 1]
            ytb = controller_youtube()
            print(figlet_format("YouTube", font="doh"))

            if os.path.exists(pl_file):
                ytb.download_from_file(pl_file)

            else :
                print (f"\033[1m\033[33m[Error] : file is not found : {pl_file}")
                sys.exit(1)
        else :
            print ("\033[1m\033[33m[Error] : use cli.py --help to help")
            sys.exit(1)
    
    if "--help" in sys.argv or "-h" in sys.argv:
        print ("Please read file README.md to Instruccions")
        sys.exit(0)
            
    else :
        print ("\033[1m\033[33m[Error] : use cli.py --help or -h")
        sys.exit(1)