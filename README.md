Simple aiohttp test
===================
### Run project
```
$ git clone git@github.com:NelsonEAX/aiohttp.git aiotest
$ cd aiotest
$ mv .env.example .env
$ pip install -r requirements.txt
$ python3 app.py
```

### Project settings .env
##### Secret key for session
```
SECRET_KEY='kGVpDE_X9rNsyJfQTLKSK65FoXAZ7bJ3nfALpt6oCZs='
```
##### DataBase settings
```
PG_DATABASE = 'database'
PG_USERNAME = 'postgres'
PG_PASSWORD = 'postgres'
PG_SERVER = '127.0.0.1'
PG_PORT = 5432
```
##### DataBase seeding
To fill the database with test data, execute the script from the [file](https://github.com/NelsonEAX/aiohttp/blob/master/seed/backup.sql).


### Example result
Open in browser http://localhost:8080/