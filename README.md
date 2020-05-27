# AUTOWRITE

This tool was made to simplify and automate the process of flashing and validating devices (usually to make bootable media)

Autowrite currently has features for:
* Flashing multiple devices with a specified image file (from CLI or in prompt)
* Verifying the hash of a downloaded file
* Validating a flash device (by hashing the image file, and the flashed disk)
* Setting up a flashed device for use as a [headless](https://learn.sparkfun.com/tutorials/headless-raspberry-pi-setup/all) raspberry pi (wpa_supplicant.conf OR ssh on boot OR uart on boot)
* Blacklisting dangerous devices (like sda or nvme0n1)

# Guide:

## Installing:
  1. Install `argparse`: `sudo pip3 install --user argparse` or whatever you want (venv)
  2. Install autowrite: `git clone https://github.com/BusesCanFly/autowrite && cd ./autowrite; chmod +x autowrite.py`

## Usage:
```
usage: autowrite.py [-h] [-f IMAGE] [-d DEVICE] [-v] [--hash HASH] [-s] [-u] [-w WPA] [--rpi] [-y]

optional arguments:
  -h, --help            show this help message and exit
  -f IMAGE, --image IMAGE
                        Path to image to use
  -d DEVICE, --device DEVICE
                        Device to flash (ex/ "mmcblk0")
  -v, --validate        Validate flashed device hash
  --hash HASH           Expected hash of image file (iso, img, etc.)
  -s, --ssh             Setup headless raspi ssh
  -u, --serial          Setup headless raspi uart
  -w WPA, --wpa WPA     Path to the wpa_supplicant.conf file for headless raspi setup
  --rpi                 Same as -s -u -w
  -y, --yes             Answer yes to all prompts
```

## Notes:
  * By default, autowrite will refuse to flash `/dev/sda` or `/dev/nvme0n1`. The blacklist is found at the top of the script, uncomment/remove/add whatever is helpful.
  * "\*" is a valid answer for `-d/--device` or in the scripts prompt

## Disclaimer:
_Be careful not to overwrite any drives you don't mean to (boot, fs, etc.)_
I am not responsible for anything that happens.
