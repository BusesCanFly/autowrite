#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import argparse
from time import sleep
from termcolor import colored, cprint

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--image', type=str,
                    help='Path to image to use')
parser.add_argument('-v', dest='verbose', action='store_true',
                    help='Enable dd\'s status=progress')
parser.add_argument('--no-sda', action='store_true', dest='rpi',
                    help='Ignore /dev/sda')
parser.add_argument('--validate', action='store_true',
                    help='Image the drive and compare it to the original image')
parser.add_argument('-e', '--eject', action='store_true',
		    help='Unmount drive after finishing flashing/validation')
parser.add_argument('--safe', action='store_true',
                    help='Print, not dd')
args = parser.parse_args()

global ignore
global verbose

if args.rpi:
        ignore=' | grep -v sda '
else:
	ignore=' '

if args.verbose:
        verbose=' status=progress '
else:
        verbose=' '

cprint("Locating storage devices to write to...", "green")
os.system("lsblk -i | grep disk | cut -d\  -f1 | grep -iE \"sd|mmcblk|hdd\""+ignore+" > ./devices.txt")

list = './devices.txt'
with open(list) as inf:
                devices = [line.strip() for line in inf]
os.system("rm ./devices.txt")

cprint("NOTE: use --no-sda to disable writing to /dev/sda if that is your host disk", "red")

if args.verbose or args.safe:
	c=0
	cprint("Located devices:", "yellow")
	while c < len(devices):
		print("/dev/"+devices[c])
		c+=1
	print(raw_input(colored("\nPress any key to proceed to imaging ", "green")))

if not args.safe:
	i=0
	while i < len(devices):
		start_msg = colored("Starting write to ", "green")+colored("/dev/"+devices[i], "yellow")
	        print(start_msg)
	        os.system("sudo dd bs=4M if="+args.image+" of=/dev/"+devices[i]+verbose+"conv=fsync")
	        cprint("Write complete", "green")
	        sleep(1)
	        if args.validate:
		        count=raw_input(colored("\nEnter the number before \"+0 records out\" to validate: ", "yellow"))
		        os.system("sudo dd bs=4M if=/dev/"+devices[i]+verbose+" of=./images/SDCARD.img count="+count)
		        cprint("Comparing disk image to original... ", "green")
		        os.system("diff -s ./images/SDCARD.img "+args.image)
		        sleep(1)
		        os.system("rm ./images/SDCARD.img")
		if args.eject:
                        os.system('sudo umount /dev/'+devices[i]+'*')
		i+=1
else:
	i=0
	while i < len(devices):
		start_msg = colored("\nStarting write to ", "green")+colored("/dev/"+devices[i], "yellow")
	        print(start_msg)
	        print("sudo dd bs=4M if="+args.image+" of=/dev/"+devices[i]+verbose+"conv=fsync")
	        cprint("Write complete", "green")
	        sleep(1)
	        if args.validate:
		        count=raw_input(colored("\nEnter the number before \"+0 records out\" to validate: ", "yellow"))
		        print("sudo dd bs=4M if=/dev/"+devices[i]+verbose+" of=./images/SDCARD.img count="+count)
		        cprint("Comparing disk image to original... ", "green")
		        print("diff -s ./images/SDCARD.img "+args.image)
		        sleep(1)
		        print("rm ./images/SDCARD.img")
		if args.eject:
			print('sudo umount /dev/'+devices[i]+'*')
		i+=1
