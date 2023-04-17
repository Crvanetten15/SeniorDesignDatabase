import requests
from bs4 import BeautifulSoup
import sendtoSQL as s2Q
from covid import buildCovid, covidTable
import re
import time

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
                ) if columns[col1].text.strip() != '-' else '0'
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


def runIndividual(url, name, year, indexes):
    data = parse_table(give_url(url), indexes[0], indexes[1])
    date = re.findall(f"{year}-..", url)
    s2Q.send(data, date[0], f'{name}')


def Malaria(year):
    for x in range(1, 53):
        x = x if x >= 10 else f'0{x}'
        url = f"https://wonder.cdc.gov/nndss/static/{year}/{x}/{year}-{x}-table1v.html"
        runIndividual(url, "malaria", year, [0, 1])


def Malaria23(year):
    for x in range(1, 14):
        x = x if x >= 10 else f'0{x}'
        url = f"https://wonder.cdc.gov/nndss/static/{year}/{x}/{year}-{x}-table860.html"
        runIndividual(url, "malaria", year, [0, 1])


def Campylobacteriosis(year):
    for x in range(1, 53):
        x = x if x >= 10 else f'0{x}'
        url = f"https://wonder.cdc.gov/nndss/static/{year}/{x}/{year}-{x}-table1f.html"
        runIndividual(url, "campylobacteriosis", year, [4, 5])


def Campylobacteriosis23(year):
    for x in range(1, 14):
        x = x if x >= 10 else f'0{x}'
        url = f"https://wonder.cdc.gov/nndss/static/{year}/{x}/{year}-{x}-table350.html"
        runIndividual(url, "campylobacteriosis", year, [0, 1])


def Pneumococcal(year):
    for x in range(1, 53):
        x = x if x >= 10 else f'0{x}'
        url = f"https://wonder.cdc.gov/nndss/static/{year}/{x}/{year}-{x}-table1s.html"
        runIndividual(url, "pneumococcal", year, [0, 1])


def Pneumococcal23(year):
    for x in range(1, 14):
        x = x if x >= 10 else f'0{x}'
        url = f"https://wonder.cdc.gov/nndss/static/{year}/{x}/{year}-{x}-table773.html"
        runIndividual(url, "pneumococcal", year, [0, 1])


def Syphilis(year):
    for x in range(1, 53):
        x = x if x >= 10 else f'0{x}'
        url = f"https://wonder.cdc.gov/nndss/static/{year}/{x}/{year}-{x}-table1hh.html"
        runIndividual(url, "syphilis", year, [4, 5])


def Syphilis19(year):
    for x in range(1, 53):
        x = x if x >= 10 else f'0{x}'
        url = f"https://wonder.cdc.gov/nndss/static/{year}/{x}/{year}-{x}-table1hh.html"
        runIndividual(url, "syphilis", year, [8, 9])


def Syphilis23(year):
    for x in range(1, 14):
        x = x if x >= 10 else f'0{x}'
        url = f"https://wonder.cdc.gov/nndss/static/{year}/{x}/{year}-{x}-table1260.html"
        runIndividual(url, "syphilis", year, [0, 1])


def Tuberculosis(year):
    for x in range(1, 53):
        x = x if x >= 10 else f'0{x}'
        url = f"https://wonder.cdc.gov/nndss/static/{year}/{x}/{year}-{x}-table1jj.html"
        runIndividual(url, "tuberculosis", year, [0, 1])


def Tuberculosis23(year):
    for x in range(1, 14):
        x = x if x >= 10 else f'0{x}'
        url = f"https://wonder.cdc.gov/nndss/static/{year}/{x}/{year}-{x}-table1309.html"
        runIndividual(url, "tuberculosis", year, [0, 1])


def Gonorrhea(year):
    for x in range(1, 53):
        x = x if x >= 10 else f'0{x}'
        url = f"https://wonder.cdc.gov/nndss/static/{year}/{x}/{year}-{x}-table1m.html"
        runIndividual(url, "gonorrhea", year, [0, 1])


def Gonorrhea23(year):
    for x in range(1, 14):
        x = x if x >= 10 else f'0{x}'
        url = f"https://wonder.cdc.gov/nndss/static/{year}/{x}/{year}-{x}-table560.html"
        runIndividual(url, "gonorrhea", year, [0, 1])


def Chlamydia(year):
    for x in range(1, 53):
        x = x if x >= 10 else f'0{x}'
        url = f"https://wonder.cdc.gov/nndss/static/{year}/{x}/{year}-{x}-table1g.html"
        runIndividual(url, "chlamydia", year, [4, 5])


def Chlamydia20(year):
    for x in range(1, 53):
        x = x if x >= 10 else f'0{x}'
        url = f"https://wonder.cdc.gov/nndss/static/{year}/{x}/{year}-{x}-table1g.html"
        runIndividual(url, "chlamydia", year, [8, 9])


def Chlamydia23(year):
    for x in range(1, 14):
        x = x if x >= 10 else f'0{x}'
        url = f"https://wonder.cdc.gov/nndss/static/{year}/{x}/{year}-{x}-table370.html"
        runIndividual(url, "chlamydia", year, [0, 1])


def GonorrheaALL():
    Gonorrhea(2019)
    time.sleep(1)
    Gonorrhea(2020)
    time.sleep(1)
    Gonorrhea(2021)
    time.sleep(1)
    Gonorrhea(2022)
    time.sleep(1)
    Gonorrhea23(2023)
    time.sleep(1)


def ChlamydiaALL():
    Chlamydia(2019)
    time.sleep(1)
    Chlamydia20(2020)
    time.sleep(1)
    Chlamydia20(2021)
    time.sleep(1)
    Chlamydia20(2022)
    time.sleep(1)
    Chlamydia23(2023)
    time.sleep(1)


def TuberculosisALL():
    Tuberculosis(2021)
    time.sleep(1)
    Tuberculosis(2022)
    time.sleep(1)
    Tuberculosis23(2023)
    time.sleep(1)


def SyphilisALL():
    Syphilis19(2019)
    time.sleep(1)
    Syphilis(2020)
    time.sleep(1)
    Syphilis(2021)
    time.sleep(1)
    Syphilis(2022)
    time.sleep(1)
    Syphilis23(2023)
    time.sleep(1)


def MalariaALL():
    Malaria(2019)
    time.sleep(1)
    Malaria(2020)
    time.sleep(1)
    Malaria(2021)
    time.sleep(1)
    Malaria(2022)
    time.sleep(1)
    Malaria23(2023)
    time.sleep(1)


def CampylobacteriosisALL():
    Campylobacteriosis(2019)
    time.sleep(1)
    Campylobacteriosis(2020)
    time.sleep(1)
    Campylobacteriosis(2021)
    time.sleep(1)
    Campylobacteriosis(2022)
    time.sleep(1)
    Campylobacteriosis23(2023)
    time.sleep(1)


def PneumococcalALL():
    Pneumococcal(2019)
    time.sleep(1)
    Pneumococcal(2020)
    time.sleep(1)
    Pneumococcal(2021)
    time.sleep(1)
    Pneumococcal(2022)
    time.sleep(1)
    Pneumococcal23(2023)
    time.sleep(1)


def buildDB():
    # Creation of tables
    s2Q.makeTable()
    covidTable()
    # Creation of wonder tables
    GonorrheaALL()
    TuberculosisALL()
    SyphilisALL()
    MalariaALL()
    CampylobacteriosisALL()
    ChlamydiaALL()
    PneumococcalALL()
    # Initialize covid section
    buildCovid()


buildDB()
