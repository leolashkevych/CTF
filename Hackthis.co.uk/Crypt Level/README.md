# Crypt Levels

## Lvl 1
Reverse the text in the box.
```javascript
("blockquote")[0].innerHTML.split("").reverse().join("")
```
## Lvl 2
```
Aipgsqi fego, xlmw pizip mw rsx ew iewc ew xli pewx fyx wxmpp rsx xss gleppirkmrk. Ws ks elieh erh irxiv xlmw teww: wlmjxxlexpixxiv
```
Caesar cipher, alphabet shift is 4.
## Lvl 3
```
.... .. --..-- / - .... .- -. -.- ... / - --- / ... .- -- ..- . .-.. / -- --- .-. ... . / - .... . / - .-. .- -. ... -- .. ... ... .. --- -. / --- ..-. / - . .-.. . --. .-. .- .--. .... .. -.-. / .. -. ..-. --- .-. -- .- - .. --- -. / .-- .- ... / ... - .- -. -.. .- .-. -.. .. --.. . -.. .-.-.- / .... . / ..- ... . -.. / -.. --- - ... / .- -. -.. / -.. .- ... .... . ... / - --- / -.-. .-. . .- - . / .- / ... - .- -. -.. .- .-. -.. / .-- .- -.-- / --- ..-. / -.-. --- -- -- ..- -. .. -.-. .- - .. --- -. --..-- / .... . / .... .- ... / .... . .-.. .--. . -.. / -.-- --- ..- / - --- -.. .- -.-- / - --- / --. . - / - .... . / .--. .- ... ... ---... / - .... .- -. -.- -.-- --- ..- ... .. .-.
```
SOS! It's Morse code.
## Lvl 4
```
Dc, gdcl cl h lcrcshn ckqh gz sqwqs guz. Gdcl gcrq qhyd sqggqn cl hllcomqk h ljqycacqk nqshgczmldcj ucgd hmzgdqn sqggqn. Jhll: cdhwqancqmkl
```
[Substitution cipher](https://en.wikipedia.org/wiki/Substitution_cipher) seems useful
## Lvl 5
```
qoymlNlpY :ccdf lpy yzJ .qoh ln lxigqoh qlxlm eeiw zot ydpy gmipylnoC ,zot gmiyqdncyzo ho ydpy ci lniqk tN .lsie sooe tlpy ydpw yom ,smipy amd tdc tlpy ydpw tj lefolf gmigazb ho ydpy ci lniqk tN .tyicoiqzk ho ydpy ci lniqk tN .edminiqk d nd i clT
```
See [Lvl 1](#Lvl 1) & [Lvl 4](#Lvl 4)
## Lvl 6

- Visualize .wav file with [Audacity](http://www.audacityteam.org) (or whatever).
![Sick Tunes](https://github.com/leolashkevych/CTF/blob/master/Hackthis.co.uk/Crypt%20Level/Crypt-Lvl-6.png?raw=true "Sick tunes")

- [Maya numerals](https://en.wikipedia.org/wiki/Maya_numerals) look kinda familiar now.

- "Decrypt" to numbers ```69 59 30 78 61 60 75```
- Convert HEX to a string

## Lvl 7

### Sources

- An image file ```DSWii6x```
- pastebin.com link
- hint -  0xBBA5

Contents of pastebin:
```
17:xeH
70:loC
0121:woR
AF:xeH
41:loC
9021:woR
11:xeH
51:loC
0021:woR
47:xeH
60:loC
1911:woR
```
### Solving the puzzle

- Reverse the text and get the offset
- Open an image in ```hexedit``` and navigate the locations specified
- Put the pieces together to get tinyurl.com/q3qkk4h

 ![Sick guy](https://tinyurl.com/q3qkk4h "Sick guy")

- Quick Google search suggests that the guy is [Rear Admiral Sir Francis Beaufort](https://en.wikipedia.org/wiki/Beaufort_cipher) who coincidentally also developed a cipher

- Go back to hex and go to 0xBBA5 offset from the hint. ```qlijfkqqxtgwqoyfsmly``` is a cipher text

- Use decoders and try brute forcing the cipher with guessing portions of plaintext (e.g 'flag', 'password')
