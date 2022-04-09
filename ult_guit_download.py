#!/bin/env python

import sys, threading
from modules.UltimateDownloader.ultimatedownloader import UltimateDownloader
from modules.YouTubeDownloader.youtubedownloader import YoutubeDownloader


options = {
    "downloadTab": False,
    "downloadYT": False,
    "tab_url": None, # Accepts UG urls
    "youtube_url": None, # Accepts any youtube url mobile/shortened/normal
    "youtube_type": "audio", # Accepts (audio, best, 1080, 720),
    "bulkYT": False
}

for a in sys.argv:
    if "guitar.com" in a:
        options["downloadTab"] = True
        options["tab_url"] = a
    elif a in ["--bulk", "--bt", "--bulktube"]:
        options["bulkYT"] = True
    elif "youtu" in a:
        options["downloadYT"] = True
        options["youtube_url"] = a
    elif "ytype=" in a:
        #options["youtube_type"]
        options["youtube_type"] = a.split("=")[1].replace('"', '')
        if options["youtube_type"] not in ["audio", "best", "1080", "720"]:
            print("Youtube media type not valid try one of these [audio, best, 1080, 720] (default to Audio Only)")
            options["youtube_type"] = "audio"

def processTab():
    UltDown = UltimateDownloader()
    if options["downloadTab"] and options["tab_url"]:
        UltDown.setURL(options["tab_url"])
        UltDown.getTab()

def processYoutube():
    YouDown = YoutubeDownloader(options["youtube_type"])
    if options["downloadYT"] and options["youtube_url"]:
        YouDown.setVideoURL(options["youtube_url"])
        YouDown.download()

def downloadYT(url=""):
    try:
        YouDown = YoutubeDownloader(options["youtube_type"])
        YouDown.setVideoURL(url)
        YouDown.download()
    except:
        print(f"[DOWNLOAD ERROR] - {url}")

def bulkYoutube():
    urls = openYTBulkFile()
    print(f"{len(urls)} bulk urls to be processed...")
    YouDown = YoutubeDownloader(options["youtube_type"])
    
    bulkThreads = []
    for url in urls:        
        # YouDown.setVideoURL(url)
        # YouDown.download()
        t = threading.Thread(target=downloadYT, args=(url,))
        t.start()
        bulkThreads.append(t)

    for t in bulkThreads:
        t.join()


def openYTBulkFile():
    result = None
    with open("youtube_list", "r") as ytFile:
        result = ytFile.read()
    
    result = result.split("\n")
    return result

if not options["bulkYT"]:
    processTab()
    processYoutube()
else:
    bulkYoutube()
