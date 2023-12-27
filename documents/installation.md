Installation instructions

## Sovelluksen testaaminen

Download the code from top right corner green Code button:(> Download zip). Extract the ZIP file and save in your computer. Add .env file to the root directory and copy the following text below as its content:

```bash
DATABASE_URL=<your local url>
SECRET_KEY=<any number series>
```

Open terminal and navigate to the app folder. 

Create virtual enviroment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Create database schema:

```bash
psql < schema.sql
```

Start the application:

```bash
flask run
```
