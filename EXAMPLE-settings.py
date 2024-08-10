#IMPORTANT: remember to change 'C:\\Users\\ayele\\realestate\\all_scraper_1.6' in all files
#  to all_scraper_1.6's path on your device
folder_path = 'C:\\Users\\ayele\\realestate\\all_scraper_1.6'

# Hud API settup:
HUD_API_KEY = 'YOUR_HUD_API_KEY'
HUD_BASE_URL = 'https://www.huduser.gov/hudapi/public/fmr'
STATE_CODE = 'CA'
FMR_YEAR = '2023'
DEFAULT_FMR = 1100 # if not able to find fmrs
SECURE_HEADER = {
    'Authorization': f'Bearer {HUD_API_KEY}',
    'Content-Type': 'application/json'
}    


# Location to scrape 
# 1: SACRAMENTO COUNTY  (SACRAMENTO)
# 2: SAN JOAQUIN COUNTY (STOCKTON)
# 3: SANTA CLARA COUNTY (SAN JOSE)
# 4: ALAMEDA COUNTY (OAKLAND)
# 5: CONTRA COSTA COUNTY (RICHMOND)

# Read the location input from the config file
with open(r"C:\Users\ayele\realestate\all_scraper_1.6\config.txt", "r") as config_file:
    location = int(config_file.read())

#location = 1

# Function to return location string based on specified location (counties)
def location_assign(location):
    if location == 1:
        return 'SACRAMENTOCOUNTY'
    elif location == 2:
        return 'SANJOAQUINCOUNTY'
    elif location == 3:
        return 'SANTACLARACOUNTY'
    elif location == 4:
        return 'ALAMEDACOUNTY'
    elif location == 5:
        return 'CONTRACOSTACOUNTY'

# Function to assign url based on specified location
def url_assign(location, sacramento, sanjoaquin, santaclara, alameda, contracosta):
    if location == 1:
        return sacramento
    elif location == 2:
        return sanjoaquin
    elif location == 3:
        return santaclara
    elif location == 4:
        return alameda
    elif location == 5:
        return contracosta

# Function to assign pages based on specified location
def pages_assign(location, sacramento_pages, sanjoaquin_pages, santaclara_pages, alameda_pages, contracosta_pages):
    if location == 1:
        return sacramento_pages
    elif location == 2:
        return sanjoaquin_pages
    elif location == 3:
        return santaclara_pages
    elif location == 4:
        return alameda_pages
    elif location == 5:
        return contracosta_pages

#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
#                                         BEATIFULSOUP4 HEAVY SCRAPERS                                                    
#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>


# SCRAPE COLDWELLBANKERHOMES.COM ------------------------------------------------------------
scrape_cbhomes = True
cbhomes_url =url_assign(location,
    # example link: 'https://www.coldwellbankerhomes.com/ca/sacramento/kvc-17_2/'
    # Sacramento County (Sacramento)
    'https://www.coldwellbankerhomes.com/ca/sacramento-county/kvc-17_2/',
    # San Joaquin County (Stockton)
    'https://www.coldwellbankerhomes.com/ca/san-joaquin-county/kvc-17_2/',
    # Santa Clara County (San Jose)
    'https://www.coldwellbankerhomes.com/ca/santa-clara-county/kvc-17_2/',
    # Alameda County (Oakland)
    'https://www.coldwellbankerhomes.com/ca/alameda-county/kvc-17_2/',
    # Contra Costa County (Richmond) 
    'https://www.coldwellbankerhomes.com/ca/contra-costa-county/kvc-17_2/'
)
cbhomes_pages = pages_assign(location,
    # Sacramento County (Sacramento)
    4,
    # San Joaquin County (Stockton)
    4,
    # Santa Clara County (San Jose)
    4,
    # Alameda County (Oakland)
    5,
    # Contra Costa County (Richmond) 
    4
)

# proxy settings:
# If this is true, script will use proxies when using request.get() method
CBHOMES_REQUEST_GET_PROXIES_USE = False
# Which proxy service would you like to use for the request.get() method? Options are:
# 1. 'scrapeops'
# 2. 'oxylabs'
# 3. 'iproyal'
# 4. 'scrapingbee'
CBHOMES_REQUEST_GET_PROXIES_SERVICE = 'scrapeops'

# SCRAPE COMPASS.COM -----------------------------------------------------------------------
scrape_compass = False
compass_url =url_assign(location,
    #example link: 'https://www.compass.com/homes-for-sale/sacramento-ca/property-type=multi-family/'
    # Sacramento County (Sacramento)
    'https://www.compass.com/homes-for-sale/sacramento-county-ca/property-type=multi-family/',
    # San Joaquin County (Stockton)
    'https://www.compass.com/homes-for-sale/san-joaquin-county-ca/property-type=multi-family/',
    # Santa Clara County (San Jose)
    'https://www.compass.com/homes-for-sale/santa-clara-county-ca/property-type=multi-family/',
    # Alameda County (Oakland)
    'https://www.compass.com/homes-for-sale/alameda-county-ca/property-type=multi-family/',
    # Contra Costa County (Richmond) 
    'https://www.compass.com/homes-for-sale/contra-costa-county-ca/property-type=multi-family/'
)
compass_pages = pages_assign(location,
    # Sacramento County (Sacramento)
    18,
    # San Joaquin County (Stockton)
    4,
    # Santa Clara County (San Jose)
    4,
    # Alameda County (Oakland)
    8,
    # Contra Costa County (Richmond) 
    4
)

