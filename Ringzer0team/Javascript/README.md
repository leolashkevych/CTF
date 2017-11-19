# Javascript

## Client side validation is bad!

```js
// Look's like weak JavaScript auth script :)
$(".c_submit").click(function(event) {
	event.preventDefault()
	var u = $("#cuser").val();
	var p = $("#cpass").val();
	if(u == "admin" && p == String.fromCharCode(74,97,118,97,83,99,114,105,112,116,73,115,83,101,99,117,114,101)) {
	    if(document.location.href.indexOf("?p=") == -1) {   
	        document.location = document.location.href + "?p=" + p;
	    }
	} else {
	    $("#cresponse").html("<div class='alert alert-danger'>Wrong password sorry.</div>");
	}
});
```

```js
>console.log(String.fromCharCode(74,97,118,97,83,99,114,105,112,116,73,115,83,101,99,117,114,101))
[Log] JavaScriptIsSecure
```
##	Hashing is more secure
```js
// Look's like weak JavaScript auth script :)
$(".c_submit").click(function(event) {
	event.preventDefault();
	var p = $("#cpass").val();
	if(Sha1.hash(p) == "b89356ff6151527e89c4f3e3d30c8e6586c63962") {
	    if(document.location.href.indexOf("?p=") == -1) {   
	        document.location = document.location.href + "?p=" + p;
	    }
	} else {
	    $("#cresponse").html("<div class='alert alert-danger'>Wrong password sorry.</div>");
	}
});
```
[Crackstation](https://crackstation.net) wordlist decodes the hash to "adminz"

## Then obfuscation is more secure
```js
// Look's like weak JavaScript auth script :)
var _0xc360=["\x76\x61\x6C","\x23\x63\x70\x61\x73\x73","\x61\x6C\x6B\x33","\x30\x32\x6C\x31","\x3F\x70\x3D","\x69\x6E\x64\x65\x78\x4F\x66","\x68\x72\x65\x66","\x6C\x6F\x63\x61\x74\x69\x6F\x6E","\x3C\x64\x69\x76\x20\x63\x6C\x61\x73\x73\x3D\x27\x65\x72\x72\x6F\x72\x27\x3E\x57\x72\x6F\x6E\x67\x20\x70\x61\x73\x73\x77\x6F\x72\x64\x20\x73\x6F\x72\x72\x79\x2E\x3C\x2F\x64\x69\x76\x3E","\x68\x74\x6D\x6C","\x23\x63\x72\x65\x73\x70\x6F\x6E\x73\x65","\x63\x6C\x69\x63\x6B","\x2E\x63\x5F\x73\x75\x62\x6D\x69\x74"];$(_0xc360[12])[_0xc360[11]](function (){var _0xf382x1=$(_0xc360[1])[_0xc360[0]]();var _0xf382x2=_0xc360[2];if(_0xf382x1==_0xc360[3]+_0xf382x2){if(document[_0xc360[7]][_0xc360[6]][_0xc360[5]](_0xc360[4])==-1){document[_0xc360[7]]=document[_0xc360[7]][_0xc360[6]]+_0xc360[4]+_0xf382x1;} ;} else {$(_0xc360[10])[_0xc360[9]](_0xc360[8]);} ;} );
```

Deobfuscate this script with [here](https://puzzlefiles.com/Deobfuscate/) to get this:

```js
$('.c_submit')['click'](function () {
    var _0xf382x1 = $('#cpass')['val']();
    var _0xf382x2 = 'alk3';
    if (_0xf382x1 == '02l1' + _0xf382x2) {
        if (document['location']['href']['indexOf']('?p=') == -1) {
            document['location'] = document['location']['href'] + '?p=' + _0xf382x1;
        };
    } else {
        $('#cresponse')['html']('<div class=\'error\'>Wrong password sorry.</div>');
    };
});
```
The password would be ``02l1alk3``.
## Why not?
```js
// Look's like weak JavaScript auth script :)
$(".c_submit").click(function(event) {
	event.preventDefault();
	var k = new Array(176,214,205,246,264,255,227,237,242,244,265,270,283);
	var u = $("#cuser").val();
	var p = $("#cpass").val();
	var t = true;

	if(u == "administrator") {
		for(i = 0; i < u.length; i++) {
			if((u.charCodeAt(i) + p.charCodeAt(i) + i * 10) != k[i]) {
				$("#cresponse").html("<div class='alert alert-danger'>Wrong password sorry.</div>");
				t = false;
				break;
			}
		}
	} else {
		$("#cresponse").html("<div class='alert alert-danger'>Wrong password sorry.</div>");
		t = false;
	}
	if(t) {
		if(document.location.href.indexOf("?p=") == -1) {
			document.location = document.location.href + "?p=" + p;
         			}
	}
});
```
Use the script below to decode the password.
```python
u = "administrator"
i = 0
k = [176,214,205,246,264,255,227,237,242,244,265,270,283]
pw = ""

for letter in u:
	charcode = ord(letter)
	print (k[iterator] - (charcode + i * 10))
	passw += chr(k[i] - (charcode + i * 10))
	i++

print pw
```
The result is ``OhLord4309111``

## Valid key required
```js
function curry( orig_func ) {
	var ap = Array.prototype, args = arguments;

	function fn() {
	ap.push.apply( fn.args, arguments );
	return fn.args.length < orig_func.length ? fn : orig_func.apply( this, fn.args );
	}

	return function() {
	fn.args = ap.slice.call( args, 1 );
	return fn.apply( this, arguments );
	};
}

function callback(x,y,i,a) {
  return !y.call(x, a[a["length"]-1-i].toString().slice(19,21)) ? x : {};
}

var ref = {T : "BG8",J : "jep",j : "M2L",K : "L23",H : "r1A"};

function validatekey()
{
	e = false;
	var _strKey = "";
    try {
		_strKey = document.getElementById("key").value;
        var a = _strKey.split("-");
        if(a.length !== 5)
        	e = true;

        var o=a.map(genFunc).reduceRight(callback, new (genFunc(a[4]))(Function));

        if(!equal(o,ref))
			e = true;

    }catch(e){
    	e = true;
    }

    if(!e) {
    	if(document.location.href.indexOf("?p=") == -1) {
			document.location = document.location.href + "?p=" + _strKey;
       		}
    } else {
    	$("#cresponse").html("<div class='alert alert-danger'>Wrong password sorry.</div>");
	}   
}

function equal(o,o1)
{
    var keys1 = Object.keys(o1);
    var keys = Object.keys(o);
    if(keys1.length != keys.length)
        return false;

    for(var i=0;i<keys.length;i++)
         if(keys[i] != keys1[i] || o[keys[i]] != o1[keys1[i]])
            return false;

    return true;

}

function hook(f1,f2,f3) {
    return function(x) { return f2(f1(x),f3(x));};
}

var h = curry(hook);
var fn = h(function(x) {return x >= 48;},new Function("a","b","return a && b;"));
function genFunc(_part) {
    if(!_part || !(_part.length) || _part.length !== 4)
        return function() {};

    return new Function(_part.substring(1,3), "this." + _part[3] + "=" + _part.slice(1,3) + "+" + (fn(function(y){return y<=57})(_part.charCodeAt(0)) ?  _part[0] : "'"+ _part[0] + "'"));
}
```

So...

- The code has to be split up in 5 elements
- Each element consist of 4 characters
- Elements will be passed through functions and compared to ``ref`` array
- If arrays match, validation is passed

Lets try running a magic function with ``abcd-efgh-ijkl-mnop-wxyz`` and see what happens.

```js
> var a = ['abcd','efgh','ijkl','mnop','wxyz'];
a.map(genFunc).reduceRight(callback, new(genFunc(a[4]))(Function));
< anonymous = $5

d: "xya"

h: "noe"

l: "jki"

p: "fgm"

z: "bcw"
```

From this output, we can see how the elements are parsed into the array, for example:

- First letter of the element becomes the last one
- The last letter of an element becomes the key
- etc

Now all that is left to do is to substitute the initial array with elements from ref (``{T : "BG8",J : "jep",j : "M2L",K : "L23",H : "r1A"}``) using a correct positioning:

```js
> var a = ["ABGH", "3jeK", "LM2j", "pL2J","8r1T"];
a.map(genFunc).reduceRight(callback, new(genFunc(a[4]))(Function));
< anonymous {T: "BG8", J: "jep", j: "M2L", K: "L23", H: "r1A"}
```

## Most Secure Crypto Algo
```javascript
$(".c_submit").click(function(event) {
  event.preventDefault();
  var k = CryptoJS.SHA256("\x93\x39\x02\x49\x83\x02\x82\xf3\x23\xf8\xd3\x13\x37");
  var u = $("#cuser").val();
  var p = $("#cpass").val();
  var t = true;

  if(u == "\x68\x34\x78\x30\x72") {
    if(!CryptoJS.AES.encrypt(p, CryptoJS.enc.Hex.parse(k.toString().substring(0,32)), { iv: CryptoJS.enc.Hex.parse(k.toString().substring(32,64)) }) == "ob1xQz5ms9hRkPTx+ZHbVg==") {
      t = false;
    }
  } else {
    $("#cresponse").html("<div class='alert alert-danger'>Wrong password sorry.</div>");
    t = false;
  }
  if(t) {
    if(document.location.href.indexOf("?p=") == -1) {
      document.location = document.location.href + "?p=" + p;
              }
  }
});
```
Decode the user value

```js
> var u = "\x68\x34\x78\x30\x72"; console.log(u)
[Log] h4x0r
```
Decrypt using CryptoJS
```js
> var k = CryptoJS.SHA256("\x93\x39\x02\x49\x83\x02\x82\xf3\x23\xf8\xd3\x13\x37");
var key = CryptoJS.enc.Hex.parse(k.toString().substring(0,32));
var iv = CryptoJS.enc.Hex.parse(k.toString().substring(32,64));
var encrypted = "ob1xQz5ms9hRkPTx+ZHbVg==";
pass = '' + CryptoJS.AES.decrypt(encrypted, key, {iv: iv})
console.log(pass);
[Log] 50617373573052442132383925212a
```
``50617373573052442132383925212a`` converts to ASCII as ``PassW0RD!289%!*``
