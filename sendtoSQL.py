import mysql.connector

from decouple import config

'''
Passing data into my MySQL Database
'''
user = config('USER')
passwrd = config('PASSWRD')
database = config('DATABASE')
host = config('HOST')


def send(data, date, name):
    '''
    THIS IS THE DATA YOU NEED TO UPDATE
    '''
    # configuration data for logging in
    config = {
        'user': f'{user}',
        'password': f'{passwrd}',
        'host': f'{host}',
        'database': f'{database}',
        'raise_on_warnings': False
    }

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    for _ in data:
        sql = \
            """
        INSERT INTO weekly_data (disease_name, year, week, disease_cases, disease_deaths, state) VALUES
            (%s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE disease_cases = disease_cases, disease_deaths = disease_deaths; 
        """
        if type(_[1]) != int:
            _[1] = _[1].replace(',', '')
        year, week = map(int, date.split('-'))
        if _[1] == 'NC' or _[1] == 'U' or _[1] == 'N':
            _[1] = 0
        val = (name, year, week, int(_[1]), 0, _[0])
        cursor.execute(sql, val)
        cnx.commit()

    print(f"{name} : {date} inserted. ")


def makeTable():
    # configuration data for logging in
    config = {
        'user': f'{user}',
        'password': f'{passwrd}',
        'host': f'{host}',
        'database': f'{database}',
        'raise_on_warnings': False
    }

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    # cursor.execute('DROP TABLE wondertables')
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS weekly_data (
            disease_name VARCHAR(50) NOT NULL,
            year INT NOT NULL,
            week INT NOT NULL,
            disease_cases INT NOT NULL,
            disease_deaths INT NOT NULL,
            state VARCHAR(50) NOT NULL,
            PRIMARY KEY (disease_name, year, week, state)
            );
        """)
    cnx.commit()