# proxy settings:
# If this is true, script will use proxies when using request.get() method
COMPASS_REQUEST_GET_PROXIES_USE = False
# Which proxy service would you like to use for the request.get() method? Options are:
# 1. 'scrapeops'
# 2. 'oxylabs'
# 3. 'iproyal'
# 4. 'scrapingbee'
COMPASS_REQUEST_GET_PROXIES_SERVICE = 'scrapeops'

# SCRAPE HOMES.COM ------------------------------------------------------------------------
scrape_homes = False
homes_url =url_assign(location,
    # example link: 'https://www.homes.com/sacramento-county-ca/'
    # Sacramento County (Sacramento)
    'https://www.homes.com/sacramento-county-ca/',
    # San Joaquin County (Stockton)
    'https://www.homes.com/san-joaquin-county-ca/',
    # Santa Clara County (San Jose)
    'https://www.homes.com/santa-clara-county-ca/',
    # Alameda County (Oakland)
    'https://www.homes.com/alameda-county-ca/',
    # Contra Costa County (Richmond) 
    'https://www.homes.com/contra-costa-county-ca/'
)
homes_pages = pages_assign(location,
    # Sacramento County (Sacramento)
    4,
    # San Joaquin County (Stockton)
    4,
    # Santa Clara County (San Jose)
    4,
    # Alameda County (Oakland)
    18,
    # Contra Costa County (Richmond) 
    4
)

# proxy settings:
# If this is true, script will use proxies when using request.get() method
HOMES_REQUEST_GET_PROXIES_USE = True
# Which proxy service would you like to use for the request.get() method? Options are:
# 1. 'scrapeops'
# 2. 'oxylabs'
# 3. 'iproyal'
# 4. 'scrapingbee'
HOMES_REQUEST_GET_PROXIES_SERVICE = 'scrapeops'

# SCRAPE MLSLISTINGS.COM ------------------------------------------------------------------
scrape_mlslistings = True
# make sure there is no '/1' at the end of the urls!!!
mlslistings_url =url_assign(location,
    # example link: 'https://www.mlslistings.com/Search/Result/63c50642-5609-4c69-a3c1-fbcd23f5dcc1/'
    # Sacramento County (Sacramento)
    'https://www.mlslistings.com/Search/Result/f7b60af5-e585-4e27-8c42-b0f9542d748e/',
    # San Joaquin County (Stockton)
    'https://www.mlslistings.com/Search/Result/31de6b11-d294-416f-80a2-5f481cc654a2/',
    # Santa Clara County (San Jose)
    'https://www.mlslistings.com/Search/Result/8884d771-3d21-4fac-8d3a-6516ad5a3c27/',
    # Alameda County (Oakland)
    'https://www.mlslistings.com/Search/Result/5269971a-d455-4213-9337-ef9d85eb2439/',
    # Contra Costa County (Richmond) 
    'https://www.mlslistings.com/Search/Result/e76502d7-9615-48af-9304-b227d9f23171/'
)
mlslistings_pages = pages_assign(location,
    # Sacramento County (Sacramento)
    8,
    # San Joaquin County (Stockton)
    4,
    # Santa Clara County (San Jose)
    4,
    # Alameda County (Oakland)
    10,
    # Contra Costa County (Richmond) 
    4
)

# proxy settings:
# If this is true, script will use proxies when using request.get() method
MLSLISTINGS_REQUEST_GET_PROXIES_USE = False
# Which proxy service would you like to use for the request.get() method? Options are:
# 1. 'scrapeops'
# 2. 'oxylabs'
# 3. 'iproyal'
# 4. 'scrapingbee'
MLSLISTINGS_REQUEST_GET_PROXIES_SERVICE = 'scrapeops'

# SCRAPE POINT2HOMES.COM ------------------------------------------------------------------
scrape_point2homes = True
point2homes_url =url_assign(location,
    # example link: 'https://www.point2homes.com/US/Real-Estate-Listings/CA/Oakland.html?PropertyType=MultiFamily'
    # Sacramento County (Sacramento)
    'https://www.point2homes.com/US/Real-Estate-Listings/CA/Sacramento.html?PropertyType=MultiFamily',
    # San Joaquin County (Stockton)
    'https://www.point2homes.com/US/Real-Estate-Listings/CA/San-Joaquin-County.html?PropertyType=MultiFamily',
    # Santa Clara County (San Jose)
    'https://www.point2homes.com/US/Real-Estate-Listings/CA/Santa-Clara-County.html?PropertyType=MultiFamily',
    # Alameda County (Oakland)
    'https://www.point2homes.com/US/Real-Estate-Listings/CA/Alameda-County.html?PropertyType=MultiFamily',
    # Contra Costa County (Richmond) 
    'https://www.point2homes.com/US/Real-Estate-Listings/CA/Contra-Costa-County.html?PropertyType=MultiFamily'
)
point2homes_pages = pages_assign(location,
    # Sacramento County (Sacramento)
    1,
    # San Joaquin County (Stockton)
    4,
    # Santa Clara County (San Jose)
    4,
    # Alameda County (Oakland)
    4,
    # Contra Costa County (Richmond) 
    4
)

# proxy settings:
# If this is true, script will use proxies when using request.get() method
POINT2HOMES_REQUEST_GET_PROXIES_USE = True
# Which proxy service would you like to use for the request.get() method? Options are:
# 1. 'scrapeops'
# 2. 'oxylabs'
# 3. 'iproyal'
# 4. 'scrapingbee'
POINT2HOMES_REQUEST_GET_PROXIES_SERVICE = 'scrapeops'

