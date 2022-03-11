import sys, os, requests

class UltimateDownloader:

    def __init__(self):
        self.name = "Ultimate Guitar Tab Downloader"
        self.url = None
        self.cookies_file = "cookies.txt"
        self.download_url = None
        self.download_path = os.path.join(os.getcwd(), "downloads")
        self.download_parameters = {
            "Referer": None,
            "Cookie": None,
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "*.*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"
        }        
        self.createFolder()

    def createFolder(self):        
        if not os.path.isdir(self.download_path):
            os.mkdir(self.download_path)
            self.displayMessage(f"Downloads folder has been created here: {self.download_path}")

    def getTab(self):
        self.getCookies()
        self.generateRequestParameters()
        if self.download_url and self.download_parameters["Referer"]:
            self.downloadTablature()

    def getCookies(self):
        if not os.path.exists("cookies.txt"):
            msg = "[Missing cookies.txt]"
            msg = msg + "\n\nLogin to Ultimate-Guitar then open inspector window Cntr+Shift+I (chrome)"
            msg = msg + "\ntype document.cookie copy the text that appears and create a cookies.txt file in this dirctory and paste the contents and save"
            self.displayMessage(msg)
            exit(0)
        else:
            f = open(self.cookies_file, "r")
            self.download_parameters["Cookie"] = f.read()
            f.close()
    
    def generateRequestParameters(self):
        url_split = self.url.split("-")
        tab_id = url_split[len(url_split) - 1]        
        self.download_url = f"https://tabs.ultimate-guitar.com/download/public/{tab_id}"
        self.download_parameters['Referer'] = self.url

    def downloadTablature(self):
        r = requests.get(self.download_url, headers=self.download_parameters, allow_redirects=False)
        content_disposition = r.headers.get("content-disposition")
        if ".gp" in content_disposition:
            disposition_split = content_disposition.split(";")
            for d in disposition_split:
                if "filename=" in d:
                    filename = d.replace("filename=", "").replace('"', "").replace(";", "").replace(" ", "")
                    break
            f = open(os.path.join(self.download_path, filename), "wb")
            f.write(r.content)
            f.close()

    def displayMessage(self, msg):
        print("\n")
        print("*" * 20)
        print(msg)
        print("*" * 20)
        print("\n")

UltDown = UltimateDownloader()

if len(sys.argv) == 2:
    UltDown.url = sys.argv[1]
    UltDown.getTab()
else:
    UltDown.displayMessage(f'[USAGE: python {sys.argv[0]} https://tabs.ultimate-guitar.com/tab/EXAMPLE/EXAMPLE-SONG-TITLE-12345678]')
    exit(0)
