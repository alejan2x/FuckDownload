import sys
import os
import yt_dlp
import subprocess

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

        try:

            print (ouput_folder)

            output_file = os.path.join(ouput_folder,'%(title)s.%(ext)s')

            ydl_opts = self.get_ydl_opts(output_file) 

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                error_code = ydl.download(URLS) 
                print (error_code)

        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            sys.exit(1)

    def get_ydl_opts(self, output):
        return {
            'format': 'best',
            # 'cookiefile': 'C:/Users/ahroque/Downloads/cookies.txt',
            # 'cookiesfrombrowser': ('edge', 'Default'),
            'extractor_args': {
                'youtube': {
                    'player_client': ['android']
                }
            },
            "outtmpl": output,
            "ignoreerrors": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
        }    
        