# SCRAPE PROPERTYSHARK.COM ----------------------------------------------------------------
scrape_propertyshark = True
propertyshark_url =url_assign(location,
    # example link: 'https://www.propertyshark.com/homes/US/Real-Estate-Listings/CA/Oakland.html?PropertyType=MultiFamily'
    # Sacramento County (Sacramento)
    'https://www.propertyshark.com/homes/US/Real-Estate-Listings/CA/Sacramento-County.html?PropertyType=MultiFamily',
    # San Joaquin County (Stockton)
    'https://www.propertyshark.com/homes/US/Real-Estate-Listings/CA/San-Joaquin-County.html?PropertyType=MultiFamily',
    # Santa Clara County (San Jose)
    'https://www.propertyshark.com/homes/US/Real-Estate-Listings/CA/Santa-Clara-County.html?PropertyType=MultiFamily',
    # Alameda County (Oakland)
    'https://www.propertyshark.com/homes/US/Real-Estate-Listings/CA/Alameda-County.html?PropertyType=MultiFamily',
    # Contra Costa County (Richmond) 
    'https://www.propertyshark.com/homes/US/Real-Estate-Listings/CA/Contra-Costa-County.html?PropertyType=MultiFamily'
)
propertyshark_pages = pages_assign(location,
    # Sacramento County (Sacramento)
    1,
    # San Joaquin County (Stockton)
    4,
    # Santa Clara County (San Jose)
    4,
    # Alameda County (Oakland)
    3,
    # Contra Costa County (Richmond) 
    4
)

# proxy settings:
# If this is true, script will use proxies when using request.get() method
PROPERTYSHARK_REQUEST_GET_PROXIES_USE = False
# Which proxy service would you like to use for the request.get() method? Options are:
# 1. 'scrapeops'
# 2. 'oxylabs'
# 3. 'iproyal'
# 4. 'scrapingbee'
PROPERTYSHARK_REQUEST_GET_PROXIES_SERVICE = 'scrapeops'

# SCRAPE REDFIN.COM -----------------------------------------------------------------------
scrape_redfin = True
redfin_url =url_assign(location,
    # example link: 'https://www.redfin.com/city/16409/CA/Sacramento/filter/property-type=multifamily'
    # Sacramento County (Sacramento)
    'https://www.redfin.com/county/336/CA/Sacramento-County/filter/property-type=multifamily',
    # San Joaquin County (Stockton)
    'https://www.redfin.com/county/341/CA/San-Joaquin-County/filter/property-type=multifamily',
    # Santa Clara County (San Jose)
    'https://www.redfin.com/county/345/CA/Santa-Clara-County/filter/property-type=multifamily',
    # Alameda County (Oakland)
    'https://www.redfin.com/county/303/CA/Alameda-County/filter/property-type=multifamily',
    # Contra Costa County (Richmond) 
    'https://www.redfin.com/county/309/CA/Contra-Costa-County/filter/property-type=multifamily'
)
redfin_pages = pages_assign(location,
    # Sacramento County (Sacramento)
    3,
    # San Joaquin County (Stockton)
    4,
    # Santa Clara County (San Jose)
    4,
    # Alameda County (Oakland)
    8,
    # Contra Costa County (Richmond) 
    4
)

# proxy settings:
# If this is true, script will use proxies when using request.get() method
REDFIN_REQUEST_GET_PROXIES_USE = True
# Which proxy service would you like to use for the request.get() method? Options are:
# 1. 'scrapeops'
# 2. 'oxylabs'
# 3. 'iproyal'
# 4. 'scrapingbee'
REDFIN_REQUEST_GET_PROXIES_SERVICE = 'scrapeops'

# SCRAPE REMAX.COM ------------------------------------------------------------------------
scrape_remax = True
remax_url =url_assign(location,
    #example link: 'https://www.remax.com/homes-for-sale/ca/sacramento/city/0664000/'
    # Sacramento County (Sacramento)
    'https://www.remax.com/multi-family-homes-for-sale/ca/sacramento/city/0664000/',
    # San Joaquin County (Stockton)
    'https://www.remax.com/multi-family-homes-for-sale/ca/san-joaquin/county/06077/',
    # Santa Clara County (San Jose)
    'https://www.remax.com/multi-family-homes-for-sale/ca/santa-clara/county/06085/',
    # Alameda County (Oakland)
    'https://www.remax.com/multi-family-homes-for-sale/ca/alameda/county/06001/',
    # Contra Costa County (Richmond) 
    'https://www.remax.com/multi-family-homes-for-sale/ca/contra-costa/county/06013/'
)
remax_pages = pages_assign(location,
    # Sacramento County (Sacramento)
    5,
    # San Joaquin County (Stockton)
    4,
    # Santa Clara County (San Jose)
    4,
    # Alameda County (Oakland)
    10,
    # Contra Costa County (Richmond) 
    4
)

# proxy settings:
# If this is true, script will use proxies when using request.get() method
REMAX_REQUEST_GET_PROXIES_USE = False
# Which proxy service would you like to use for the request.get() method? Options are:
# 1. 'scrapeops'
# 2. 'oxylabs'
# 3. 'iproyal'
# 4. 'scrapingbee'
REMAX_REQUEST_GET_PROXIES_SERVICE = 'scrapeops'

