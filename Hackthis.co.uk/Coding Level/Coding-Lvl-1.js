var answer = document.getElementsByName("answer")[0].innerHTML;
answer = document.getElementsByTagName("fieldset")[0].getElementsByTagName("textarea")[0].innerHTML.split(", ").sort().join(", ");
