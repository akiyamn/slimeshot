import subprocess
import requests
import sys
from .config import *

"""
Container module for the Screenshot class
"""

class Screenshot:
    """
    Sends image data various places, dictated by its driver class: SSDriver.

    This class represents a single screenshot instance, which saves its result from maim into a path
    defined in config.ini. This class does not interface with the user except quitting if a right click is detected.
    """

    def clipboard(self, data):
        """
        Sends string data to the clipboard via stdin through xclip.
        :param data: the string to be added to the clipboard
        """
        p = subprocess.Popen(["xclip", "-selection", "clipboard"], stdin=subprocess.PIPE)
        p.stdin.write(data.encode())
        p.stdin.close()

    def clip(self):
        """
        Takes a screenshot using the selection interface of maim. Saves it to the image path
        specified in config.ini
        Quits on detection of a right click.
        :return: an error as a string in the case of an error. An empty string otherwise.
        """
        maim = subprocess.Popen(["maim", "-s", IMG_PATH], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        maim.wait()
        out, err = maim.communicate()
        err = err.decode()
        if "right-click" in err:
            sys.exit(0)  # Exit on right click
        else:
            return err

    def imageToClipboard(self, imagePath):
        """
        Sends a png image to the clipboard via xclip.
        :param imagePath: the path to the png image file to be uploaded
        """
        subprocess.Popen(["xclip", "-selection", "clipboard", "-t", "image/png", "-i", imagePath])

    def post(self, key):
        """
        Posts the image at the image path defined in config.ini to the server defined in config.ini
        :param key: the personal key (string) of the user needed to access the service
        :return: a requests.post() object containing the information of the attempted request.
        """
        with open(IMG_PATH, "rb") as img:
            req = requests.post(URL, files={"photo": img}, data={"pass": key})
            img.close()
            return req
