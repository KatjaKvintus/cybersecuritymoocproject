
# Cyber Security Project I essay
(in progress)

Link to the project:
https://github.com/KatjaKvintus/cybersecuritymoocproject 

Installation instructions: 
https://github.com/KatjaKvintus/cybersecuritymoocproject/blob/main/documents/installation.md 

OWASP Top list used in this project: 
OWASP Top 10 2021: https://owasp.org/www-project-top-ten/



## FLAW 1: A03 Injection 

link to row: https://github.com/KatjaKvintus/cybersecuritymoocproject/blob/10cee4709ed0f6ada0688e73e2a75683adac8b45/users.py#L57 
(rows 57-65)

description of flaw: 
A03:202 Injection was the third most common risk in OWASP 2021 list [1]. It makes the application vunerable to attack in several cases and in this essay I present one of them: “Dynamic queries or non-parameterized calls without context-aware escaping are used directly in the interpreter”.

In my code there is a flaw that allows to create a new admin level user without knowing the required code. When creating a new user, a malicuous hacker could add to the password fields the following text:

chooseanypassword', 'admin') --

Username can be anything and the user level you choose from the form is “user”. It will end up in an error message, because the app can register the new user in the text that was filled on the password field, but it does not crash the add and will create a new admin evel user. When you try to log in with with your new username and password chooseanypassword, you can log in and notice that this new user account is admin level account. 

how to fix it: 
User inputs should always be combined to the SQL command as parameters. The correct code is commented out in lines 68-78: https://github.com/KatjaKvintus/cybersecuritymoocproject/blob/10cee4709ed0f6ada0688e73e2a75683adac8b45/users.py#L68 

Also password should be better sealed, for example turned as a hash value:
https://github.com/KatjaKvintus/cybersecuritymoocproject/blob/10cee4709ed0f6ada0688e73e2a75683adac8b45/users.py#L4
https://github.com/KatjaKvintus/cybersecuritymoocproject/blob/10cee4709ed0f6ada0688e73e2a75683adac8b45/users.py#L32 
https://github.com/KatjaKvintus/cybersecuritymoocproject/blob/10cee4709ed0f6ada0688e73e2a75683adac8b45/users.py#L54C3-L54C3 


## FLAW 2: Vulnerable and Outdated Components 
link to row: https://github.com/KatjaKvintus/cybersecuritymoocproject/blob/fb33fefcfc00acbc9807467e1d1736f20ea1a871/requirements.txt#L2C12-L2C12 

description of flaw: 
This version on Flask (0.1) is very old and outdated. There are four known security flaws and one of them is a Arbitrary File Download [3]. This one is an issue only when using Windows operating system. A hostile hancker can use backslashes to escape the directory, and thus expose files. 

how to fix it:  
The issue can be fixed by using the newst stable version of Flask. Run command “pip install --upgrade Flask” in terminal. Ath the momement (27.12.2023) it is 2.2.2. So the row in the requirements.txt should be:
Flask==2.2.2


## FLAW 3: Broken Access Control

link to row:
https://github.com/KatjaKvintus/cybersecuritymoocproject/blob/82eb38aa08e8d80b56862d2ace80af10ae31c84a/templates/mainpage.html#L42 

description of flaw:
“Broken access control” is a very common flaw [4]. It means that users of the application can use functions that their user level don’t allow, or access data their user level does not allow. In my example the application lacks a script that controls access to admin tools.

The link points out a missing script that checks the user’s user level. Without it any user can access admin section of the app and get access for creating new admin users. 

how to fix it: 
Rows 42-52 will fix the issue by adding a script that checks the logged in users user level and prevents access if not admin level user. 



## FLAW 4:

link to row:


description of flaw:


how to fix it: 




## FLAW 5:

link to row:


description of flaw:


how to fix it: 




## FLAW 6:

link to row:


description of flaw:


how to fix it: 



References:

[1] https://owasp.org/Top10/A03_2021-Injection/ 
[2] Wikipedia: SQL injection https://en.wikipedia.org/wiki/SQL_injection 
[3] https://security.snyk.io/package/pip/flask/0.1 
[4] https://owasp.org/Top10/A01_2021-Broken_Access_Control/ 

