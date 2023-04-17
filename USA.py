
import csv
import mysql.connector

from decouple import config

user = config('USER')
passwrd = config('PASSWRD')
database = config('DATABASE')
host = config('HOST')

'''
THIS IS THE DATA YOU NEED TO UPDATE
'''
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

cursor.execute(
        """
        CREATE TABLE population_data (
            state VARCHAR(50) NOT NULL,
            population INT NOT NULL,
            urban_population DOUBLE NOT NULL
            );
        """)
cnx.commit()

usa_pop = []
with open('population.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for x in reader:
        state = x["ï»¿Geographic Area"]
        totals = x['April 1, 2020 Estimates Base']
        usa_pop.append([state, totals])

urban_pop = []
with open('urban_population.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for x in reader:
        # print(x)
        state = x['State']
        percentage = x['total_percent']
        urban_pop.append([state, percentage])


def merge_data(data1, data2):
    # Create a dictionary to store the merged data
    merged_data = {}

    # Loop through the first list and add the state and total to the dictionary
    for state, total in data1:
        merged_data[state] = [total]

    # Loop through the second list and add the percentage to the corresponding state in the dictionary
    for state, percentage in data2:
        merged_data[state].append(percentage)

    # Convert the dictionary back to a list of lists
    result = [[state, *merged_data[state]] for state in merged_data]

    return result


result = merge_data(usa_pop, urban_pop)

for _ in result:
    sql = \
        """
    INSERT INTO population_data (state, population, urban_population) VALUES
        (%s, %s, %s)
    """
    val = (_[0], int(_[1].replace(',','')), float(_[2]))
    cursor.execute(sql, val)
    cnx.commit()
