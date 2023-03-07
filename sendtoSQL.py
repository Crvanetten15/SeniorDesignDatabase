import mysql.connector
'''
Passing data into my MySQL Database
'''


def send(data, date, name):
    '''
    THIS IS THE DATA YOU NEED TO UPDATE
    '''
    user = 'root'
    passwrd = 'pass'
    database = 'dd'
    # configuration data for logging in
    config = {
        'user': f'{user}',
        'password': f'{passwrd}',
        'host': '127.0.0.1',
        'database': f'{database}',
        'raise_on_warnings': True
    }

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    for _ in data:
        sql = "INSERT INTO wondertables (disease, date, state, current_week, previous_52) VALUES (%s, %s, %s, %s, %s)"
        val = (name, date, _[0], _[1],
               _[2])
        cursor.execute(sql, val)
        cnx.commit()

    print(f"{name} : {date} inserted. ")


def makeTable():
    # configuration data for logging in

    user = 'root'
    passwrd = '@@'
    database = 'dd'
    config = {
        'user': f'{user}',
        'password': f'{passwrd}',
        'host': '127.0.0.1',
        'database': f'{database}',
        'raise_on_warnings': True
    }

    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    # cursor.execute('DROP TABLE wondertables')
    cursor.execute(
        "CREATE TABLE wondertables (disease VARCHAR(30), date VARCHAR(10), state VARCHAR(45), current_week VARCHAR(5), previous_52 VARCHAR(8));")
    cnx.commit()

    # cursor.execute('DROP TABLE coviddata')
    cursor.execute(
        "CREATE TABLE coviddata (disease VARCHAR(30), date VARCHAR(10), state VARCHAR(45), current_cases VARCHAR(5));")
    cnx.commit()
