import subprocess
import requests
from playsound import playsound
import os

url = 'http://slimecorp.biz/i/pics.php'
thisDir = os.path.dirname(os.path.realpath(__file__))
os.chdir(thisDir)

keyFile = open("key.txt", "rb")
key = keyFile.read().decode()
keyFile.close()


def clipboard(data):
    p = subprocess.Popen(['xclip', '-selection', 'clipboard'], stdin=subprocess.PIPE)
    p.stdin.write(data.encode())
    p.stdin.close()


def clip():
    maim = subprocess.Popen(["maim", "-s", "temp.png"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = maim.communicate()
    err = err.decode()
    print(err)
    if err == "":
        return True
    else:
        return False


def post():
    with open("temp.png", "rb") as img:
        req = requests.post(url, files={"photo": img}, data={"pass": key})
        img.close()
        return req.text


def notify(title, text="", icon=""):
    subprocess.Popen(["notify-send", "-i", icon, title, text])


message = ""
cancelled = False

if clip():
    message = post()
else:
    cancelled = True

if message != "":
    clipboard(message)
    notify("Screenshot successful!", message, thisDir + "/temp.png")
    playsound("success.mp3")
elif not cancelled:
    notify("It fucked up.", message)
