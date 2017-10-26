# JS Levels

## Lvl 1

There is a script in the source code which compares the value to a variable called 'correct'
```javascript
<script type='text/javascript'> $(function(){ $('.level-form').submit(function(e){ e.preventDefault(); if(document.getElementById('pass').value == correct) { document.location = '?pass=' + correct; } else { alert('Incorrect password') } })})</script>
```
Open a console and enter ```console.log(correct)
// returns 'selurj'```

## Lvl 2

Find a script in the source code
``` javascript
<script type='text/javascript'>
                var length = 5;
                var x = 3;
                var y = 2;
                y = Math.sin(118.13);
                y = -y;
                x = Math.ceil(y);
                y++;
                y = y+x+x;
                y *= (y/2);
                y++;
                y++;
                length = Math.floor(y);
</script>
```
Output 'length' variable from the console (or just do the math :pencil2:).
## Lvl 3
The code for the submit button is
```javascript
<script type='text/javascript'> var thecode = 'code123'; $(function(){ $('.level-form').submit(function(e){ e.preventDefault(); if ($('.level-form #pass')[0].value == thecode) { document.location = "?pass=" + thecode; } else { alert('Incorrect Password'); } }); }); </script>
```
Output 'thecode' which returnes 'getinhere'

## Lvl 4
Find the sorce code -
```view-source: https://www.hackthis.co.uk/levels/javascript/4?output```

Search for the level form.
```html
<div class='center'>The password is: smellthecheese</div>
```
## Lvl 5
Go to console and search for keys of your window.
```
Object.keys( window );
```
The output is
```
["top", "window", "location", "external", "chrome", "document", "NREUM", "__nr_require", "$", "jQuery", "io", "html5", "Modernizr", "yepnope", "_gs", "timeSince", "timeString", "PopupCenter", "createCookie", "FavCounter", "loggedIn", "thecode", "_idl", "timer_start", "hljs", "socket", "favcounter", "counter_chat", "counter_notifications", "searchsuggest", "set", "a", "b", "c", "d", "p", "__commandLineAPI"]
```
Find variables a, b, c and d. Output them.

Output of ```alert(d)``` is cool.
