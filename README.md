# slimeshot.py

A simple screenshot script/program built for GNU/Linux which uploads to the [slimecorp.biz/i](http://slimecorp.biz/i) platform.
Written for the GNU/Linux platform, based on Python 3.6.


## Usage
`python3 slimeshot.py`

A file must be created in the main directory, called `key.txt`.
This file must include only one line, which is a valid key
for the [slimecorp.biz/i](http://slimecorp.biz/i) platform to function correctly.


## Depends on

### Packages
-   python3
-   maim
-   xclip (required by maim)
-   pip (to install Python libs)

### Python Libs
-   request
-   playsound
