import argparse
import os.path
import configparser as cp

os.chdir(os.path.abspath(os.path.dirname(__file__)))

# Static globals
__version__ = "0.5.0-indev"
CONFIG_PATH = "../config.ini"

# Read from config file
config = cp.ConfigParser()
config.read(CONFIG_PATH)

URL = config["URLS"]["img_url"]
KEY_PATH = config["PATHS"]["key"]
SOUND_PATH = config["PATHS"]["sound"]
IMG_PATH = config["PATHS"]["temp_img"]

# Argument parsing
parser = argparse.ArgumentParser(description="A simple Python-based screenshot program for slimecorp.biz/i.")
parser.add_argument("--version", action="version", version="%(prog)s " + __version__)
parser.add_argument("-c", "--clipboard", help="sends the image itself to the clipboard rather than uploading it",
                    action='store_true')
parser.add_argument("-q", "--quiet", help="mutes all sound, text and notification output", action='store_true')
parser.add_argument("-r", "--reset", help="resets the key stored in key.txt to be empty", action='store_true')
parser.add_argument("--dryrun", help="takes a screenshot without uploading it", action='store_true')
parser.add_argument("--silent", help="disables audio output", action='store_true')
args = parser.parse_args()

if args.quiet:
    args.silent = True

