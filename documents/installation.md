
## Instructions for testing

Download the code from top right corner green Code button:(> Download zip). Extract the ZIP file and save in your computer. Add .env file to the root directory and copy the following text below as its content:

```bash
DATABASE_URL="postgresql:///oatmealdb"
SECRET_KEY=<any number series>
```


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

Start the application:

```bash
flask run
```

Copy the web address from row starting "* Running on..." ja paste it into a browser address bar.

If you want to create a new admin user, you need an admin key. You will find it users.py file:
https://github.com/KatjaKvintus/cybersecuritymoocproject/blob/5cff06c0035bb7e529c65a756b148c3bef14b80b/users.py#L10
