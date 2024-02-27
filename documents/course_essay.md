
# Cyber Security Project I essay

Link to the project: 
https://github.com/KatjaKvintus/cybersecuritymoocproject 
 
Installation instructions:  
https://github.com/KatjaKvintus/cybersecuritymoocproject/blob/main/documents/installation.md 

OWASP Top list used in this project:  
OWASP Top 10, 2021: https://owasp.org/www-project-top-ten/ 
  

### FLAW 1: A03 Injection  

link to row:  
https://github.com/KatjaKvintus/cybersecuritymoocproject/blob/0abb20e07289129b4b61662be90be0370673f366/users.py#L50  

https://github.com/KatjaKvintus/cybersecuritymoocproject/blob/0abb20e07289129b4b61662be90be0370673f366/users.py#L86  

description of flaw:  
Injection [1] was the third most common risk in OWASP 2021 list. It makes the application vunerable to attack in several cases and in this essay, I present one of them: “Dynamic queries or non-parameterized calls without context-aware escaping are used directly in the interpreter”. 

In my code there is a flaw that allows to create a new admin level user without knowing the required code. When creating a new user, a malicious hacker could add to the password fields the following text: 

chooseanypassword', 'admin') -- 

Username can be anything and the user level you choose from the form is “user”. It will end up in an error message, because the app can register the new user in the text that was filled in on the password field, but it does not crash the app and will create a new admin evel user. When you try to log in with with your new username and password ‘chooseanypassword’, you can log in and notice that this new user account is an admin level account.  

how to fix it:  
User inputs should always be combined to the SQL command as parameters [10]. This applies to all functions that store data in the database.  

https://github.com/KatjaKvintus/cybersecuritymoocproject/blob/0abb20e07289129b4b61662be90be0370673f366/users.py#L62  

https://github.com/KatjaKvintus/cybersecuritymoocproject/blob/0abb20e07289129b4b61662be90be0370673f366/users.py#L98  

 
### FLAW 2: Vulnerable and Outdated Components  

link to row: https://github.com/KatjaKvintus/cybersecuritymoocproject/blob/bb8f6217a76a91f5c86c4f239c7dabb1ed87400c/requirements.txt#L2  

description of flaw:  
This version on Flask (0.1) is very old and outdated. There are four known security flaws and one of them is a Arbitrary File Download [3]. This one is an issue only when using Windows operating system. A hostile hacker can use backslashes to escape the directory, and thus expose any files.  

how to fix it:   
The issue can be fixed by using the newest stable version of Flask. Run command “pip install --upgrade Flask” in terminal. At the moment (3.2.2024) it is 3.0.1. So, the second row in the requirements.txt file should be as follows: 
Flask== 3.0.1 

  
### FLAW 3: Broken Access Control 

link to rows: 
(Missing checks) 

https://github.com/KatjaKvintus/cybersecuritymoocproject/blob/06567acbb10a80e8fc221eb42713c14c3e024eda/routes.py#L361  

https://github.com/KatjaKvintus/cybersecuritymoocproject/blob/06567acbb10a80e8fc221eb42713c14c3e024eda/routes.py#L380 

https://github.com/KatjaKvintus/cybersecuritymoocproject/blob/06567acbb10a80e8fc221eb42713c14c3e024eda/routes.py#L399  

description of flaw: 
“Broken access control” [4] is the most common flaw in OWASP 2021 list. It means that users of the application can use functions that their user level doesn’t allow, or access data their user level does not allow. Usually this means that regular users can access admin level functions, or visitors have more than read level rights. In my example the application lacks a check that controls access to admin tools, letting any signed in user use those. 

The links above point out the flaw, three missing backend checks, that check the user level before granting entry to the admin tools page or using the admin tools functionalities. (There is also a script in templates/mainpage.html that tries to prevent user from accessing admin tools if they are not an admin, but a malicious hacker can disable the script in browser, so the script does not actually protect the application.) 

If the user level is not checked trustworthy, any user can access the admin section of the app and get access to every admin tool, and one of those is for creating new admin users.  

how to fix it:  

Uncomment the check_if_loggend_in_user_is_admin() method in users.py: 

https://github.com/KatjaKvintus/cybersecuritymoocproject/blob/06567acbb10a80e8fc221eb42713c14c3e024eda/users.py#L174  

 Uncomment the user level checks in three places: 

https://github.com/KatjaKvintus/cybersecuritymoocproject/blob/06567acbb10a80e8fc221eb42713c14c3e024eda/routes.py#L361  

