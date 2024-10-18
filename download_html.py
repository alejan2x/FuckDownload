import urllib3
import re
from urllib import request as rq
from bs4 import BeautifulSoup
from youtube_dl import YoutubeDL
import datetime
from pytube import Playlist

from common.common import controller_common
common = controller_common()


def get_ydl_opts(path):
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

def getHtml(url):
    http = urllib3.PoolManager()
    response = http.request('GET', url)

    soup = BeautifulSoup(response.data, 'html.parser')
    return soup

def parse_html(html_data):
    lista = list()
    for x in soup.find_all('a'):
        song = x.string
        if song != None and " - " in song:
            lista.append(song.strip().replace(" ","%20"))
    return lista

def search_yt(list_song):

    count = 0
    items = list()

    now = datetime.datetime.now()
    time_format = now.strftime('%d-%m-%YT%H_%M_%S')
    pl_name = f"YouTube-playlist-{time_format}"
    path = common.create_download_directory(pl_name)

    with YoutubeDL(get_ydl_opts(path)) as ydl:
        for track in list_song:
            html = rq.urlopen(
                f"https://www.youtube.com/results?search_query={track}"
            )
            video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())

            if video_ids:
                url = "https://www.youtube.com/watch?v=" + video_ids[0]
                print ( f"Add [{count}] - {url}" )
                count = count + 1
                items.append(url)
    
    res = common.thread_pool(items,path,"download")
    if res:
        common.converterto_mp3(path)

if __name__ == '__main__':
    soup = getHtml("https://101dancehits.bandcamp.com/album/psy-trance-2023-top-100-hits")
    list_to_search = parse_html(soup)
    url_list = search_yt(list_to_search)  
   