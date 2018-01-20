https://blog.rapid7.com/2017/11/30/announcing-the-metasploitable3-community-ctf/
https://metasploitable3ctf.com/
```
nmap -v -sV -sC -oA target 10.0.84.99

Starting Nmap 7.60 ( https://nmap.org ) at 2017-12-04 17:49 UTC
NSE: Loaded 146 scripts for scanning.
NSE: Script Pre-scanning.
Initiating NSE at 17:49
Completed NSE at 17:49, 0.00s elapsed
Initiating NSE at 17:49
Completed NSE at 17:49, 0.00s elapsed
Initiating Ping Scan at 17:49
Scanning 10.0.84.99 [2 ports]
Completed Ping Scan at 17:49, 0.00s elapsed (1 total hosts)
Initiating Parallel DNS resolution of 1 host. at 17:49
Completed Parallel DNS resolution of 1 host. at 17:49, 0.00s elapsed
Initiating Connect Scan at 17:49
Scanning 10.0.84.99 [1000 ports]
Discovered open port 21/tcp on 10.0.84.99
Discovered open port 80/tcp on 10.0.84.99
Discovered open port 22/tcp on 10.0.84.99
Discovered open port 3306/tcp on 10.0.84.99
Discovered open port 445/tcp on 10.0.84.99
Discovered open port 8181/tcp on 10.0.84.99
Discovered open port 631/tcp on 10.0.84.99
Completed Connect Scan at 17:49, 4.41s elapsed (1000 total ports)
Initiating Service scan at 17:49
Scanning 7 services on 10.0.84.99
Stats: 0:00:11 elapsed; 0 hosts completed (1 up), 1 undergoing Service Scan
Service scan Timing: About 42.86% done; ETC: 17:49 (0:00:08 remaining)
Completed Service scan at 17:49, 6.12s elapsed (7 services on 1 host)
NSE: Script scanning 10.0.84.99.
Initiating NSE at 17:49
Completed NSE at 17:50, 40.10s elapsed
Initiating NSE at 17:50
Completed NSE at 17:50, 0.00s elapsed
Nmap scan report for 10.0.84.99
Host is up (0.00069s latency).
Not shown: 992 filtered ports
PORT     STATE  SERVICE     VERSION
21/tcp   open   ftp         ProFTPD 1.3.5
22/tcp   open   ssh         OpenSSH 6.6.1p1 Ubuntu 2ubuntu2 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   1024 2b:1e:ef:45:d5:ce:70:a0:ce:34:4e:f3:e4:7c:80:42 (DSA)
|   2048 9f:e5:65:74:1a:95:18:6f:1a:36:12:25:cc:74:df:48 (RSA)
|_  256 f1:eb:79:1f:27:4d:ab:2c:32:a7:b8:c6:28:40:a9:98 (ECDSA)
80/tcp   open   http        Apache httpd 2.4.7
| http-ls: Volume /
| SIZE  TIME              FILENAME
| -     2017-11-07 16:42  chat/
| -     2011-07-27 20:17  drupal/
| 1.7K  2017-11-07 16:42  payroll_app.php
| -     2013-04-08 12:06  phpmyadmin/
|_
| http-methods:
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: Apache/2.4.7 (Ubuntu)
|_http-title: Index of /
445/tcp  open   netbios-ssn Samba smbd 4.3.11-Ubuntu (workgroup: WORKGROUP)
631/tcp  open   ipp         CUPS 1.7
| http-methods:
|   Supported Methods: GET HEAD OPTIONS POST PUT
|_  Potentially risky methods: PUT
| http-robots.txt: 1 disallowed entry
|_/
|_http-server-header: CUPS/1.7 IPP/2.1
|_http-title: Home - CUPS 1.7.2
3000/tcp closed ppp
3306/tcp open   mysql       MySQL (unauthorized)
8181/tcp open   http        WEBrick httpd 1.3.1 (Ruby 2.3.5 (2017-09-14))
| http-methods:
|_  Supported Methods: GET HEAD
|_http-server-header: WEBrick/1.3.1 (Ruby/2.3.5/2017-09-14)
|_http-title: Site doesn't have a title (text/html;charset=utf-8).
Service Info: Hosts: 10.0.84.99, IP-10-0-84-99; OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Host script results:
| smb-os-discovery:
|   OS: Windows 6.1 (Samba 4.3.11-Ubuntu)
|   Computer name: ip-10-0-84-99
|   NetBIOS computer name: IP-10-0-84-99\x00
|   Domain name: \x00
|   FQDN: ip-10-0-84-99
|_  System time: 2017-12-04T17:49:40+00:00
| smb-security-mode:
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-security-mode:
|   2.02:
|_    Message signing enabled but not required
| smb2-time:
|   date: 2017-12-04 17:49:41
|_  start_date: 1601-01-01 00:00:00

NSE: Script Post-scanning.
Initiating NSE at 17:50
Completed NSE at 17:50, 0.00s elapsed
Initiating NSE at 17:50
Completed NSE at 17:50, 0.00s elapsed
Read data files from: /usr/bin/../share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 51.88 seconds
```
