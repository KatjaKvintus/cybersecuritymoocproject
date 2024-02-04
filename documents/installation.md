
## Instructions for testing

_**Note: these instructions are for a Linux computer (Ubuntu OS).**_


### Downloading the applicating files from GitHub

Download the code from top right corner green Code button:(> Download zip). Extract the ZIP file and save in your computer. 

Add .env file to the root directory and copy the following text below as its content:

```bash
DATABASE_URL="postgresql:///oatmealdb"
SECRET_KEY=<any number series>
```

### PostgeSQL

If you dont have PostreSQL installed, installit it by following these instructions:
https://www.postgresql.org/download/ 

Or follow instructions from this video (in Finnish):
https://www.helsinki.fi/fi/unitube/video/617d690b-b1ce-44f0-997a-dca01bf7eff0


### Creating the database

Open terminal and navigate to the app folder. Create database:

```bash
pg_ctl start
psql
CREATE DATABASE oatmealdb;
\c oatmealdb
```

Create the database schema by copying the contenst of the schema.sql file into terminal.

Open another tab in terminal and create a virtual enviroment:

```bash
python3 -m venv venv
source venv/bin/activate
```

### Start testing

Start the application:

```bash
flask run
```

Copy the web address from row starting "* Running on..." ja paste it into a browser address bar.

If you want to create a new admin user, you need an admin key. You will find it users.py file line 10:

https://github.com/KatjaKvintus/cybersecuritymoocproject/blob/main/users.py
