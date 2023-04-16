import mysql.connector
from weeks import get_week_number

from decouple import config

user = config('USER')
passwrd = config('PASSWRD')
database = config('DATABASE')
host = config('HOST')
config = {
    'user': f'{user}',
    'password': f'{passwrd}',
    'host': f'{host}',
    'database': f'{database}',
    'raise_on_warnings': True
}


def makeTable():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    # cursor.execute('DROP TABLE wondertables')
    cursor.execute(
        """
        CREATE TABLE daily_data (
            disease_name VARCHAR(50) NOT NULL,
            date VARCHAR(50) NOT NULL,
            disease_cases INT NOT NULL,
            disease_deaths INT NOT NULL,
            state VARCHAR(50) NOT NULL
            );
        """)
    cnx.commit()


def Send_Covid_daily(data):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    for _ in data:
        sql = \
            """
        INSERT INTO daily_data (disease_name, date, disease_cases, disease_deaths, state) VALUES
            (%s, %s, %s, %s, %s)
        """

        val = (_[0], _[1], int(_[2]), int(_[3]), _[4])
        cursor.execute(sql, val)
        cnx.commit()

    print(f"Covid Daily inserted.")


def runCovid():
    import requests
    import csv

    url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv'

    response = requests.get(url)
    reader = csv.reader(response.text.strip().split('\n'))
    days = []
    for row in reader:
        day = row[0:2] + row[3:]
        days.append(day)

    for _ in range(len(days)):
        # disease_name, date, disease_cases, death, state
        temp = "covid", days[_][0], days[_][2], days[_][3], days[_][1]
        days[_] = list(temp)
    days = days[1:]

    # Only me and god know how this works... now only god knows
    # previous = days[1][1]
    # temp = []
    # holder = []
    # holder.append(days[1])
    # for _ in range(2, len(days)):
    #     current = days[_][1]
    #     if current == previous:
    #         holder.append(days[_])
    #         continue
    #     if current != previous:
    #         temp.append(holder)
    #         holder = []
    #         if _ == len(days):
    #             break
    #         previous = days[_ + 1][1]
    # DataByDay = temp

    # for _ in days:
    #     Send_Covid_daily(_)

    days_with_week = []
    for _ in range(len(days)):
        temp = ['covid', days[_][1][:4], get_week_number(
            days[_][1]), days[_][2], days[_][3], days[_][4]]
        days_with_week.append(temp)
    print(days_with_week[:10])


'''
['covid', '2023-03-22', '308893', '1438', 'Alaska']
['covid', '2023-03-22', '8320', '34', 'American Samoa']
['covid', '2023-03-22', '2451062', '33190', 'Arizona']
['covid', '2023-03-22', '1008303', '13068', 'Arkansas']
['covid', '2023-03-22', '12155467', '104196', 'California']
'''
# daily Data
# makeTable()

runCovid()


"""
INSERT INTO weekly_data (disease_name, year, week, disease_cases, state) VALUES
    (%s, %s, %s, %s, %s)
"""