# SCRAPE ZERODOWN.COM ---------------------------------------------------------------------
scrape_zerodown = False
zerodown_url =url_assign(location, 
    # example link: 'https://zerodown.com/homes-for-sale/san-jose--ca?searchCode=eyJsaW1pdCI6MTgsIm9mZnNldCI6MCwiZmlsdGVycyI6eyJjaXRpZXMiOlsiU2FuIEpvc2UiXSwic2VvS2V5d29yZCI6IiIsInN0YXRlcyI6WyJDQSJdLCJzdGF0dXNlcyI6WyJGT1JfU0FMRSIsIlBFTkRJTkciLCJDT01JTkdfU09PTiJdLCJob21lVHlwZXMiOlsibXVsdGktZmFtaWx5Il19fQ%3D%3D%2F'
    # Sacramento County (Sacramento)
    'https://zerodown.com/c/search?location=sacramento-county--ca&searchCode=eyJsaW1pdCI6MTgsIm9mZnNldCI6MCwiZmlsdGVycyI6eyJjaXRpZXMiOlsiU2FuIEpvc2UiXSwiaG9tZVR5cGVzIjpbIm11bHRpLWZhbWlseSJdLCJzZW9LZXl3b3JkIjoiIiwic3RhdGVzIjpbIkNBIl0sInN0YXR1c2VzIjpbIkZPUl9TQUxFIiwiUEVORElORyIsIkNPTUlOR19TT09OIl19LCJib3VuZHMiOnsibGF0TWF4IjozOS4zNTE0NzcyOTI0MDg4NiwibGF0TWluIjozNy4zNzYxMzg3MTA2NTMzOCwibG9uZ01pbiI6LTEyNC4wNTc4OTkzNTk4MDMxMywibG9uZ01heCI6LTExOS43MTI3NzE5MDEwMTI4NH19',
    # San Joaquin County (Stockton)
    'https://zerodown.com/c/search?searchCode=eyJsaW1pdCI6MTgsIm9mZnNldCI6MCwiZmlsdGVycyI6eyJjaXRpZXMiOlsiU2FuIEpvc2UiXSwiaG9tZVR5cGVzIjpbIm11bHRpLWZhbWlseSJdLCJzZW9LZXl3b3JkIjoiIiwic3RhdGVzIjpbIkNBIl0sInN0YXR1c2VzIjpbIkZPUl9TQUxFIiwiUEVORElORyIsIkNPTUlOR19TT09OIl19LCJib3VuZHMiOnsibGF0TWluIjozNy40ODE3ODMsImxhdE1heCI6MzguMzAwMjUyLCJsb25nTWluIjotMTIxLjU4NTA3OCwibG9uZ01heCI6LTEyMC45MTcxNzF9fQ%3D%3D&location=san-joaquin-county--ca',
    # Santa Clara County (San Jose)
    'https://zerodown.com/c/search?searchCode=eyJsaW1pdCI6MTgsIm9mZnNldCI6MCwiZmlsdGVycyI6eyJjaXRpZXMiOlsiU2FuIEpvc2UiXSwiaG9tZVR5cGVzIjpbIm11bHRpLWZhbWlseSJdLCJzZW9LZXl3b3JkIjoiIiwic3RhdGVzIjpbIkNBIl0sInN0YXR1c2VzIjpbIkZPUl9TQUxFIiwiUEVORElORyIsIkNPTUlOR19TT09OIl19LCJib3VuZHMiOnsibGF0TWluIjozNi44OTMwMzI5OTk5OTk5OTYsImxhdE1heCI6MzcuNDg0NjM3LCJsb25nTWluIjotMTIyLjIwMjY1MywibG9uZ01heCI6LTEyMS4yMDgyMjc5OTk5OTk5OX19&location=santa-clara-county--ca',
    # Alameda County (Oakland)
    'https://zerodown.com/c/search?searchCode=eyJsaW1pdCI6MTgsIm9mZnNldCI6MCwiZmlsdGVycyI6eyJjaXRpZXMiOlsiU2FuIEpvc2UiXSwiaG9tZVR5cGVzIjpbIm11bHRpLWZhbWlseSJdLCJzZW9LZXl3b3JkIjoiIiwic3RhdGVzIjpbIkNBIl0sInN0YXR1c2VzIjpbIkZPUl9TQUxFIiwiUEVORElORyIsIkNPTUlOR19TT09OIl19LCJib3VuZHMiOnsibGF0TWluIjozNy40NTQxODYsImxhdE1heCI6MzcuOTA1ODIzOTk5OTk5OTk2LCJsb25nTWluIjotMTIyLjM0MjI1MywibG9uZ01heCI6LTEyMS40NjkyMTR9fQ%3D%3D&location=alameda-county--ca',
    # Contra Costa County (Richmond) 
    'https://zerodown.com/c/search?searchCode=eyJsaW1pdCI6MTgsIm9mZnNldCI6MCwiZmlsdGVycyI6eyJjaXRpZXMiOlsiU2FuIEpvc2UiXSwiaG9tZVR5cGVzIjpbIm11bHRpLWZhbWlseSJdLCJzZW9LZXl3b3JkIjoiIiwic3RhdGVzIjpbIkNBIl0sInN0YXR1c2VzIjpbIkZPUl9TQUxFIiwiUEVORElORyIsIkNPTUlOR19TT09OIl19LCJib3VuZHMiOnsibGF0TWluIjozNy43MTg2MjksImxhdE1heCI6MzguMDk5ODc4LCJsb25nTWluIjotMTIyLjQzMDA4NywibG9uZ01heCI6LTEyMS41MzQyNDd9fQ%3D%3D&location=contra-costa-county--ca'
)
zerodown_pages = pages_assign(location,
    # Sacramento County (Sacramento)
    4,
    # San Joaquin County (Stockton)
    4,
    # Santa Clara County (San Jose)
    4,
    # Alameda County (Oakland)
    4,
    # Contra Costa County (Richmond) 
    4
)

