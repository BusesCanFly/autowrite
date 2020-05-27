#!/usr/bin/python3

# Rewrite of github.com/BusesCanFly/autowrite in better python
# (more comfort features than would be easy to make in bash)

import os
import argparse
import subprocess
# while `import blkinfo` exists, I'd rather parse lsblk myself

indent = ' '*2
hashType = "sha256sum" # bash command used in validating flash
mountpoint = f"/media/{os.getlogin()}"
#mountpoint = f"/run/media/{os.getlogin()}" # uncomment for fedora where devices are in /run/media/, not /media/

exclude = [
	"nvme0n1"
	,"sda" 	# comment this line out to allow flashing /dev/sda (if that is not your host disk)
]

def args():
	parser = argparse.ArgumentParser()
	parser.add_argument("-f", "--image", type=str, help="Path to image to use")
	parser.add_argument("-d", "--device", type=str, help="Device to flash (ex/ \"mmcblk0\")")
	parser.add_argument("-v", "--validate", action="store_true", help="Validate flashed device hash")
	parser.add_argument("--hash", type=str, help="Expected hash of image file (iso, img, etc.)")
	parser.add_argument("-s", "--ssh", action="store_true", help="Setup headless raspi ssh")
	parser.add_argument("-u", "--serial", action="store_true", help="Setup headless raspi uart")
	parser.add_argument("-w", "--wpa", type=str, help="Path to wpa_supplicant.conf for headless raspi setup")
	parser.add_argument("--rpi", action="store_true", help="Same as -s -u -w")
	parser.add_argument("-y", "--yes", action="store_true", help="Skip all prompts")
	return parser.parse_args()

def diskInfo():
	lsblk = subprocess.getoutput("lsblk -r -o NAME,LABEL,TYPE").split("\n")

	devices = []
	partitions = []

	for line in lsblk:
		line = line.strip("`")
		line = line.split()
		if "loop" not in line[0]:
			if len(line) == 2: # Disk, or part with no label
				if "disk" in line[1]:
					devices.append(line[0]) # device name
				if "part" in line[1]:
					partitions.append(line[0]) # partition /dev/ name
			if len(line) == 3: # Disk or part with label
				if "disk" in line[2]:
					devices.append(line[0])
				if "part" in line[2]:
					partitions.append([line[0], line[1]]) # [label, /dev/ name]

	deviceInfo = []
	deviceInfo.append(devices)
	deviceInfo.append(partitions)
	return deviceInfo # [devices, partitions]

def getPartitions(device):
	partitions = []
	devInfo = subprocess.getoutput(f"lsblk -r -o NAME,LABEL,TYPE /dev/{device}").split("\n")
	for line in devInfo:
		line = line.split()
		if len(line) == 3: # Don't need to get device info
			if "part" in line[2]:
				partitions.append([line[0], line[1]]) # [label, /dev/ name]
	return partitions

def menu(devices, partitions):
	print("[*] Found devices:")
	for device in devices:
		print(f"{indent}[{devices.index(device) + 1}]: {device}")
		for partition in partitions:
			if len(partition) == 2: # partition has label
				if device in partition[0]:
					print(f"{indent*2} ╚═> {partition[1]}")
			else:
				if device in partition:
					print(f"{indent*2} ╚═> {partition}")

	toFlash = []
	devs = input("\n[~] Enter device number to flash, comma separated (or \"*\" for all devices): ")
	if devs == "*":
		for device in devices:
			if device not in exclude:
				toFlash.append(device)
			else:
				print(f"[!] {device} is in the exclude list, skipping flash.")
	else:
		for dev in devs.split(","):
			device = devices[int(dev) - 1]
			input(f"[!] You are about to reflash device /dev/{device}, press [ENTER] to confirm ")
			if device not in exclude:
				toFlash.append(device)
			else:
				print(f"[!] {device} is in the exclude list, skipping flash.")
				print("[^] Check the top of the script to find excluded device names.")
	return toFlash

def imagePrompt():
	return input("\n[~] Enter path to image file: ")

def flash(device, image):
	print(f"\n[*] Starting flash of {device}")
	subprocess.call(f"sudo dd bs=4M if={image} of=/dev/{device} status=progress conv=fsync", shell=True)

def hashCheck():
	status = ""
	while status == "":
		continue_answer = input("[?] Continue? [y/n]: ")
		if continue_answer == "y" or continue_answer == "Y":
			status = "continue"
		elif continue_answer == "n" or continue_answer == "N":
			status = "exit"
		else:
			print("[-] Answer with \"y\" or \"n\"")	
	if status == "exit":
		print("[!] Exiting!")
		os._exit(1)	

