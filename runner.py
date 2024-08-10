import os
import time
import settings

#IMPORTANT: remember to change: sys.path.append(r'C:\Users\ayele\all_scraper_1.6') in all files
#  to all_scraper_1.6's path on your device

# Location to scrape 
# 1: SACRAMENTO COUNTY (SACRAMENTO)
# 2: SAN JOAQUIN COUNTY (STOCKTON)
# 3: SANTA CLARA COUNTY (SAN JOSE)
# 4: ALAMEDA COUNTY (OAKLAND)
# 5: CONTRA COSTA COUNTY (RICHMOND)
location_input = int(input("1. SACRAMENTO COUNTY (SACRAMENTO)\n2. SAN JOAQUIN COUNTY (STOCKTON)\n3. SANTA CLARA COUNTY (SAN JOSE)\n4. ALAMEDA COUNTY (OAKLAND)\n5. CONTRA COSTA COUNTY (RICHMOND)\nEnter number of location: "))

# Capture the input
with open(r"C:\Users\ayele\realestate\all_scraper_1.6\config.txt", "w") as config_file:
    config_file.write(str(location_input))

os.chdir("scrapers")


#ALL BS4 HEAVY SCRAPERS---------------------------------------------------------------------

if settings.scrape_cbhomes==True:
    os.system("python cbhomesscraper.py")
    time.sleep(180) # Wait for 3 minutes (180 seconds)

if settings.scrape_compass==True:
    os.system("python compassscraper.py")
    time.sleep(180) # Wait for 3 minutes (180 seconds)

if settings.scrape_homes==True:
    os.system("python homesscraper.py")
    time.sleep(180) # Wait for 3 minutes (180 seconds)

if settings.scrape_mlslistings==True:
    os.system("python mlslistingsscraper.py")
    time.sleep(180) # Wait for 3 minutes (180 seconds)

if settings.scrape_point2homes==True:
    os.system("python point2homesscraper.py")
    time.sleep(180) # Wait for 3 minutes (180 seconds)

if settings.scrape_propertyshark==True:
    os.system("python propertysharkscraper.py")
    time.sleep(180) # Wait for 3 minutes (180 seconds)

if settings.scrape_redfin==True:
    os.system("python redfinscraper.py")
    time.sleep(180) # Wait for 3 minutes (180 seconds)

if settings.scrape_remax==True:
    os.system("python remaxscraper.py")
    time.sleep(180) # Wait for 3 minutes (180 seconds)

if settings.scrape_zerodown==True:
    os.system("python zerodownscraper.py")
    time.sleep(180) # Wait for 3 minutes (180 seconds)


#ALL PLAYWRIGHT HEAVY SCRAPERS---------------------------------------------------------------------

if settings.scrape_vanguard==True:
    os.system("python vanguardscraper.py")
    time.sleep(180) # Wait for 3 minutes (180 seconds)

if settings.scrape_zillow==True:
    os.system("python zillowscraper.py")
    time.sleep(180) # Wait for 3 minutes (180 seconds)

if settings.scrape_investorlift==True:
    os.system("python investorliftscraper.py")
    time.sleep(180) # Wait for 3 minutes (180 seconds)

if settings.scrape_realtor==True:
    os.system("python realtorscraper.py")
    time.sleep(180) # Wait for 3 minutes (180 seconds)

if settings.scrape_trulia==True:
    os.system("python truliascraper.py")
    time.sleep(180) # Wait for 3 minutes (180 seconds)

if settings.scrape_rockethomes==True:
    os.system("python rockethomesscraper.py")
    time.sleep(180) # Wait for 3 minutes (180 seconds)

if settings.scrape_flyhomes==True:
    os.system("python flyhomesscraper.py")
    time.sleep(180) # Wait for 3 minutes (180 seconds)

if settings.scrape_movoto==True:
    os.system("python movotoscraper.py")
    time.sleep(180) # Wait for 3 minutes (180 seconds)


