import sys
import os
import yt_dlp
import subprocess

import time

# example: /home/user/music
download_base_path = r"C:\Users\ahroque\Downloads\download"

if "--dst" in sys.argv:
    dst = sys.argv[sys.argv.index("--dst") + 1]
    download_base_path = (os.path.join(dst,"download"))

class controller_common:

    def create_download_directory(self, dir_name):
        
        path_download = os.path.join(download_base_path,dir_name)

        try :
            os.makedirs(path_download)
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            raise
        
        return path_download
    
    def download(self,URLS,ouput_folder):

        max_retries = 3
        attempt = 0
        success = False

        while attempt < max_retries and not success:
            try:
                output_file = os.path.join(ouput_folder,'%(title)s.%(ext)s')
                subprocess.run(['yt-dlp', '--rm-cache-dir'])

                ydl_opts = self.get_ydl_opts(output_file) 

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    error_code = ydl.download(URLS)
                    if error_code == 0:
                        success = True

            except Exception as err:
                attempt += 1
                print(f"Unexpected {err=}, {type(err)=}")
                if attempt < max_retries:
                    print("wait 10 sec.")
                    time.sleep(10)
                else:
                    print("Se agotaron los intentos permitidos.")
                
    def get_ydl_opts(self, output):
        return {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
            'extractor_args': {
                'youtube': {
                    'player_client': ['android'],
                }
            },
            'concurrent_fragment_downloads': 5,
            'retries': 10,
            'fragment_retries': 10,
            "outtmpl": output,
            "ignoreerrors": False,
            'nocheckcertificate': True,
            'geo_bypass': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
        }    
        