# proxy settings:
# If this is true, script will use proxies when using request.get() method
ZERODOWN_REQUEST_GET_PROXIES_USE = True
# Which proxy service would you like to use for the request.get() method? Options are:
# 1. 'scrapeops'
# 2. 'oxylabs'
# 3. 'iproyal'
# 4. 'scrapingbee'
ZERODOWN_REQUEST_GET_PROXIES_SERVICE = 'scrapeops'

#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>
#                                         PLAYWRIGHT HEAVY SCRAPERS                                                    
#<><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><>

# SCRAPE VANGUARDPROPEPERTIES.COM ---------------------------------------------------------
scrape_vanguard = True
# Use headless browser?
vanguard_headless = False
vanguard_url =url_assign(location,
    #example link: 'https://vanguardproperties.com/home-search/listings?sortBy=STATUS_CHANGE_TIMESTAMP&sortDirection=DESC&propertyType=%5B%22MULTI_FAMILY%22%2C%22OTHER%22%5D&listingStatus=%5B%22ACTIVE%22%2C%22PENDING%22%2C%22ACTIVE_UNDER_CONTRACT%22%5D&regionId=c7953732-f66d-4c47-98ac-1ae123149b3c&center=%7B%22lat%22%3A37.75871755655042%2C%22lng%22%3A-122.23530789082145%7D&zoom=12&boundary=%5B%5B%5B37.817865570119714%2C-122.33006497089957%5D%2C%5B37.817865570119714%2C-122.14055081074332%5D%2C%5B37.699522212479%2C-122.14055081074332%5D%2C%5B37.699522212479%2C-122.33006497089957%5D%2C%5B37.817865570119714%2C-122.33006497089957%5D%5D%5D&omnibox=Oakland%2C+CA%2C+USA&keyword=&page=1&limit=10&isLease=false'
    # Sacramento County (Sacramento)
    'https://vanguardproperties.com/home-search/listings?sortBy=STATUS_CHANGE_TIMESTAMP&sortDirection=DESC&propertyType=%5B%22MULTI_FAMILY%22%2C%22OTHER%22%5D&listingStatus=%5B%22ACTIVE%22%2C%22PENDING%22%2C%22ACTIVE_UNDER_CONTRACT%22%5D&regionId=79c13477-54cc-4678-baf0-94381cb59d43&center=%7B%22lat%22%3A38.377412953058894%2C%22lng%22%3A-121.44485292685695%7D&zoom=10&boundary=%5B%5B%5B38.61172547460929%2C-121.82388124716945%5D%2C%5B38.61172547460929%2C-121.06582460654445%5D%2C%5B38.14233910042599%2C-121.06582460654445%5D%2C%5B38.14233910042599%2C-121.82388124716945%5D%2C%5B38.61172547460929%2C-121.82388124716945%5D%5D%5D&omnibox=Sacramento+County%2C+CA%2C+USA&keyword=&page=1&limit=10&isLease=false',
    # San Joaquin County (Stockton)
    'https://vanguardproperties.com/home-search/listings?sortBy=STATUS_CHANGE_TIMESTAMP&sortDirection=DESC&propertyType=%5B%22MULTI_FAMILY%22%2C%22OTHER%22%5D&listingStatus=%5B%22ACTIVE%22%2C%22PENDING%22%2C%22ACTIVE_UNDER_CONTRACT%22%5D&regionId=05a63639-4133-47d6-9cba-8c88599ed9be&center=%7B%22lat%22%3A37.89101756390815%2C%22lng%22%3A-121.25282901190715%7D&zoom=10&boundary=%5B%5B%5B38.12690101296094%2C-121.63185733221965%5D%2C%5B38.12690101296094%2C-120.87380069159465%5D%2C%5B37.65437593600586%2C-120.87380069159465%5D%2C%5B37.65437593600586%2C-121.63185733221965%5D%2C%5B38.12690101296094%2C-121.63185733221965%5D%5D%5D&omnibox=San+Joaquin+County%2C+CA%2C+USA&keyword=&page=1&limit=10&isLease=false',
    # Santa Clara County (San Jose)
    'https://vanguardproperties.com/home-search/listings?sortBy=STATUS_CHANGE_TIMESTAMP&sortDirection=DESC&propertyType=%5B%22MULTI_FAMILY%22%2C%22OTHER%22%5D&listingStatus=%5B%22ACTIVE%22%2C%22PENDING%22%2C%22ACTIVE_UNDER_CONTRACT%22%5D&regionId=3787b314-1f4f-43bb-926b-4fa5af11dd99&center=%7B%22lat%22%3A37.18880646879423%2C%22lng%22%3A-121.70541551397945%7D&zoom=10&boundary=%5B%5B%5B37.426928001038085%2C-122.08444383429195%5D%2C%5B37.426928001038085%2C-121.32638719366695%5D%2C%5B36.94993169386424%2C-121.32638719366695%5D%2C%5B36.94993169386424%2C-122.08444383429195%5D%2C%5B37.426928001038085%2C-122.08444383429195%5D%5D%5D&omnibox=Santa+Clara+County%2C+CA%2C+USA&keyword=&page=1&limit=10&isLease=false',
    # Alameda County (Oakland)
    'https://vanguardproperties.com/home-search/listings?sortBy=STATUS_CHANGE_TIMESTAMP&sortDirection=DESC&propertyType=%5B%22MULTI_FAMILY%22%2C%22OTHER%22%5D&listingStatus=%5B%22ACTIVE%22%2C%22PENDING%22%2C%22ACTIVE_UNDER_CONTRACT%22%5D&regionId=39d3413b-0c18-4cab-9a43-1f426f42e5e4&center=%7B%22lat%22%3A37.68000498959205%2C%22lng%22%3A-121.9214979964303%7D&zoom=10&boundary=%5B%5B%5B37.91656469802909%2C-122.30052631674279%5D%2C%5B37.91656469802909%2C-121.54246967611779%5D%2C%5B37.442688537865614%2C-121.54246967611779%5D%2C%5B37.442688537865614%2C-122.30052631674279%5D%2C%5B37.91656469802909%2C-122.30052631674279%5D%5D%5D&omnibox=Alameda+County%2C+CA%2C+USA&keyword=&page=1&limit=10&isLease=false',
    # Contra Costa County (Richmond) 
    'https://vanguardproperties.com/home-search/listings?sortBy=STATUS_CHANGE_TIMESTAMP&sortDirection=DESC&propertyType=%5B%22MULTI_FAMILY%22%2C%22OTHER%22%5D&listingStatus=%5B%22ACTIVE%22%2C%22PENDING%22%2C%22ACTIVE_UNDER_CONTRACT%22%5D&regionId=ad9dee9d-9c65-4369-9b83-878dedbcf3cf&center=%7B%22lat%22%3A37.90920445626534%2C%22lng%22%3A-121.9878429924924%7D&zoom=10&boundary=%5B%5B%5B38.14502947025357%2C-122.3668713128049%5D%2C%5B38.14502947025357%2C-121.6088146721799%5D%2C%5B37.67262114162293%2C-121.6088146721799%5D%2C%5B37.67262114162293%2C-122.3668713128049%5D%2C%5B38.14502947025357%2C-122.3668713128049%5D%5D%5D&omnibox=Contra+Costa+County%2C+CA%2C+USA&keyword=&page=1&limit=10&isLease=false'
)
vanguard_pages = pages_assign(location,
    # Sacramento County (Sacramento)
    2,
    # San Joaquin County (Stockton)
    4,
    # Santa Clara County (San Jose)
    4,
    # Alameda County (Oakland)
    28,
    # Contra Costa County (Richmond) 
    4
)

