import os
import re
import sys
import datetime
from pytube import Playlist,YouTube
from urllib import request as rq
from youtube_dl import YoutubeDL
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

## fix to skip use for PYTHONPATH 
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(),"..","common"))

from common.common import controller_common
common = controller_common()

class controller_youtube:

    def download_track (self,track_uri):
        
        items = list()

        now = datetime.datetime.now()
        time_format = now.strftime('%d-%m-%YT%H_%M_%S')
        pl_name = f"YouTube-track-{time_format}"

        path = common.create_download_directory(pl_name)
        video_ids = re.findall(r"watch\?v=(\S{11})", track_uri)
        url = "https://www.youtube.com/watch?v=" + video_ids[0]
        items.append(url)

        res = common.thread_pool(items,path,"download")
        
        if res:
            common.converterto_mp3(path)
    
    def download_tracks(self, pl_uri):

        if  not "playlist?list=" in pl_uri:
            print ("\033[1m\033[33m[Error] : playlist invalid url")
            sys.exit(1)
        
        now = datetime.datetime.now()
        time_format = now.strftime('%d-%m-%YT%H_%M_%S')

        items = Playlist(pl_uri)
        pl_name = f"YouTube-playlist-{time_format}"
        path = common.create_download_directory(pl_name)
        
        res = common.thread_pool(items,path,"download")

        if res:
            common.converterto_mp3(path)
    
    def download_from_file(self,pl_file):

        items = list()
        trackslist = list()
        count = 0

        now = datetime.datetime.now()
        time_format = now.strftime('%d-%m-%YT%H_%M_%S')
        pl_name = f"YouTube-list-{time_format}"
        
        path = common.create_download_directory(pl_name)

        with open (pl_file) as txt:
            lines = txt.readlines()

            lines = [line for line in lines if line.strip()]
            for url in lines:
                urlName = url.replace("\n","").strip()
                
                if not "##" in urlName:
                    video_ids = re.findall(r"watch\?v=(\S{11})", urlName)
                    url = "https://www.youtube.com/watch?v=" + video_ids[0]
                    items.append(url)

       
        with YoutubeDL(self.get_ydl_opts(path)) as ydl:
            for track in items:
                yt = YouTube(track)
                titleSong = yt.title
                titleSong = titleSong.replace(" ", "%20").encode('utf-8').strip()
                html = rq.urlopen(
                    f"https://www.youtube.com/results?search_query={titleSong}%20lyrics"
                )
               
                video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
                if video_ids:
                    url = "https://www.youtube.com/watch?v=" + video_ids[0]
                    print ( f"Add [{count}] - {url}" )
                    count = count + 1
                    trackslist.append(url)


        res = common.thread_pool(trackslist,path,"download")
        
        if res:    
            common.converterto_mp3(path)

    def download_tracks_selenium(self, pl_uri,chromedriver_path):

        now = datetime.datetime.now()
        time_format = now.strftime('%d-%m-%YT%H_%M_%S')
        pl_name = f"YouTube-mix-{time_format}"
        
        items = self.get_pl_list(pl_uri,chromedriver_path)
        path = common.create_download_directory(pl_name)
        
        res = common.thread_pool(items,path,"download")

        if res:
            common.converterto_mp3(path)

    def get_pl_list(self,urlFetch,chromedriver_path):

        print(f"\n Get mix YouTube list of {urlFetch}")
        count = 0
        lista = []

        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('----no-sandbox')
        chrome_options.add_argument("--disable-infobars")
        # chrome_options.add_argument("--incognito")

        url= urlFetch
        driver = webdriver.Chrome(chromedriver_path,chrome_options=chrome_options)
        driver.get(url)
        driver.implicitly_wait(30)
        items = driver.find_elements_by_css_selector("div#items.playlist-items ytd-playlist-panel-video-renderer a#wc-endpoint")
        
        for item in items :
            uri_base = item.get_attribute("href")
            video_ids = re.findall(r"watch\?v=(\S{11})", uri_base)
            url_video = "https://www.youtube.com/watch?v=" + video_ids[0]
            print ( f"Add [{count}] - {url_video}" )
            count = count + 1
            lista.append(url_video)

        return lista
        
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
        
