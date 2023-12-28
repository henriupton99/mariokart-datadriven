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

import sys, os
from copy import deepcopy
sys.path.insert(0,"..")
from tqdm import tqdm

import requests
from bs4 import BeautifulSoup
import urllib

from config import CONFIG

# Creation of two distinct directories : metadata and images
#for data_path in [CONFIG.METADATA_PATH,CONFIG.IMAGES_PATH]:
#    assert not os.path.isdir(data_path),\
#        f'Destination directory "{data_path}" already exists.'
#    os.mkdir(data_path)

# Collection of the table of the MarioWiki website :
response = requests.get(CONFIG.SCRAPING_URL)
soup = BeautifulSoup(response.text, features="lxml")
tables = soup.find_all("table")

# Players/Gliders/Tires/Bodies are the 4 first tables of the page :
for n,table in enumerate(tables[:4]):
    # Get the body of the table and its table rows (tr):
    body = table.find("tbody")
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
        try:
            unique_id = header.find("i").text
            assert unique_id != "1"
            name = f"{name}({unique_id})"
        except:
            pass
        
        # If no name found or the name is already in the list, we break
        # particular case : Link has 2 forms but both have the same stats
        # so we omit the second form 
        if not name: continue
        stats.insert(0,name)
        
        # Collect row image :
        for e in str(image_url).split(" "):
            if e.startswith("https"):
                opener = urllib.request.URLopener()
                opener.addheader("User-Agent", 'whatever')
                opener.retrieve(e, os.path.join(CONFIG.IMAGES_PATH,f"{name}.png"))
                stats.append(f"{name}.png")
        
        # Append full stats of the row in the final data list :
        data.append(stats)
        
        # Particular cases : add Mii Small size & Mii Large size :
        # Small Size == same characteristics than Bebe Luigi :
        if name == "Baby Mario(MroB)":
            mii_stats = deepcopy(stats)
            mii_stats[0] = "Mii(MiiS)"
            mii_stats[-1] = "Mii(MiiM).png"
            data.append(mii_stats)
        
        # Large Size == same characteristics than Dry Bowser :
        if name == "Dry Bowser(KopB)":
            mii_stats = deepcopy(stats)
            mii_stats[0] = "Mii(MiiL)"
            mii_stats[-1] = "Mii(MiiM).png"
            data.append(mii_stats)
        
    # End of scraping, save result in dest_filename in metadata directory :
    dest_filename = os.path.join(CONFIG.METADATA_PATH,f"{table_title}.txt")
    print(f"Scraping successful, destination file : {dest_filename}")
    with open(dest_filename,"w") as data_file:
        for row in data:
            for i,d in enumerate(row):
                data_file.write(str(d))
                if i != len(row)-1:
                    data_file.write(",")
            data_file.write("\n")
    data_file.close()