# proxy settings:
# If this is true, script will use proxies for playwright headless browser 
VANGUARD_PLAYWRIGHT_PROXIES_USE = True
# Which proxy service would you like to use for playwright? Options are:
# 1. 'scrapeops'
# 2. 'oxylabs'
# 3. 'iproyal'
# 4. 'scrapingbee'
VANGUARD_PLAYWRIGHT_PROXIES_SERVICE = 'oxylabs'
# If this is true, script will use useragents for playwright headless browser 
VANGUARD_PLAYWRIGHT_USERAGENTS_USE = True

# If this is true, script will use proxies when using request.get() method
VANGUARD_REQUEST_GET_PROXIES_USE = True
# Which proxy service would you like to use for the request.get() method? Options are:
# 1. 'scrapeops'
# 2. 'oxylabs'
# 3. 'iproyal'
# 4. 'scrapingbee'
VANGUARD_REQUEST_GET_PROXIES_SERVICE = 'scrapeops'

# SCRAPE ZILLOW.COM -----------------------------------------------------------------------
scrape_zillow = True
# Use headless browser?
zillow_headless = False
zillow_url =url_assign(location, 
    #example link: 'https://www.zillow.com/sacramento-ca/duplex/'
    # Sacramento County (Sacramento)
    'https://www.zillow.com/sacramento-county-ca/duplex/',
    # San Joaquin County (Stockton)
    'https://www.zillow.com/san-joaquin-county-ca/duplex/',
    # Santa Clara County (San Jose)
    'https://www.zillow.com/santa-clara-county-ca/duplex/',
    # Alameda County (Oakland)
    'https://www.zillow.com/alameda-county-ca/duplex/',
    # Contra Costa County (Richmond) 
    'https://www.zillow.com/contra-costa-county-ca/duplex/'
)
zillow_pages = pages_assign(location,
    # Sacramento County (Sacramento)
    3,
    # San Joaquin County (Stockton)
    4,
    # Santa Clara County (San Jose)
    4,
    # Alameda County (Oakland)
    6,
    # Contra Costa County (Richmond) 
    4
)

# proxy settings:
# If this is true, script will use proxies for playwright headless browser 
ZILLOW_PLAYWRIGHT_PROXIES_USE = True
# Which proxy service would you like to use for playwright? Options are:
# 1. 'scrapeops'
# 2. 'oxylabs'
# 3. 'iproyal'
# 4. 'scrapingbee'
ZILLOW_PLAYWRIGHT_PROXIES_SERVICE = 'oxylabs'
# If this is true, script will use useragents for playwright headless browser 
ZILLOW_PLAYWRIGHT_USERAGENTS_USE = True

# If this is true, script will use proxies when using request.get() method
ZILLOW_REQUEST_GET_PROXIES_USE = True
# Which proxy service would you like to use for the request.get() method? Options are:
# 1. 'scrapeops'
# 2. 'oxylabs'
# 3. 'iproyal'
# 4. 'scrapingbee'
ZILLOW_REQUEST_GET_PROXIES_SERVICE = 'scrapeops'

# SCRAPE INVESTORLIFT.COM -----------------------------------------------------------------------
scrape_investorlift = True
# Use headless browser?
investorlift_headless = False
investorlift_url = 'https://investorlift.com/properties/california'
investorlift_pages = 1 # infinite scroll

