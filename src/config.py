import os
class CONFIG:
    SCRAPING_URL = "https://www.mariowiki.com/Mario_Kart_8_Deluxe_in-game_statistics"
    DATA_PATH = "./src/data/"
    METADATA_PATH = os.path.join(DATA_PATH,"metadata")
    IMAGES_PATH = os.path.join(DATA_PATH,"images")
    
    COMPONENTS = {
        "Drivers" : (os.path.join(METADATA_PATH,"Drivers(DV).txt"),"Driver"),
        "Tires" : (os.path.join(METADATA_PATH,"Tires(TR).txt"),"Tire"),
        "Bodies" : (os.path.join(METADATA_PATH,"Bodies(BD).txt"),"Body"),
        "Gliders" : (os.path.join(METADATA_PATH,"Gliders(WG).txt"),"Glider")
    }