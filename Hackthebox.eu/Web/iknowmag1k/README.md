# iknowmag1k

## Register and authenticate
Register using the form, log in with the credentials used.

After authentication the server generates iknowmag1k value, so cookies end up looking like this:
```
Cookie:
PHPSESSID=bqha27mii******************;
iknowmag1k=DsxnEMX0OZ4NZ13RAEkzjgxVIGdB8Y6i%2BpibchwP8GjWkSjs97upxQ%3D%3D
```

This cookie is url-encoded base64 string, however it does not convert to ASCII, therefore must be encoded/encrypted
```
DsxnEMX0OZ4NZ13RAEkzjgxVIGdB8Y6i+pibchwP8GjWkSjs97upxQ==
```
## Doing some mag1k
Changing this value leads to a couple of possible outcomes:
- code 200 -'valid' encoding
- code 500 - 'invalid' encoding

The string is likely encrypted with CBC and susceptible to padding oracle attack because of the ability to toss a ciphertext to the server (oracle) and get a response (200/500) whether this ciphertext (padding) is valid.

### Running [padbuster](https://github.com/GDSSecurity/PadBuster):
```
perl padBuster.pl http://*ip*:*port*/profile.php DsxnEMX0OZ4NZ13RAEkzjgxVIGdB8Y6i%2BpibchwP8GjWkSjs97upxQ%3D%3D 8 --cookies "PHPSESSID=bqha27mi************; iknowmag1k=DsxnEMX0OZ4NZ13RAEkzjgxVIGdB8Y6i%2BpibchwP8GjWkSjs97upxQ%3D%3D" --encoding 0 --verbose

```

Result:	(HEX)  : 7B2275736572223A22757365726E616D65222C22726F6C65223A2275736572227D0F0F0F0F0F0F0F0F0F0F0F0F0F0F0F
	(ASCII): {"user":"username","role":"user"}

Simply changing the role to ‘admin’ should do the trick. Getting an encrypted value:
```
perl padBuster.pl http://*ip*:*port*/profile.php DsxnEMX0OZ4NZ13RAEkzjgxVIGdB8Y6i%2BpibchwP8GjWkSjs97upxQ%3D%3D 8 --cookies "PHPSESSID=bqha27mi***********; iknowmag1k=DsxnEMX0OZ4NZ13RAEkzjgxVIGdB8Y6i%2BpibchwP8GjWkSjs97upxQ%3D%3D" --encoding 0 --verbose -plaintext "{\"user\”:\”username\”,\”role\":\"admin\"}"
```
Replacing the original cookie with an encrypted value from padbuster gets admin’s page with a flag!
 :tada:  
