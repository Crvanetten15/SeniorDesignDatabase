# Infectious Disease DataSets

---

**_Disclaimer :_**
**All Information collected for this project is the property of the [CDC](https://www.cdc.gov/nndss/) or the [NewYorkTimes](https://github.com/nytimes/covid-19-data) and is being used for an educational and non-commercial project.**

**This data is in compliance with all licenses from original sources and must be followed if you plan to use our collection.**

---

### Purpose

For Team Scared to Compile at Cleveland State University we have chosen to make a web application regarding infectious diseases tracking and prediction. For this we needed to come up with alot of up to date records regarding a multitude of diseases. This is repository will act as a collection of data sorted by date and disease with as current of information that is available for us.

### How to use :

#### Install MySQL

To install MySQL we will also want to install MySQL Workbench so we can easily work with the database. I recommend watching this video from WebDevSimplified as it was exactly what I did.
[Click here to open video](https://www.youtube.com/watch?v=u96rVINbAUI)

#### Creating the DataBase

When installing your MySQL workbench you should get your login credentials, and a local instance on your host IP (127.0.0.1). Remember those as you will need to edit some python code to get this running locally. Open up your local instance and we will be creating a database on your local instance for us to put all our data in. Start a new query and proceed to make a databse. you can choose any name you like but feel free to copy my code below and run.

```MySQL
CREATE DATABASE SDDATA;
USE SDDATA;
```

Now our database is created and is ready to be used.

#### Setting up Python Code

I used two python packaged to make this parser, and I put them in a requirements.txt file for ease of use. If you have pip installed onto your device please go to your terminal, go to the project folder and run :

```bash
pip install -r requirements.txt
```

Doing this will install all needed libraries for the code.

Inside the main.py file, you will see at the bottom this section of code.

```python
s2Q.makeTable()


runMeasles()
runMalaria()
runMumps()
runPneumococcal()
runCSyphilis()
runTuberculosis()
```

Things to keep in mind for the future, each function will send all of the data for the stated disease individually to your database. Also, in the current state s2Q.makeTable() will only create the tables. Therefore if you run it again without commenting this out it will error.

Now for the actually changes needed. Inside of `sendtoSQL.py` i have a section of variables that I state your need to change. They are your login credentials and name of database for your local instance. Once this is done you should be good to run your code and make your database.

```python
    '''
    THIS IS THE DATA YOU NEED TO UPDATE
    '''
    user = 'root'
    passwrd = 'A PassWORD'
    database = 'DATABaSE'
    # configuration data for logging in
    config = {
        'user': f'{user}',
        'password': f'{passwrd}',
        'host': '127.0.0.1',
        'database': f'{database}',
        'raise_on_warnings': True
    }
```

#### Running the Code

The only file that your individually need to run is main.py.

`python main.py`

### Diseases and their sources

- Covid _[via NyTimes](https://github.com/nytimes/covid-19-data)_
- Measles _[via CDC](https://wonder.cdc.gov)_
- Malaria _[via CDC](https://wonder.cdc.gov)_
- Mumps _[via CDC](https://wonder.cdc.gov)_
- Pneumona _[via CDC](https://wonder.cdc.gov)_
- Syphilis _[via CDC](https://wonder.cdc.gov)_
- Tuberculosis _[via CDC](https://wonder.cdc.gov)_

### Contributors

For this direct repository of data collection, the scripts and CSV files have been configured by Connor Van Etten

### TDLR :

run this :
`pip install -r requirements.txt`
Make sure your database is empty
`create database SeniorDesign;`
use .env.example to enter your info on your database

```
USER=example
PASSWRD=example
DATABASE=example
HOST=example
```

Run with `python main.py`
It takes about 5 mins to fully build
