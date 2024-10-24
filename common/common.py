import sys
import os
import yt_dlp

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

            ydl_opts = {
                'format': 'm4a/bestaudio/best',
                'outtmpl': output_file,
                # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
                'postprocessors': [{  # Extract audio using ffmpeg
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                }],
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                error_code = ydl.download(URLS) 
                print (error_code)

        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            raise