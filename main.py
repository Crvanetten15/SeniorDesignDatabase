import requests
from bs4 import BeautifulSoup
import sendtoSQL as s2Q
import re

list_of_regions = ['U.S. Residents, excluding U.S. Territories',
                   'New England',
                   'Middle Atlantic',
                   'East North Central',
                   'West North Central',
                   'South Atlantic',
                   'East South Central',
                   'West South Central',
                   'Mountain',
                   'Pacific',
                   'U.S. Territories',
                   'Non-U.S. Residents',
                   'Total']


def parse_table(table, col1, col2):
    global list_of_regions
    data = []
    for row in table.find_all("tr"):
        state = row.find('th')
        if state.text in list_of_regions:
            continue
        columns = row.find_all("td")
        if len(columns) > 0:
            current_week = \
                columns[col1].text.strip(
                ) if columns[col1].text.strip() != '-' else '~0'
            previous52 = columns[col2].text.strip()
            data.append([state.text, current_week, previous52])
        data = sorted(data, key=lambda x: x[0])
    return data


def give_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find(
        "table", {"class": "nndss-data-table"})
    return table
# https://wonder.cdc.gov/nndss/static/2022/06/2022-06-table1v.html

# Make Table for 2022


def runMeasles():
    for x in range(1, 53):
        x = x if x >= 10 else f'0{x}'
        url = f"https://wonder.cdc.gov/nndss/static/2022/{x}/2022-{x}-table1v.html"
        data = parse_table(give_url(url), 4, 5)
        date = re.findall("2022-..", url)

        s2Q.send(data, date[0], 'Measles')


def runMalaria():
    for x in range(1, 53):
        x = x if x >= 10 else f'0{x}'
        url = f"https://wonder.cdc.gov/nndss/static/2022/{x}/2022-{x}-table1v.html"
        data = parse_table(give_url(url), 1, 2)
        date = re.findall("2022-..", url)

        s2Q.send(data, date[0], 'Malaria')


def runMumps():
    for x in range(1, 53):
        x = x if x >= 10 else f'0{x}'
        url = f"https://wonder.cdc.gov/nndss/static/2022/{x}/2022-{x}-table1y.html"
        data = parse_table(give_url(url), 1, 2)
        date = re.findall("2022-..", url)

        s2Q.send(data, date[0], 'Mumps')


def runPneumococcal():
    for x in range(1, 53):
        x = x if x >= 10 else f'0{x}'
        url = f"https://wonder.cdc.gov/nndss/static/2022/{x}/2022-{x}-table1s.html"
        data = parse_table(give_url(url), 1, 2)
        date = re.findall("2022-..", url)

        s2Q.send(data, date[0], 'Pneumococcal disease')


def runCSyphilis():
    for x in range(1, 53):
        x = x if x >= 10 else f'0{x}'
        url = f"https://wonder.cdc.gov/nndss/static/2022/{x}/2022-{x}-table1hh.html"
        data = parse_table(give_url(url), 1, 2)
        date = re.findall("2022-..", url)

        s2Q.send(data, date[0], 'CSyphilis')


def runTuberculosis():
    for x in range(1, 53):
        x = x if x >= 10 else f'0{x}'
        url = f"https://wonder.cdc.gov/nndss/static/2022/{x}/2022-{x}-table1jj.html"
        data = parse_table(give_url(url), 1, 2)
        date = re.findall("2022-..", url)

        s2Q.send(data, date[0], 'Tuberculosis')


s2Q.makeTable()


runMeasles()
runMalaria()
runMumps()
runPneumococcal()
runCSyphilis()
runTuberculosis()
