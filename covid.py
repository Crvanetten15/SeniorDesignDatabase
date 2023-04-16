import mysql.connector
from decouple import config
from weeks import get_week_number

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


def covidTable():
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    # cursor.execute('DROP TABLE wondertables')
    cursor.execute(
        """
        CREATE TABLE daily_data (
            disease_name VARCHAR(50) NOT NULL,
            date DATE NOT NULL,
            disease_cases INT NOT NULL,
            disease_deaths INT NOT NULL,
            state VARCHAR(50) NOT NULL
            );
        """)
    cnx.commit()


def Send_Covid_daily(data):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    for __ in data:
        for _ in __:
            sql = \
                """
            INSERT INTO daily_data (disease_name, date, disease_cases, disease_deaths, state) VALUES
                (%s, %s, %s, %s, %s)
            """

            val = (_[0], _[1], int(_[2]), int(_[3]), _[4])
            cursor.execute(sql, val)
            cnx.commit()

    print(f"Covid Daily inserted.")


def Send_Covid_Weekly(data):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    for _ in data:
        for __ in _:
            sql = \
                """
            INSERT INTO weekly_data (disease_name, year, week, disease_cases, disease_deaths, state) VALUES
                (%s, %s, %s, %s, %s, %s)
            """

            val = (__[0], __[1], int(__[2]), int(__[3]), __[4], __[5])
            cursor.execute(sql, val)
            cnx.commit()

    print(f"Covid weekly inserted.")


def grouped_list(lst, index):
    return [[x for x in lst if x[index] == i]
            for i in set(map(lambda x: x[index], lst))]


def sort_by_date(arr):
    def get_date(sub_arr):
        return sub_arr[0]

    sorted_arr = sorted(arr, key=get_date)
    return sorted_arr


def grouped_list(lst, index):
    return [[x for x in lst if x[index] == i]
            for i in set(map(lambda x: x[index], lst))]


def sort_by_index(lst, index):
    sorted_list = []
    for sub_list in lst:
        sorted_sub_list = sorted(sub_list, key=lambda x: x[index])
        sorted_list.append(sorted_sub_list)
    return sorted_list


def runCovid():
    global data_2020, data_2021, data_2022, data_2023
    import requests
    import csv

    url = 'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv'

    response = requests.get(url)
    reader = csv.reader(response.text.strip().split('\n'))
    days = []
    for row in reader:
        day = row[0:2] + row[3:]
        days.append(day)
    days = days[1:]
    for _ in range(len(days)):
        # disease_name, date, disease_cases, death, state
        temp = "covid", days[_][0], int(
            days[_][2]), int(days[_][3]), days[_][1]
        days[_] = list(temp)

    # print(days)
    states = grouped_list(days, 4)
    # print(states)
    for _ in range(len(states)):
        sorted_arr = sort_by_date(states[_])
        states[_] = sorted_arr

    for _ in range(len(states)):
        previous_case = states[_][0][2]
        previous_death = states[_][0][3]
        for i in range(1, len(states[_])):
            old_cases = states[_][i][2]
            old_deaths = states[_][i][3]
            states[_][i][2] -= previous_case
            states[_][i][3] -= previous_death
            states[_][i][2] = states[_][i][2] if states[_][i][2] >= 0 else 0
            states[_][i][3] = states[_][i][3] if states[_][i][3] >= 0 else 0
            previous_case = old_cases
            previous_death = old_deaths
    return states
    # Send_Covid_daily(states)

# Processes all data for covid and Adds it


def returnTotals(data):
    WeeklyData = []
    for _ in range(len(data)):
        # print(data[_])
        Current_week = grouped_list(data[_], 5)
        for i in range(len(Current_week)):
            total_cases = 0
            total_deaths = 0
            temp = []
            for x in Current_week[i]:
                year = x[1]
                week = x[2]
                total_cases += int(x[3])
                total_deaths += int(x[4])
                state = x[5]
            temp.append(['covid', year, week,
                        total_cases, total_deaths, state])
            Current_week[i] = temp[0]
        WeeklyData.append(Current_week)
    return WeeklyData


def setWeekly(data):
    data = [inner for outer in data for inner in outer]
    holder = []
    for _ in range(len(data)):
        temp = ['covid', int(data[_][1][:4]), get_week_number(
            data[_][1]), data[_][2], data[_][3], data[_][4]]
        holder.append(temp)
    data = holder
    data_sorted_by_year = grouped_list(data, 1)
    data_sorted_by_year = sort_by_index(data_sorted_by_year, 1)

    data_2020 = grouped_list(data_sorted_by_year[0], 2)
    data_2021 = grouped_list(data_sorted_by_year[1], 2)
    data_2022 = grouped_list(data_sorted_by_year[2], 2)
    data_2023 = grouped_list(data_sorted_by_year[3], 2)

    data_2020 = returnTotals(data_2020)
    data_2021 = returnTotals(data_2021)
    data_2022 = returnTotals(data_2022)
    data_2023 = returnTotals(data_2023)
    Full_WeeklyData = data_2020 + data_2021 + data_2022 + data_2023

    return Full_WeeklyData


def buildCovid():
    # does Daily
    states = runCovid()
    Send_Covid_daily(states)
    week_data = setWeekly(states)
    Send_Covid_Weekly(week_data)
