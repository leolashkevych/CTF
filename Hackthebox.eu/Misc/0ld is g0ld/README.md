# 0ld is g0ld

## Determine PDF VERSION

```
hexdump 0ld\ is\ g0ld.pdf -C
00000000  25 50 44 46 2d 31 2e 36  0d 0a 25 b5 b5 b5 b5 0d  |%PDF-1.6..%.....|
00000010  0a 31 20 30 20 6f 62 6a  0d 0a 3c 3c 2f 54 79 70  |.1 0 obj..<</Typ|
00000020  65 2f 43 61 74 61 6c 6f  67 2f 50 61 67 65 73 20  |e/Catalog/Pages |
00000030  32 20 30 20 52 2f 4c 61  6e 67 28 91 ab 01 02 20  |2 0 R/Lang(.... |
00000040  d2 4b 24 fc bc 53 fe dc  13 a7 34 41 98 c9 c7 f4  |.K$..S....4A....|
00000050  cb 5a 7b f9 2a 2e c6 23  de c5 e0 29 20 2f 53 74  |.Z{.*..#...) /St|
00000060  72 75 63 74 54 72 65 65  52 6f 6f 74 20 31 31 20  |ructTreeRoot 11 |
```

PDF-1.6

## Get the hash
```
./pdf2john.pl /root/Desktop/0ld\ is\ g0ld.pdf > pdfhash.txt
```
## Crack the hash
```
hashcat -a 0 -m 10500 Downloads/pdfhash.txt hashcat/rockyou.txt
hashcat (v3.20-18-g2039e2c) starting...
```

- a 0    : *wordlist attack type*
- m 10500: *PDF 1.4 - 1.6 (Acrobat 5 - 8) mode*

```
$pdf$4*4*128*-1060*1*16*5c8f37d2a45eb64e9dbbf71ca3e86861*32*9cba5cfb1c536f1384bba7458aae3f8100000000000000000000000000000000*32*702cc7ced92b595274b7918dcb6dc74bedef6ef851b4b4b5b8c88732ba4dac0c:jumanji69

Session..........: hashcat
Status...........: Cracked
Hash.Type........: PDF 1.4 - 1.6 (Acrobat 5 - 8)
...
```
## Open the PDF

The pdf contains a lovely picture of Samuel Morse with morse code encoded flag
