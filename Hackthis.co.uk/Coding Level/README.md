# Coding Level
Run the scripts in JS console.
## Lvl 1
```javascript
var answer = document.getElementsByName("answer")[0].innerHTML;
answer = document.getElementsByTagName("fieldset")[0].getElementsByTagName("textarea")[0].innerHTML.split(", ").sort().join(", ");
```
## Lvl 2
```javascript
var str1 = document.getElementsByTagName("textarea")[0].value +'';
var words = str1.split(" ");
for(i=0; i < words.length;i++){
	var chars = words[i].split(",");
	for (j=0; j < chars.length; j++ ){
		if(chars[j]==0){
			chars[j] = ''
		}else{
		chars[j] = String.fromCharCode(126 - chars[j]);
		}
	}
	words[i] = chars.join("");
}
var str2 = words.join(" ");
document.getElementsByName("answer")[0].innerHTML = str2.toLowerCase();
```