https://github.com/KatjaKvintus/cybersecuritymoocproject/blob/06567acbb10a80e8fc221eb42713c14c3e024eda/routes.py#L380 

https://github.com/KatjaKvintus/cybersecuritymoocproject/blob/06567acbb10a80e8fc221eb42713c14c3e024eda/routes.py#L399  


### FLAW 4: Security Misconfiguration  

link to row: 
https://github.com/KatjaKvintus/cybersecuritymoocproject/blob/06567acbb10a80e8fc221eb42713c14c3e024eda/schema.sql#L96  

description of flaw:  

‘Security misconfiguration’ [5] is a comman flaw that makes an application vunerable to malicious users. It can appear in many ways and one way is to have a built-in default admin user credentials that no-one can change. In this case the database schema includes one row that creates an admin user with username “admin” and password “admin” that are very easy to guess as they are sadly common [6]. 

how to fix it:  
Remove the linked row that creates a default admin user account. 


### FLAW 5: Cryptographic Failures  

link to row: 
https://github.com/KatjaKvintus/cybersecuritymoocproject/blob/06567acbb10a80e8fc221eb42713c14c3e024eda/users.py#L52  

description of flaw: 
Cryptographic failure is the second most common flaw in OWASP 2021 list. It means that sensitive data is not protected with cryptography [7]. In this case all users' passwords are stored in the database as they are, not crypted in any way.  

 how to fix it:  
There is a ready library that provides excellent tools for this. Verkzeung [8], a comprehensive WSGI web application library, has a ‘generate_password_hash()’ function [9] that stores passwords securely as a hash value. To fix the issue in this application you have to import the security tools and use functions ‘generate_password_hash()’ when creating a new user account and ‘check_password_hash()’ function when checking the signed in users pasword validity. 

 https://github.com/KatjaKvintus/cybersecuritymoocproject/blob/06567acbb10a80e8fc221eb42713c14c3e024eda/users.py#L4 (add import) 

 https://github.com/KatjaKvintus/cybersecuritymoocproject/blob/06567acbb10a80e8fc221eb42713c14c3e024eda/users.py#L33 (replace line 34 with this) 

 https://github.com/KatjaKvintus/cybersecuritymoocproject/blob/0abb20e07289129b4b61662be90be0370673f366/users.py#L96  

 https://github.com/KatjaKvintus/cybersecuritymoocproject/blob/0abb20e07289129b4b61662be90be0370673f366/users.py#L61 (replace the ‘create_new_account’ function contents with lines 61-74) 

 
### FLAW 6: Security Misconfiguration   

Flaw:  
https://github.com/KatjaKvintus/cybersecuritymoocproject/blob/main/.env  (the whole file)  

Fix:  
https://github.com/KatjaKvintus/cybersecuritymoocproject/blob/main/documents/installation.md  
(“Creating the database” section, the part about .env file)  

 An application could have several different kinds of security misconfiguration flaws [11]. One of them happens when a password or other sensitive data would be visible in a product [12]. This might compromise the system and give a malicious attacker a chance to gain access to sensitive information like passwords, credit card data or anything GDPR might cover.  

 In database web apps it is adviced that the Github project does not include .env file, that contains the database SECRET_KEY. Instead, the user is instructed to create one after cloning the project.   

How to fix it:  
Remove the .env file from Github project. Add a section to installation instructions to create an own .env file and write there an entire new made-up SECRET_KEY that is harder to guess than "123456".  

 
References: 

[1] https://owasp.org/Top10/A03_2021-Injection/   
[2] https://en.wikipedia.org/wiki/SQL_injection  
[3] https://security.snyk.io/package/pip/flask/0.1  
[4] https://owasp.org/Top10/A01_2021-Broken_Access_Control/  
[5] https://owasp.org/Top10/A05_2021-Security_Misconfiguration/  
[6] https://en.wikipedia.org/wiki/List_of_the_most_common_passwords  
[7] https://owasp.org/Top10/A02_2021-Cryptographic_Failures/  
[8] https://werkzeug.palletsprojects.com/en/  
[9] https://werkzeug.palletsprojects.com/en/2.3.x/utils/#werkzeug.security.generate_password_hash  
[10] https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html  
[11] https://owasp.org/Top10/A05_2021-Security_Misconfiguration/  
[12] https://cwe.mitre.org/data/definitions/260.html 
