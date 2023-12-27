"""
Scarping script for collection of 4 tables statistics : Drivers, Bodies, Tires, Gliders
Source website : https://www.mariowiki.com/Mario_Kart_8_Deluxe_in-game_statistics

Each of the 4 tables contains in game kart features. Additionally, we collect the
in-game sprite image for each component that we store in another repository. 
Here are the resulting metadata structure : 
Driver/Body/Tire/Glider : Name of the Driver/Body/Tire/Glider
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
Image: Image name of the Driver/Body/Tire/Glider in the image file
"""

import os
from tqdm import tqdm

import requests
from bs4 import BeautifulSoup
import urllib

import config

# Creation of two distinct directories : metadata and images
for data_dir in ["metadata","images"]:
    assert not os.path.isdir(f"{config.OUT_DIR}/{data_dir}"),\
        f'Destination directory "{config.OUT_DIR}/metadata" already exists.'
    os.mkdir(f"{config.OUT_DIR}/{data_dir}")
IMAGES_OUT_DIR = f"{config.OUT_DIR}/images/"
METADATA_OUT_DIR = f"{config.OUT_DIR}/metadata/"

# Collection of the table of the MarioWiki website :
response = requests.get(config.URL)
soup = BeautifulSoup(response.text, features="lxml")
tables = soup.find_all("table")

# Players/Gliders/Tires/Bodies are the 4 first tables of the page :
for t in tables[:4]:
    # Get the body of the table and its table rows (tr):
    body = t.find("tbody")
    table_rows = body.find_all("tr")
    
    # Get title of the table :
    table_title = table_rows[0].text
    for e in ["\n"," "]:
        table_title = table_title.replace(e,"")
    print(f"Scraping of table : {table_title}")
    
    # Loop accross the rows of the table :
    for i, row in tqdm(enumerate(table_rows[1:])):
        
        # First row = Header :
        if i == 0:
            colnames = [c.text.replace("\n","") for c in row.find_all("th")]
            colnames.append("Image")
            # Creation of data list to append :
            data = [colnames]
            continue
        
        # Next rows = Components :
        # Get row header (th) and row data (td) :
        header, stats = row.find("th"), row.find_all("td")
        stats = [int(d.text) for d in stats]
        infos = header.find_all("a")
        image_url, name = infos[0], infos[1].get("title")
        if not name: continue
        stats.insert(0,name)
        
        # Collect row image :
        for e in str(image_url).split(" "):
            if e.startswith("https"):
                opener = urllib.request.URLopener()
                opener.addheader("User-Agent", 'whatever')
                opener.retrieve(e, f"{IMAGES_OUT_DIR}{name}.png")
                stats.append(f"{name}.png")
        
        # Append full stats of the row in the final data list :
        data.append(stats)
    
    # End of scraping, save result in dest_filename in metadata directory :
    dest_filename = f"{METADATA_OUT_DIR}{table_title}.txt"
    print(f"Scraping successful, destination file : {dest_filename}")
    with open(dest_filename,"w") as data_file:
        for row in data:
            for i,d in enumerate(row):
                data_file.write(str(d))
                if i != len(row)-1:
                    data_file.write(",")
            data_file.write("\n")
    data_file.close()