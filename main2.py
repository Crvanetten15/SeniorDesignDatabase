import math
import pandas
import mysql.connector

from decouple import config
'''
Passing data into my MySQL Database
'''
user = config('USER')
passwrd = config('PASSWRD')
database = config('DATABASE')
host = config('HOST')


def send(name, year, week, data, state):
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

    sql = \
        """
    INSERT INTO prediction_weekly_data (disease_name, year, week, disease_cases, disease_deaths, state) VALUES
        (%s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE disease_cases = disease_cases, disease_deaths = disease_deaths; 
    """

    val = (name, year, week, data, 0, state)
    cursor.execute(sql, val)
    cnx.commit()

    print(f"{name} : {week} inserted. ")


df = pandas.read_csv("preds.csv")

df = df.drop(["ID"], axis=1)
weeks = [14, 15, 16, 17]

# for _ in range(len(df)):
#     if (df["locality"][_] == "US"):
#         continue
#     totals = df["predictions"][_][2:-2].split()
#     # print(len(totals))
#     for i in range(len(totals)):
#         totals[i] = float(totals[i])
#         totals[i] = int(totals[i])
#         if totals[i] <= -20:
#             totals[i] = totals[i] * -1
#         elif totals[i] <= 0:
#             totals[i] = 0

#     for y in range(len(totals)):
#         send(df["disease_name"][_], 2023, weeks[y],
#              totals[y],  df["locality"][_])


def sendC(name, year, week, data, ):
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

    sql = \
        """
    INSERT INTO prediction_weekly_totals (disease, year, week, CasesInWeek) VALUES
        (%s, %s, %s, %s); 
    """

    val = (name, year, week, data)
    cursor.execute(sql, val)
    cnx.commit()

    print(f"TOTALS {name} : {week} inserted. ")


for _ in range(8):
    totals = df["predictions"][_][2:-2].split()
    # print(len(totals))
    for i in range(len(totals)):
        totals[i] = float(totals[i])
        totals[i] = math.ceil(totals[i])
        totals[i] = int(totals[i])
        if totals[i] <= -20:
            totals[i] = totals[i] * -1
        elif totals[i] <= 0:
            totals[i] = 0

    for x in range(len(totals)):
        sendC(df["disease_name"][_], 2023, weeks[x], totals[x])
