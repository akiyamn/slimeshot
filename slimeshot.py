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


# Sends 'data' to the clipboard
def clipboard(data):
    p = subprocess.Popen(['xclip', '-selection', 'clipboard'], stdin=subprocess.PIPE)
    p.stdin.write(data.encode())
    p.stdin.close()


# Opens maim and allows the user to make a screenshot
## Returns whether the screenshot was successful
def clip():
    maim = subprocess.Popen(["maim", "-s", "temp.png"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = maim.communicate()
    err = err.decode()
    print(err)
    if err == "":
        return True
    else:
        return False

# Sends a POST request to the screenshot server including the screenshot and the key
## Returns text sent back from the server
def post():
    with open("temp.png", "rb") as img:
        req = requests.post(url, files={"photo": img}, data={"pass": key})
        img.close()
        return req.text


# Sends a GNU/Linux notification via 'notify-send'
def notify(title, text="", icon=""):
    subprocess.Popen(["notify-send", "-i", icon, title, text])


# Sends an error notification to the user via 'notify-send'
def showError(error):
    notify("Error", error)


message = ""
error = ""

if clip():
    message = post()
else:
    showError("Error" , "Failed to clip the specified region!")

if message != "You fucked up.":
    clipboard(message)
    notify("Screenshot successful!", message, thisDir + "/temp.png")
    playsound("success.mp3")
else:
    showError("Server failed to upload the screenshot.")
