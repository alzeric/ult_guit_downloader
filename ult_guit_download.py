#!/bin/env python

import sys

from click import option
from modules import YouTubeDownloader
from modules.UltimateDownloader.ultimatedownloader import UltimateDownloader
from modules.YouTubeDownloader.youtubedownloader import YoutubeDownloader

options = {
    "downloadTab": False,
    "downloadYT": False,
    "tab_url": None, # Accepts UG urls
    "youtube_url": None, # Accepts any youtube url mobile/shortened/normal
    "youtube_type": "audio" # Accepts (audio, best, 1080, 720)
}

for a in sys.argv:
    if "guitar.com" in a:
        options["downloadTab"] = True
        options["tab_url"] = a
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

processTab()
processYoutube()
