


import requests
from bs4 import BeautifulSoup

import numpy as np
import pandas as pd

import re

provinces = {1: "Вінницька", 13: "Миколаївська", 2: "Волинська", 14: "Одеська", 3: "Дніпропетровська", 15: "Полтавська",
             4: "Донецька", 16: "Рівенська", 5: "Житомирська", 17: 'Сумська', 6: "Закарпатська", 18: "Тернопільська",
             7: "Запорізька", 19: "Харківська",
             8: "Івано-Франківська", 20: "Херсонська", 9: "Київська", 21: "Хмельницька", 10: "Кіровоградська",
             22: "Черкаська", 11: "Луганська", 23: "Чернівецька",
             12: "Львівська", 24: "Чернігівська", 25: "Республіка Крим"}







def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_provinces_data(oblast, when):
    parse_from,parse_to = when
    url = "https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_provinceData.php?country=UA&provinceID={}&year1={}&year2={}&type=Mean".format(
            oblast, parse_from, parse_to)

    resp = get_url(url)

    filename = oblast + "_" + 'Mean' + "_" + parse_from + "-" + parse_to + '.txt'
    open(filename, 'wb').write(str.encode(resp))
    print(filename, " created.")
    return filename


def choose_province():
    for every in dict.keys(provinces):
        print(every, " <=> ", provinces[every])
    oblast = input("Яку область оберете?: ")
    while True:
        from_to = input('Виберіть роки пошуку?: ').split()
        a,c=from_to
        if c>a:
            break
    print("Зачекайте, триває завантаження")
    return get_provinces_data(oblast, from_to)

def get_file_to_normal_stage(file):
    data = open(file, 'r').read()
    data = data[data.find('<pre>') + 5:data.find("</pre></tt>")]
    write_to = open(file, 'w').write(data)


def mean_file(file):
    raw = open(file, 'r+')
    headers = raw.readline().rstrip()
    headers = headers.split(',')[:2] + headers.split(',')[4:]
    data = raw.readlines()

    result = []

    # deleting stuff to get it in df
    for every in data:
        result.append(str(re.sub(r',\s\s|\s\s|\s|,\s', ',', every)[:-1]).split(','))

    df = pd.DataFrame(result, columns=headers)

    return df




filename = choose_province()
get_file_to_normal_stage(filename)

df = mean_file(filename)

print(df.head(20))
print(df.VHI.min())
print(df.VHI.max())



res = 0
for every in df.VHI:
    if float(every) > 25:
        res += 1

print("res= ", res)
