# Mirai - 10.10.10.48

## Nmap Scan
```
nmap -A -v -n -p- 10.10.10.48
```

Machine was running openssh 6.7p1 and lighthttpd 1.4.35

## Run Nikto
Visit the webpage which was blank, so run nikto to dicover any other pages/interesting stuff
```
nikto --host 10.10.10.48
```
Discover, /admin/ page and realize the host is running pihole.

## SSH Login
Mirai relied on machines running default creds, so naturally check default ssh creds to get user privledges and first flag.

## Root login
```
sudo su #l33t 0-day hack
```

## But the flag isn't there!
File which says that flag might be on a usb drive
```
root@raspberrypi:~# cat root.txt
I lost my original root.txt! I think I may have a backup on my USB stick...
```

## Check the usb stick!
```
root@raspberrypi:~# cat /media/usbstick/damnit.txt
Damnit! Sorry man I accidentally deleted your files off the USB stick.
Do you know if there is any way to get them back?

-James

```
cmon james, get your life together

## File Recovery
```
root@raspberrypi:~# fdisk -l

Disk /dev/sda: 10 GiB, 10737418240 bytes, 20971520 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0x0eddfb88

Device     Boot   Start      End  Sectors  Size Id Type
/dev/sda1  *         64  2709119  2709056  1.3G 17 Hidden HPFS/NTFS
/dev/sda2       2709504 20971519 18262016  8.7G 83 Linux

Disk /dev/sdb: 10 MiB, 10485760 bytes, 20480 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk /dev/loop0: 1.2 GiB, 1297825792 bytes, 2534816 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 byte
```

Sick 10mb usb stick bro

```
hexdump -C /dev/sdb
```
Offset 0080a800 is pretty cool