def imgHashCheck(image, isoHash):
	status = False
	fileHash = subprocess.getoutput(f"{hashType} {image}").split()[0]
	if fileHash == isoHash:
		status = True
	return status

def imgHashContinue():
	status = ""
	while status == "":
		continue_answer = input(f"[?] Continue? [y/n]: ")
		if continue_answer == "y" or continue_answer == "Y":
			status = "continue"
		elif continue_answer == "n" or continue_answer == "N":
			status = "exit"
		else:
			print("[-] Answer with \"y\" or \"n\"")	

	if status == "continue":
		return True
	elif status == "exit":
		print("[!] Exiting!")
		os._exit(3)

def validate(device, image):
	print(f"\n[*] Validating flash of {device}")
	deviceHash = subprocess.getoutput(f"sudo head -c $(stat -c '%s' {image}) /dev/{device} | {hashType}").split()[0]
	fileHash = subprocess.getoutput(f"{hashType} {image}").split()[0]
	if deviceHash == fileHash:
		print("[+] Hashes match- flash successful!")
	else:
		print("[-] Hash mismatch- flash failed.")
		if not args.yes:
			hashCheck()	

def rpiSetup(device):
	foundBoot = False
	mount = f"{mountpoint}/boot"
	diskparts = getPartitions(device)
	for partition in diskparts:
		if partition[1] == "boot":
			foundBoot = True
			mountBoot(partition, mount)
			if args.ssh or args.rpi:
				if not os.path.isfile(f"{mount}/ssh"):
					os.mknod(f"{mount}/ssh")
					print("[+] Created ssh file")
				else:
					print("[*] ssh file already present")
			if args.serial or args.rpi:
				with open(f"{mount}/config.txt", "a") as config:
					config.write("enable_uart=1\n")
				print("[+] Edited config.txt to enable UART")
			if args.wpa or args.rpi:
				subprocess.call(f"cp {args.wpa} {mount}/wpa_supplicant.conf", shell=True)
				print(f"[+] Copied {args.wpa} to boot partition")
		umount(f"/dev/{partition[0]}") # True means delete the mountpoint dir	

	os.rmdir(mount)
	if not foundBoot:
		print(f"[-] {device} partition \"boot\" not found. Exiting!")
		os._exit(2)


def mountBoot(partition, mount):
	if not os.path.isdir(mount):
		print("[*] Making mount folder.")
		os.mkdir(mount)
	elif not os.path.ismount(mount):
		subprocess.call(f"mount /dev/{partition[0]} {mount}", shell=True)
		print(f"[+] Mounted /dev/{partition[0]} to {mount}")
		return
	else:
		print(f"[-] Mountpoint {mount} already exists")
		if not args.yes:
			checkUmount(partition, mount) # mountpoint already exists	
		else:
			umount(mount)

def checkUmount(partition, mount):
	status = ""
	while status == "":
		umount_answer = input(f"[?] Unmount {mount}? [y/n]: ")
		if umount_answer == "y" or umount_answer == "Y":
			status = "umount"
		elif umount_answer == "n" or umount_answer == "N":
			status = "exit"
		else:
			print("[-] Answer with \"y\" or \"n\"")	

	if status == "umount":
		umount(mount)
		print(f"[+] Unmounted {mount}")
		mountBoot(partition, mount)
	elif status == "exit":
		print("[!] Exiting!")
		os._exit(3)

def umount(mount):
	subprocess.call(f"umount -f {mount}", shell=True)

if __name__ == '__main__':

	args = args()

	if not args.device:
		deviceInfo = diskInfo()
		devices = deviceInfo[0]
		partitions = deviceInfo[1]
		toFlash = menu(devices, partitions)
	else:
		if args.device == "all" or args.device == "*":
			deviceInfo = diskInfo()
			toFlash = deviceInfo[0]
		else:
			toFlash = [args.device]

	if not args.image:
		image = imagePrompt()
	else:
		image = args.image

	if args.hash:
		if imgHashCheck(image, args.hash):
			print(f"\n[+] Image file hash matches expected hash")
		else:
			print(f"\n[-] Image file mismatch with expected hash")
			imgHashContinue()

	for device in toFlash:
		flash(device, image)
		if args.validate:
			validate(device, image)
		if args.ssh or args.wpa:
			rpiSetup(device)