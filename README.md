# Autowrite
Automate dd'ing and verifying SD cards

This tool is useful for when you need to flash many SD cards/drives with a certain .iso/.img/etc. Autowrite automatically detects all plugged in disks and starts flashing them with the specified image.

![alt text](https://github.com/BusesCanFly/autowrite/blob/master/screenshot.png "Who doesn't love ASCII art?")

# GUIDE:

## Installation
1. Install dependencies: `sudo pip install -U argparse termcolor`
2. Download autowrite: `git clone https://github.com/BusesCanFly/autowrite`
3. Navigate to autowrite: `cd ./autowrite`
4. Make autowrite.py executable `chmod +x autowrite.py`
* One line variant: `sudo pip install -U argparse termcolor && git clone https://github.com/BusesCanFly/autowrite && cd ./autowrite && chmod +x autowrite.py`

## Images
Place desired image into `autowrite/images/`
* Examples: 
    * [Raspbian](https://www.raspberrypi.org/downloads/raspbian/)
    * [Kali](https://www.kali.org/downloads/)
    * [Ubuntu](https://www.ubuntu.com/download)

## Raspberry pi headless setup
* [It is possible](https://www.raspberrypi.org/forums/viewtopic.php?t=191252) to have your raspberry pi connect to a wifi network and open up ssh when it boots, so no screen, keyboard, or mouse is required for setup (this is known as "headless" operation)
* with `--rpi`, autowrite will automatically create the necessary config files for headless operation of a raspberry pi
	* Just edit `./images/wpa_supplicant.conf` and change the SSID and password to whatever you want to use

## Usage
```
usage: autowrite.py [-h] [-f IMAGE] [--no-sda] [--validate] [--rpi]

optional arguments:
  -h, --help            show this help message and exit
  -f IMAGE, --image IMAGE
                        Path to image to use
  --no-sda              Ignore /dev/sda
  --validate            Image the drive and compare it to the original image
  --rpi                 Enable ssh and wpa_supplicant on boot
                        (wpa_supplicant.conf from ~/images)
```
* Example: `./autowrite.py --no-sda -f ./images/raspbian.img --validate --rpi`
	* This will flash raspbian.img to every device that isn't /dev/sda, validate that the flashed disk is not corrupted, and then setup the config files for headless operation
* If running autowrite on a raspberry pi, use the `--no-sda` flag to prevent overwriting /dev/sda, the pi's internal SD card

## Disclaimer
_Be careful not to overwrite your host's main drive_

I am not responsible for anything that happens
