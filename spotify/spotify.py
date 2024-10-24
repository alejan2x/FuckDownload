import os
import re
import spotipy
from moviepy.editor import *
from urllib.parse import quote
from urllib import request as rq
from youtube_dl import YoutubeDL
from spotipy.oauth2 import SpotifyClientCredentials
import sys

## fix to skip use for PYTHONPATH
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(),"..","common"))

from common.common import controller_common
common = controller_common()

class controller_spotify:

    def __init__(self,client_api,token_api,user):

        self.__CLIENT_ID = client_api
        self.__CLIENT_SECRET = token_api
        self.__USER_ID = user

        self.auth_manager = SpotifyClientCredentials(
            client_id=self.__CLIENT_ID, client_secret=self.__CLIENT_SECRET
        )
        self.sp = spotipy.Spotify(auth_manager=self.auth_manager)

    def get_ydl_opts(self, path):
        return {
            "format": "bestaudio/best",
            "outtmpl": f"{path}/%(id)s.%(ext)s",
            "ignoreerrors": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "320",
                }
            ],
        }

    def get_user_playlists(self):
        return [
            {"value": pl.get("uri"), "name": pl.get("name")}
            for pl in self.sp.user_playlists(self.__USER_ID).get("items")
        ]

    def normalize_str(self, string):
        return string.translate(str.maketrans('\\/:*?"<>|', "__       "))

    def get_playlist_details(self, pl_uri):
        offset = 0
        fields = "items.track.track_number,items.track.name,items.track.artists.name,items.track.album.name,items.track.album.release_date,total,items.track.album.images"
        pl_name = self.sp.playlist(pl_uri)["name"]
        pl_items = self.sp.playlist_items(
            pl_uri,
            offset=offset,
            fields=fields,
            additional_types=["track"],
        )["items"]

        pl_tracks = []
        while len(pl_items) > 0:
            for item in pl_items:
                if item["track"]:
                    track_name = self.normalize_str(item["track"]["name"])
                    artist_name = self.normalize_str(
                        item["track"]["artists"][0]["name"]
                    )
                    pl_tracks.append(
                        {
                            "uri": quote(
                                f'{track_name.replace(" ", "+")}+{artist_name.replace(" ", "+")}'
                            ),
                            "file_name": f"{artist_name} - {track_name}",
                            "track_name": track_name,
                            "artist_name": artist_name,
                            "album_name": self.normalize_str(
                                item["track"]["album"]["name"]
                            ),
                            "album_date": item["track"]["album"]["release_date"],
                            "track_number": item["track"]["track_number"],
                            "album_art": item["track"]["album"]["images"][0]["url"],
                        }
                    )

            offset = offset + len(pl_items)
            pl_items = self.sp.playlist_items(
                pl_uri,
                offset=offset,
                fields=fields,
                additional_types=["track"],
            )["items"]

        return {"pl_name": pl_name, "pl_tracks": pl_tracks}

    def check_existing_tracks(self, playlist, path):
        existing_tracks = os.listdir(path)
        tracks = [
            track
            for track in playlist["pl_tracks"]
            if f"{track['file_name']}.mp3" not in existing_tracks
        ]
        return tracks

    def download_tracks(self, pl_uri):

        count = 0
        items = list()

        pl_details = self.get_playlist_details(pl_uri)
        path = common.create_download_directory(pl_details["pl_name"])
        tracks = self.check_existing_tracks(pl_details, path)
        print(
            f"\n\033[1m\033[33m[info] Downloading {len(tracks)} tracks from {pl_details['pl_name']}\033[0m"
        )
        with YoutubeDL(self.get_ydl_opts(path)) as ydl:
            for track in tracks:
                html = rq.urlopen(
                    f"https://www.youtube.com/results?search_query={track['uri']}"
                )
                video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())

                if video_ids:
                    url = "https://www.youtube.com/watch?v=" + video_ids[0]

                    print ( f"Add [{count}] - {url}" )
                    count = count + 1
                    items.append(url)

        common.download(items,path)
        print (f"\n#### MP3 Folder was created in: {path} ####")
        sys.exit(0)