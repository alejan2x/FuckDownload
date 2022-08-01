import os
import re
import sys
import datetime
from pytube import Playlist
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
        
        items = Playlist(pl_uri)
        pl_name = items.title
        path = common.create_download_directory(pl_name)
        
        res = common.thread_pool(items,path,"download")

        if res:
            common.converterto_mp3(pl_name)
    
    def download_from_file(self,pl_file):

        now = datetime.datetime.now()
        time_format = now.strftime('%d-%m-%YT%H_%M_%S')
        pl_name = f"YouTube-list-{time_format}"
        
        items = list()
        path = common.create_download_directory(pl_name)

        with open (pl_file) as txt:
            lines = txt.readlines()
            for url in lines:
                urlName = url.replace("\n","").strip()
                video_ids = re.findall(r"watch\?v=(\S{11})", urlName)
                url = "https://www.youtube.com/watch?v=" + video_ids[0]
                items.append(url)

        res = common.thread_pool(items,path,"download")
        
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
        
        
        
