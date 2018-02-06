# /wg wallpaper downloader 
import urllib
import os
import sys 
import time  
from bs4 import BeautifulSoup

def downloadHook(count, block_size, total_size):
    #expanded from: https://blog.shichao.io/2012/10/04/progress_speed_indicator_for_urlretrieve_in_python.html
    global start_time
    if count == 0: 
        start_time = time.time()  
        return
    duration = time.time() - start_time 
    if(duration == 0):
        #Division by zero fix
        duration = 0.001
    progress_size = int(count * block_size)  
    speed = int(progress_size / (1024 * duration)) 
    percent = min(int(count * block_size * 100 / total_size),100)  
    sys.stdout.write("\r...%d%%, %d MB, %d KB/s" %
                    (percent, progress_size / (1024 * 1024), speed))

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

#Website url provided as sys argument 
thread = sys.argv[1]

content = urllib.request.Request(thread, headers=hdr)
content = urllib.request.urlopen(content) 
#parse to BeautifulSoup object for easy searching
soup = BeautifulSoup(content, "html5lib")
images = soup.findAll("a", {"class" : "fileThumb"})

count = 0 
for image in images: 
    count += 1
    #filter out url junk to get relative filename
    absolute_filename = "http:" + image['href']
    relative_image = absolute_filename[21:]
    sys.stdout.write("Trying: " + str(absolute_filename) + "\n")

    if(os.path.isfile(relative_image)):
        sys.stdout.write("file exists.\n")
    else: 
        downloaded_image = urllib.request.urlretrieve(absolute_filename, relative_image, downloadHook)
        sys.stdout.write("\nsaved image successfully.\n")
    
    sys.stdout.write(str(count) + "/" + str(len(images)) + " downloaded \n\n")
    sys.stdout.flush()

