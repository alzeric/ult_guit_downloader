import os, requests, re

class UltimateDownloader:

    def __init__(self, storageLocation:str=False):
        self.name = "Ultimate Tab Downloader"
        self.data = {
            "url": None,
            "cookies_file": "cookies.txt",
            "download_url": None,
            "download_path": (os.path.join(os.getcwd(), "downloads"), storageLocation)[storageLocation],
            "download_parameters": {
                "referer": None,
                "cookie": None,
                "accept-language": "en-US,en;q=0.9",
                "accept": "*.*",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"
            }
        }
        self.createFolder()

    def setURL(self, url:str=None):
        if url:
            self.data["url"] = url

    def displayMessage(self, usermsg:str="", exitFlag:bool=False):
        msg = "".join(["*" * 20, "\n", usermsg, "\n", "*" * 20])
        print(msg)
        if exitFlag:
            exit(0) # we can pass an exit flag and stop the script in case needed (eg. not supplied expected data)

    def createFolder(self, subfolder:str=""):
        path = (self.data["download_path"], os.path.join(self.data["download_path"], subfolder))[subfolder!=""]
        if not os.path.isdir(path):
            os.mkdir(path)
            self.displayMessage(f"Downloads folder has been created here: {path}", exitFlag=False)

    def generateRequestParameters(self):
        url_split = self.data["url"].split("-")
        tab_id = url_split[len(url_split)-1]
        self.data["download_url"] = f"https://tabs.ultimate-guitar.com/download/public/{tab_id}"
        self.data["download_parameters"]["referer"] = self.data["url"]

    def downloadTablature(self):
        r = requests.get(self.data["download_url"], headers=self.data["download_parameters"], allow_redirects=False)
        content_disposition = r.headers.get("content-disposition")
        #print(r.content)
        #print(content_disposition)
        if ".gp" in content_disposition or ".ptb" in content_disposition:
            disposition_split = content_disposition.split(";")
            filename = None
            for d in disposition_split:
                if "filename=" in d:
                    filename = d.replace("filename=", "").replace('"', "").replace(";", "").replace(" ", "")
                    break
            badchars= re.compile(r'[^A-Za-z0-9_.]+|^\.|\.$|^ | $|^$')
            cleansed_filename =  badchars.sub('_', filename)
            cleaned = os.path.join(self.data["download_path"],  cleansed_filename)
            print(cleaned)
            f = open(cleaned, "wb")
            f.write(r.content)
            f.close()

    def getTab(self):
        self.getCookies()
        self.generateRequestParameters()

        if self.data["download_url"] and self.data["download_parameters"]["referer"]:
            self.downloadTablature()

    def getCookies(self):
        if not os.path.exists(self.data["cookies_file"]):
            cookies_file = self.data["cookies_file"]
            msg = "".join([f"[Missing {cookies_file}]","\nLogin to Ultimate-Guitar then open inspector window Cntr+Shift+I (chrome)", f"\ntype document.cookie copy the text that appears and create a {cookies_file} file in this dirctory and paste the contents and save"])
            self.displayMessage(msg, exitFlag=True)
        else:
            f = open(self.data["cookies_file"], "r")
            self.data["download_parameters"]["cookie"] = f.read()
            f.close()

    