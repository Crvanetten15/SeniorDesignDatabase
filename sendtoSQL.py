import mysql.connector
'''
Passing data into my MySQL Database
'''


def send(data, date, name):
    '''
    THIS IS THE DATA YOU NEED TO UPDATE
    '''
    user = 'adminroot'
    passwrd = 'Passw0rd'
    database = 'seniordesign'
    host = 'seniordesign.mysql.database.azure.com'
    # configuration data for logging in
    config = {
        'user': f'{user}',
        'password': f'{passwrd}',
        'host': f'{host}',
        'database': f'{database}',
        'raise_on_warnings': True
    }

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    for _ in data:
        sql = \
            """
        INSERT INTO weekly_data (disease_name, year, week, disease_cases, state) VALUES
            (%s, %s, %s, %s, %s)
        """
        year, week = map(int, date.split('-'))
        if _[1] == 'NC':
            _[1] = 0
        val = (name, year, week, _[1], _[0])
        cursor.execute(sql, val)
        cnx.commit()

    print(f"{name} : {date} inserted. ")


def makeTable():
    # configuration data for logging in

    user = 'adminroot'
    passwrd = 'Passw0rd'
    database = 'seniordesign'
    host = 'seniordesign.mysql.database.azure.com'
    config = {
        'user': f'{user}',
        'password': f'{passwrd}',
        'host': f'{host}',
        'database': f'{database}',
        'raise_on_warnings': True
    }

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    # cursor.execute('DROP TABLE wondertables')
    cursor.execute(
        """
        CREATE TABLE weekly_data (
            disease_name VARCHAR(50) NOT NULL,
            year INT NOT NULL,
            week INT NOT NULL,
            disease_cases INT NOT NULL,
            state VARCHAR(50) NOT NULL
            );
        """)
    cnx.commit()

    # cursor.execute(
    #     """
    #     INSERT INTO weekly_data (disease_name, year, week, disease_cases, state)
    #     VALUES
    #         ('COVID-19', 2022, 5, 100, 'California'),
    #         ('COVID-19', 2022, 5, 50, 'New York'),
    #         ('COVID-19', 2022, 6, 150, 'California'),
    #         ('COVID-19', 2022, 6, 80, 'New York'),
    #         ('Flu', 2023, 1, 200, 'California'),
    #         ('Flu', 2023, 1, 100, 'New York'),
    #         ('Flu', 2023, 2, 250, 'California'),
    #         ('Flu', 2023, 2, 150, 'New York');
    #     """)
    # cnx.commit()
