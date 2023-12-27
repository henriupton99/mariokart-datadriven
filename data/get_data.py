import requests
from bs4 import BeautifulSoup
"""
WG: Weight
AC: Acceleration
ON: On-Road traction
OF: (Off-Road) Traction
MT: Mini-Turbo
SL: Ground Speed
SW: Water Speed
SA: Anti-Gravity Speed
SG: Air Speed
TL: Ground Handling
TW: Water Handling
TA: Anti-Gravity Handling
TG: Air Handling
IV: Invincibility  
"""


import config
response = requests.get(config.URL)
soup = BeautifulSoup(response.text, features="lxml")

tables = soup.find_all("table")

for t in tables[0:3]:
    body = t.find("tbody")
    table_rows = body.find_all("tr")

    for i, row in enumerate(table_rows):
        
        # Process title :
        if i == 0:
            table_title = row.text
            for e in ["\n"," "]:
                table_title = table_title.replace(e,"")
            continue
        # Process column names :
        if i == 1:
            colnames = [c.text.replace("\n","") for c in row.find_all("th")]
            data = [colnames]
            continue
        
        # Process character columns :
        header, stats = row.find("th"), row.find_all("td")
        stats = [int(d.text) for d in stats]
        infos = header.find_all("a")
        image_url, name = infos[0], infos[1].get("title")
        if not name:
            continue
        stats.insert(0,name)
        data.append(stats)

    with open(f"{table_title}.txt","w") as data_file:
        for row in data:
            for i,d in enumerate(row):
                data_file.write(str(d))
                if i != len(row)-1:
                    data_file.write(",")
            data_file.write("\n")
    data_file.close()