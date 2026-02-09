import re
import time
import pandas
import datetime
from urllib import request as rq

from common.common import controller_common
common = controller_common()


df = pandas.read_excel(r"C:\Users\ahroque\Downloads\canciones.xlsx")

count = 0
url_list = list()

for index, row in df.iterrows():
    lyrinc = row[0] , row[1]
    values = ','.join(str(v) for v in lyrinc).strip().replace(" ","%20").encode("utf-8")

    html = rq.urlopen(
                f"https://www.youtube.com/results?search_query={values}"
            )
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())

    if video_ids:
        url = "https://www.youtube.com/watch?v=" + video_ids[0]
        print ( f"Add [{count}] - {url}" )
        count = count + 1
        url_list.append(url)

size_list = 10
trozos = [url_list[i:i + size_list] for i in range(0, len(url_list), size_list)]

now = datetime.datetime.now()
time_format = now.strftime('%d-%m-%YT%H_%M_%S')
pl_name = f"YouTube-playlist-{time_format}"
folder_path = common.create_download_directory(pl_name)

for lista in trozos:
    common.download(lista,folder_path)
    time.sleep(30)
print (f"\n#### MP3 Folder was created in: {folder_path} ####")