# proxy settings:
# If this is true, script will use proxies for playwright headless browser 
INVESTORLIFT_PLAYWRIGHT_PROXIES_USE = False
# Which proxy service would you like to use for playwright? Options are:
# 1. 'scrapeops'
# 2. 'oxylabs'
# 3. 'iproyal'
# 4. 'scrapingbee'
INVESTORLIFT_PLAYWRIGHT_PROXIES_SERVICE = 'scrapeops'
# If this is true, script will use useragents for playwright headless browser 
INVESTORLIFT_PLAYWRIGHT_USERAGENTS_USE = False

# If this is true, script will use proxies when using request.get() method
INVESTORLIFT_REQUEST_GET_PROXIES_USE = False
# Which proxy service would you like to use for the request.get() method? Options are:
# 1. 'scrapeops'
# 2. 'oxylabs'
# 3. 'iproyal'
# 4. 'scrapingbee'
INVESTORLIFT_REQUEST_GET_PROXIES_SERVICE = 'scrapeops'

# SCRAPE REALTOR.COM -----------------------------------------------------------------------
scrape_realtor = True
# Use headless browser?
realtor_headless = False
realtor_url = url_assign(location,
    # example link: 'https://www.realtor.com/realestateandhomes-search/Sacramento_CA/type-multi-family-home'
    # Sacramento County (Sacramento)
    'https://www.realtor.com/realestateandhomes-search/Sacramento-County_CA/type-multi-family-home',
    # San Joaquin County (Stockton)
    'https://www.realtor.com/realestateandhomes-search/San-Joaquin-County_CA/type-multi-family-home',
    # Santa Clara County (San Jose)
    'https://www.realtor.com/realestateandhomes-search/Santa-Clara-County_CA/type-multi-family-home',
    # Alameda County (Oakland)
    'https://www.realtor.com/realestateandhomes-search/Alameda-County_CA/type-multi-family-home',
    # Contra Costa County (Richmond) 
    'https://www.realtor.com/realestateandhomes-search/Contra-Costa-County_CA/type-multi-family-home'
)

realtor_pages = pages_assign(location,
    # Sacramento County (Sacramento)
    4,
    # San Joaquin County (Stockton)
    4,
    # Santa Clara County (San Jose)
    4,
    # Alameda County (Oakland)
    7,
    # Contra Costa County (Richmond) 
    4
)

# proxy settings:
# If this is true, script will use proxies for playwright headless browser 
REALTOR_PLAYWRIGHT_PROXIES_USE = True
# Which proxy service would you like to use for playwright? Options are:
# 1. 'scrapeops'
# 2. 'oxylabs'
# 3. 'iproyal'
# 4. 'scrapingbee'
REALTOR_PLAYWRIGHT_PROXIES_SERVICE = 'scrapeops'
# If this is true, script will use useragents for playwright headless browser 
REALTOR_PLAYWRIGHT_USERAGENTS_USE = True

# If this is true, script will use proxies when using request.get() method
REALTOR_REQUEST_GET_PROXIES_USE = True
# Which proxy service would you like to use for the request.get() method? Options are:
# 1. 'scrapeops'
# 2. 'oxylabs'
# 3. 'iproyal'
# 4. 'scrapingbee'
REALTOR_REQUEST_GET_PROXIES_SERVICE = 'scrapeops'


# SCRAPE TRULIA.COM -----------------------------------------------------------------------
scrape_trulia = True
# Use headless browser?
trulia_headless = False
trulia_url =url_assign(location,
    # example link: 'https://www.trulia.com/CA/Sacramento/'
    # Sacramento County (Sacramento)
    'https://www.trulia.com/for_sale/06067_c/MULTI-FAMILY_type/',
    # San Joaquin County (Stockton)
    'https://www.trulia.com/for_sale/06077_c/MULTI-FAMILY_type/',
    # Santa Clara County (San Jose)
    'https://www.trulia.com/for_sale/06085_c/MULTI-FAMILY_type/',
    # Alameda County (Oakland)
    'https://www.trulia.com/for_sale/06001_c/MULTI-FAMILY_type/',
    # Contra Costa County (Richmond) 
    'https://www.trulia.com/for_sale/06013_c/MULTI-FAMILY_type/'
)
trulia_pages = pages_assign(location,
    # Sacramento County (Sacramento)
    40,
    # San Joaquin County (Stockton)
    4,
    # Santa Clara County (San Jose)
    4,
    # Alameda County (Oakland)
    6,
    # Contra Costa County (Richmond) 
    4
)

# proxy settings:
# If this is true, script will use proxies for playwright headless browser 
TRULIA_PLAYWRIGHT_PROXIES_USE = True
# Which proxy service would you like to use for playwright? Options are:
# 1. 'scrapeops'
# 2. 'oxylabs'
# 3. 'iproyal'
# 4. 'scrapingbee'
TRULIA_PLAYWRIGHT_PROXIES_SERVICE = 'iproyal'
# If this is true, script will use useragents for playwright headless browser 
TRULIA_PLAYWRIGHT_USERAGENTS_USE = True

# If this is true, script will use proxies when using request.get() method
TRULIA_REQUEST_GET_PROXIES_USE = True
# Which proxy service would you like to use for the request.get() method? Options are:
# 1. 'scrapeops'
# 2. 'oxylabs'
# 3. 'iproyal'
# 4. 'scrapingbee'
TRULIA_REQUEST_GET_PROXIES_SERVICE = 'scrapeops'

