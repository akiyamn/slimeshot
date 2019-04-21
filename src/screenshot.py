import subprocess
import requests
import sys
from config import *


class Screenshot:
    # Sends 'data' to the clipboard
    def clipboard(self, data):
        p = subprocess.Popen(["xclip", "-selection", "clipboard"], stdin=subprocess.PIPE)
        p.stdin.write(data.encode())
        p.stdin.close()

    # Opens maim and allows the user to make a screenshot
    ## Returns whether the screenshot was successful
    def clip(self):
        maim = subprocess.Popen(["maim", "-s", IMG_PATH], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        maim.wait()
        out, err = maim.communicate()
        err = err.decode()
        if "right-click" in err:
            sys.exit(0)
        else:
            return err

    def imageToClipboard(self, imagePath):
        subprocess.Popen(["xclip", "-selection", "clipboard", "-t", "image/png", "-i", imagePath])

    # Sends a POST request to the screenshot server including the screenshot and the key
    ## Returns text sent back from the server
    def post(self, key):
        with open(IMG_PATH, "rb") as img:
            req = requests.post(URL, files={"photo": img}, data={"pass": key})
            img.close()
            return req
