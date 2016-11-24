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