# SCRAPE ROCKETHOMES.COM -----------------------------------------------------------------------
scrape_rockethomes = True
# Use headless browser?
rockethomes_headless = False
rockethomes_url = url_assign(location,
    # example link: 'https://www.rockethomes.com/ca/sacramento-county?home-type=multi'
    # Sacramento County (Sacramento)
    'https://www.rockethomes.com/ca/sacramento-county?home-type=multi',
    # San Joaquin County (Stockton)
    'https://www.rockethomes.com/ca/san-joaquin-county?home-type=multi',
    # Santa Clara County (San Jose)
    'https://www.rockethomes.com/ca/santa-clara-county?home-type=multi',
    # Alameda County (Oakland)
    'https://www.rockethomes.com/ca/alameda-county?home-type=multi',
    # Contra Costa County (Richmond) 
    'https://www.rockethomes.com/ca/contra-costa-county?home-type=multi'
)
rockethomes_pages = pages_assign(location,
    # Sacramento County (Sacramento)
    4,
    # San Joaquin County (Stockton)
    4,
    # Santa Clara County (San Jose)
    4,
    # Alameda County (Oakland)
    4,
    # Contra Costa County (Richmond) 
    4
)

# proxy settings:
# If this is true, script will use proxies for playwright headless browser 
ROCKETHOMES_PLAYWRIGHT_PROXIES_USE = False
# Which proxy service would you like to use for playwright? Options are:
# 1. 'scrapeops'
# 2. 'oxylabs'
# 3. 'iproyal'
# 4. 'scrapingbee'
ROCKETHOMES_PLAYWRIGHT_PROXIES_SERVICE = 'scrapeops'
# If this is true, script will use useragents for playwright headless browser 
ROCKETHOMES_PLAYWRIGHT_USERAGENTS_USE = False

# If this is true, script will use proxies when using request.get() method
ROCKETHOMES_REQUEST_GET_PROXIES_USE = True
# Which proxy service would you like to use for the request.get() method? Options are:
# 1. 'scrapeops'
# 2. 'oxylabs'
# 3. 'iproyal'
# 4. 'scrapingbee'
ROCKETHOMES_REQUEST_GET_PROXIES_SERVICE = 'scrapeops'

# SCRAPE FLYHOMES.COM -----------------------------------------------------------------------
scrape_flyhomes = True
# Use headless browser?
flyhomes_headless = False #THIS CANNOT BE TRUE ! - pyautogui in use
flyhomes_url =url_assign(location,
    # example link: 'https://www.flyhomes.com/county/ca/sacramento-county?prop_type=Multi-Family'
    # Sacramento County (Sacramento)
    'https://www.flyhomes.com/county/ca/sacramento-county?prop_type=Multi-Family',
    # San Joaquin County (Stockton)
    'https://www.flyhomes.com/county/ca/san-joaquin-county?prop_type=Multi-Family',
    # Santa Clara County (San Jose)
    'https://www.flyhomes.com/county/ca/santa-clara-county?prop_type=Multi-Family',
    # Alameda County (Oakland)
    'https://www.flyhomes.com/county/ca/alameda-county?prop_type=Multi-Family',
    # Contra Costa County (Richmond) 
    'https://www.flyhomes.com/county/ca/contra-costa-county?prop_type=Multi-Family'
)
flyhomes_pages = pages_assign(location,
    # Sacramento County (Sacramento)
    4,
    # San Joaquin County (Stockton)
    4,
    # Santa Clara County (San Jose)
    4,
    # Alameda County (Oakland)
    6,
    # Contra Costa County (Richmond) 
    4
)

# proxy settings:
# If this is true, script will use proxies for playwright headless browser 
FLYHOMES_PLAYWRIGHT_PROXIES_USE = False
# Which proxy service would you like to use for playwright? Options are:
# 1. 'scrapeops'
# 2. 'oxylabs'
# 3. 'iproyal'
# 4. 'scrapingbee'
FLYHOMES_PLAYWRIGHT_PROXIES_SERVICE = 'scrapeops'
# If this is true, script will use useragents for playwright headless browser 
FLYHOMES_PLAYWRIGHT_USERAGENTS_USE = False

# SCRAPE MOVOTO.COM -----------------------------------------------------------------------
scrape_movoto = True
# Use headless browser?
movoto_headless = False
movoto_url =url_assign(location,
    # example link: 'https://www.movoto.com/sacramento-ca/multi-family/@38.5815719,-121.4943996/'
    # Sacramento County (Sacramento)
    'https://www.movoto.com/sacramento-county-ca/@38.4500114,-121.3404409/',
    # San Joaquin County (Stockton)
    'https://www.movoto.com/san-joaquin-county-ca/multi-family/@37.9350336,-121.2722369/',
    # Santa Clara County (San Jose)
    'https://www.movoto.com/santa-clara-county-ca/multi-family/@37.2207774,-121.6906224/',
    # Alameda County (Oakland)
    'https://www.movoto.com/alameda-county-ca/multi-family/@37.6480811,-121.9133039/',
    # Contra Costa County (Richmond) 
    'https://www.movoto.com/contra-costa-county-ca/multi-family/@37.919479,-121.9515431/'
)
movoto_pages = pages_assign(location,
    # Sacramento County (Sacramento)
    4,
    # San Joaquin County (Stockton)
    4,
    # Santa Clara County (San Jose)
    4,
    # Alameda County (Oakland)
    8,
    # Contra Costa County (Richmond) 
    4
)

# proxy settings:
# If this is true, script will use proxies for playwright headless browser 
MOVOTO_PLAYWRIGHT_PROXIES_USE = True
# Which proxy service would you like to use for playwright? Options are:
# 1. 'scrapeops'
# 2. 'oxylabs'
# 3. 'iproyal'
# 4. 'scrapingbee'
MOVOTO_PLAYWRIGHT_PROXIES_SERVICE = 'scrapingbee'
# If this is true, script will use useragents for playwright headless browser 
MOVOTO_PLAYWRIGHT_USERAGENTS_USE = True
