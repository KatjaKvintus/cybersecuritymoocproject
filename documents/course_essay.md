
# Cyber Security Project I essay


Link to the project:
https://github.com/KatjaKvintus/cybersecuritymoocproject 

Installation instructions: 
https://github.com/KatjaKvintus/cybersecuritymoocproject/blob/main/documents/installation.md 

OWASP Top list used in this project: 
OWASP Top 10, 2021: https://owasp.org/www-project-top-ten/



### FLAW 1: A03 Injection 

link to row: https://github.com/KatjaKvintus/cybersecuritymoocproject/blob/10cee4709ed0f6ada0688e73e2a75683adac8b45/users.py#L57 
(rows 57-65)

description of flaw: 
Injection [1] was the third most common risk in OWASP 2021 list. It makes the application vunerable to attack in several cases and in this essay I present one of them: “Dynamic queries or non-parameterized calls without context-aware escaping are used directly in the interpreter”.

In my code there is a flaw that allows to create a new admin level user without knowing the required code. When creating a new user, a malicuous hacker could add to the password fields the following text:

chooseanypassword', 'admin') --

Username can be anything and the user level you choose from the form is “user”. It will end up in an error message, because the app can register the new user in the text that was filled on the password field, but it does not crash the app and will create a new admin evel user. When you try to log in with with your new username and password ‘chooseanypassword’, you can log in and notice that this new user account is admin level account. 

how to fix it: 
User inputs should always be combined to the SQL command as parameters [10]. This applies to all functions that store data in the database. The correct code for this functions (that should be used instead of lines 57-65) is commented out in lines 68-78: https://github.com/KatjaKvintus/cybersecuritymoocproject/blob/10cee4709ed0f6ada0688e73e2a75683adac8b45/users.py#L68 



### FLAW 2: Vulnerable and Outdated Components 

link to row: https://github.com/KatjaKvintus/cybersecuritymoocproject/blob/fb33fefcfc00acbc9807467e1d1736f20ea1a871/requirements.txt#L2C12-L2C12 

description of flaw: 
This version on Flask (0.1) is very old and outdated. There are four known security flaws and one of them is a Arbitrary File Download [3]. This one is an issue only when using Windows operating system. A hostile hancker can use backslashes to escape the directory, and thus expose any files. 

how to fix it:  
The issue can be fixed by using the newst stable version of Flask. Run command “pip install --upgrade Flask” in terminal. At the momement (3.2.2024) it is 3.0.1. So the second row in the requirements.txt file should be as follows:
Flask== 3.0.1



## FLAW 3: Broken Access Control

link to rows:
https://github.com/KatjaKvintus/cybersecuritymoocproject/blob/350e5ea00088523055d09c1dc75ae495fcdaaf68/routes.py#L352
(Missing user level check in rows 352-355)

description of flaw:
“Broken access control” [4] is the most common flaw in OWASP 2021 list. It means that users of the application can use functions that their user level don’t allow, or access data their user level does not allow. Usually this means that regular users can access admin level functions, or visitors have more than read level rights. In my example the application lacks a check that controls access to admin tools, letting any signed in user use those.

The link above points out the flaw, a missing backend check, that checks the user level before granting entry to the admin tools. There is a script that tries to prevent user from accessing admin tools if they are not an admin, but a malicious hacker can disable the script in browser so the script does not actually protect the application.

If user level is not checked trustworthy, any user can access the admin section of the app and get access every admin tool,  and one of those is for creating new admin users. 

how to fix it: 
The fix in routes.py in lines 352-355 checks the user level from sessions, using the get_user_role() function from users.py, and if it is “user”, denies access to admin tools. 
https://github.com/KatjaKvintus/cybersecuritymoocproject/blob/350e5ea00088523055d09c1dc75ae495fcdaaf68/routes.py#L352

https://github.com/KatjaKvintus/cybersecuritymoocproject/blob/f4a92107864996d1e8f1d2cb85f47801a955ac12/users.py#L116 


### FLAW 4: Security Misconfiguration 

link to row:
https://github.com/KatjaKvintus/cybersecuritymoocproject/blob/8d4ad5db4d432153c8a36498ae3caffbdc175111/schema.sql#L96 

description of flaw: 
‘Security misconfiguration’ [5] is a comman flaw that makes an application vunerable to malicious users. It can appear many ways and one way is to have a built-in default admin user credentials that no-one can change. In this case the database schema includes one row that creates admin user with username “admin” and password “admin” that are very easy to guess as they are sadly common [6].

how to fix it: 
Remove the linked row that creates a default admin user account.



### FLAW 5: Cryptographic Failures 

link to row:
https://github.com/KatjaKvintus/cybersecuritymoocproject/blob/d2861f06e9016eb8c1203c80bdabfce45d8ca56d/users.py#L52 

description of flaw:
Cryptographic failure is the second most common flaw in OWASP 2021 list. It means that sensitive data is not protected with cryptography [7]. In this case all users passwords are stored in the database as they are, not crypted in any way. 

how to fix it: 
There is a ready library that provides excellent tools for this. Verkzeung [8], a comprehensive WSGI web application library, has a ‘generate_password_hash()’ function [9] that stores passwords securely as a hash value. To fix the issue in this application you have to import the security tools and use functions ‘generate_password_hash()’ when creating a new user account and ‘check_password_hash()’ function when checking the signed in users pasword validity.

https://github.com/KatjaKvintus/cybersecuritymoocproject/blob/926a199b2ccb3245ed47c4f5ba7edeac54167129/users.py#L4 (add import)

https://github.com/KatjaKvintus/cybersecuritymoocproject/blob/926a199b2ccb3245ed47c4f5ba7edeac54167129/users.py#L33 (replace line 34 with this)

https://github.com/KatjaKvintus/cybersecuritymoocproject/blob/d2861f06e9016eb8c1203c80bdabfce45d8ca56d/users.py#L61 (replace the ‘create_new_account’ function contents with lines 61-74)

All changes for flaw 5 are done in users.py file. 


### References:


[1] https://owasp.org/Top10/A03_2021-Injection/  

[2] Wikipedia: SQL injection https://en.wikipedia.org/wiki/SQL_injection 

[3] https://security.snyk.io/package/pip/flask/0.1 

[4] https://owasp.org/Top10/A01_2021-Broken_Access_Control/ 

[5] https://owasp.org/Top10/A05_2021-Security_Misconfiguration/ 

[6] https://en.wikipedia.org/wiki/List_of_the_most_common_passwords 

[7] https://owasp.org/Top10/A02_2021-Cryptographic_Failures/ 

[8] https://werkzeug.palletsprojects.com/en/ 

[9] https://werkzeug.palletsprojects.com/en/2.3.x/utils/#werkzeug.security.generate_password_hash 

[10] https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html 
