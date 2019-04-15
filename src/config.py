import argparse

__version__ = "0.4.0"

URL = 'https://slimecorp.biz/i/pics.php'
KEY_PATH = "../key.txt"
SOUND_PATH = "../assets/success.wav"
IMG_PATH = "../assets/temp.png"

# Argument Parsing
parser = argparse.ArgumentParser(description="A simple Python-based screenshot program for slimecorp.biz/i.")
parser.add_argument("--version", action="version", version="%(prog)s " + __version__)
parser.add_argument("-q", "--quiet", help="mutes all sound, text and notification output", action='store_true')
parser.add_argument("-r", "--reset", help="resets the key stored in key.txt to be empty", action='store_true')
parser.add_argument("--dryrun", help="takes a screenshot without uploading it", action='store_true')
parser.add_argument("--silent", help="disables audio output", action='store_true')
args = parser.parse_args()

if args.quiet:
    args.silent = True
