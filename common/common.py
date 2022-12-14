import os
import time
import platform
import threading
import subprocess
from pytube import YouTube
from moviepy.editor import *
from pytube.cli import on_progress

# example: /home/user/music
download_base_path = "C:\download"

if "--dst" in sys.argv:
        dst = sys.argv[sys.argv.index("--dst") + 1]
        download_base_path = (os.path.join(dst,"download"))

class controller_common:

    def create_download_directory(self, dir_name):
        
        path = os.path.join(download_base_path,dir_name)

        if os.path.exists(path):
            return path

        try:
            os.makedirs(path)
            return path
        except OSError:
            print("Creation of the download directory failed")

    def clean_ws(self,path):

        print ("\n ===== Delete temporal files ===== ")
        print ("Wait 20 sec to start delete\n")
        
        time.sleep (20)

        if platform.system() == "Windows":
            cmd = ["taskkill", "/f", "/im", "ffmpeg-win64*"]

            try:      
                subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
            
            except subprocess.CalledProcessError as error:
                print(error)
                sys.exit(1)

        gppList = [ os.path.join(path,i)
                    for root,dirs,files in os.walk(path)
                        for i in files
                        if i.endswith(".3gpp") ]

        for line in gppList:
            os.remove(line)
        print (f"\n#### MP3 Folder was created in: {path} ####")
        sys.exit(0)

    def converterto_mp3(self,pl_name):

        baseDownload = (os.path.join(download_base_path,pl_name))

        gppList = [ i
                    for root,dirs,files in os.walk(baseDownload)
                    for i in files
                    if i.endswith(".3gpp") ]

        res = self.thread_pool(gppList,baseDownload,"converter")

        if res:
            self.clean_ws(baseDownload)
    
    def thread_function_download(self,id_thread,folder_output,url):

        print ( f"\nID - {id_thread}: start download")
        YouTube(url,on_progress_callback=on_progress).streams.filter().first().download(output_path=folder_output)

    def thread_function_converter(self,id_thread,folder,track):

        print ( f"\nID - {id_thread}: start convertion")
        video = VideoFileClip(os.path.join (folder,track))
        video.audio.write_audiofile(os.path.join (folder,track.replace(".3gpp",".mp3")))

    def thread_pool(self, lista, path, ftype):

        if ftype == "download":
            method = self.thread_function_download
        
        if ftype == "converter":
            method = self.thread_function_converter


        limite = len (lista)
        count = 0
        laps = 5
        threads = list()

        try:
            while True :
                while laps > count:
                    track = lista[count]
                    x = threading.Thread(target=method , args=(count,path,track,))
                    threads.append(x)
                    count = count + 1
                    x.start()

                for index, thread in enumerate(threads):
                    thread.join()

                    if (laps -1) == index:
                        print ("\n<<<< Next pool >>>>")
                        count = laps
                        laps = laps + 5

        except IndexError:
            pass

        for index, thread in enumerate(threads):
            thread.join()

        if (index + 1) == limite:
            return True