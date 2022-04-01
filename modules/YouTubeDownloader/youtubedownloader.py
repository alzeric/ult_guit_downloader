from youtube_dl.YoutubeDL import YoutubeDL
import json, os

class MyLogger(object):
    def debug(self, msg):
        pass
    def warning(self, msg):
        pass
    def error(self, msg):
        pass

class MyHook():
    def __init__(self, d):
        if d['status'] == 'finished':
            print('Done downloading youtube audio, now converting ...')

class YoutubeDownloader:

    def __init__(self, actionType:str="a"):
        self.name = "Youtube Downloader"
        self.videoURL = None
        self.exts = {'audio': 'mp3', 'video': 'mp4'}
        self.action_mode = {
            "audiobest": {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '320',
                }],
                'logger': MyLogger(),
                'progress_hooks': [MyHook],
            },
            "videobest": { # Video formats are a work in progress and are not activated currently
                'format': 'bestvideo/best+bestaudio/best',
                'progress_hooks': [MyHook]
            },
            "video1080": {
                'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]',
                'progress_hooks': [MyHook]
            },
            "video720": {
                'format': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
                'progress_hooks': [MyHook]
            },
        }
        self.youtubeOptions = None
        if actionType == "a":
            self.youtubeOptions = self.action_mode["audiobest"]
        elif actionType == "vb":
            self.youtubeOptions = self.action_mode["videobest"]
        elif actionType == "v720":
            self.youtubeOptions = self.action_mode["video720"]
        elif actionType == "v1080":
            self.youtubeOptions = self.action_mode["video1080"]
        else:
            self.youtubeOptions = self.action_mode["audiobest"]
        
    def setVideoURL(self, videoURL:str=None):
        self.videoURL = videoURL
        
        with YoutubeDL(self.youtubeOptions) as ydl:
            info_dict = ydl.extract_info(self.videoURL, download=False)
            video_id = info_dict.get("id", None)
            video_title = info_dict.get('title', None)
            video_ext = info_dict.get('ext', None)
            print(f"Title: {video_title}")
            print(f"Ext: {video_ext}")
            filename = f"{video_title}.{video_ext}"
            self.youtubeOptions["outtmpl"] = os.path.join("downloads", filename)
            print(self.youtubeOptions)
            
    def download(self):
        with YoutubeDL(self.youtubeOptions) as ydl:
            ydl.download([self.videoURL])

    def debug_json(self, json_string):
        with open('json_debug.json', 'w') as outfile:
            json.dump(json_string, outfile)