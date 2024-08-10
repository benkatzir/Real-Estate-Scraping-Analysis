
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright
import asyncio
import requests
import settings
import json
import os

# Make requests to the api
# param x url: url to make request to
# param x headers: headers to send in request
# param x verb: type of request
# code_ok: acceptable status code for response (if the response is returned with a diffrent code, the function will return the status code and None for the response)
def make_request(url, params={}, added_headers=None, verb='get', data=None, code_ok=200):
    headers = settings.SECURE_HEADER
    if added_headers is not None:   
        for k in added_headers.keys():
            headers[k] = added_headers[k]                
    try:
        response = None
        if verb == 'post':
            response = requests.post(url,params=params,headers=headers,data=data)
        elif verb == 'put':
            response = requests.put(url,params=params,headers=headers,data=data)
        else:
            response = requests.get(url,params=params,headers=headers,data=data)
        status_code = response.status_code
        if status_code == code_ok:
            json_response = response.json()
            return status_code, json_response
        else:
            return status_code, None   
    except:
        print("ERROR")
        return 400, None

# Retrieves a given a US county's general fmrs from HUD API
# location is a county and must be a string (ex. 'SACRAMENTOCOUNTY')
# param x location: location string used to retrieve official section 8 fmrs (fair market rents)
# param x default_rent: if no fmrs are found for the location, a default_rent (number) is returned
def hud_location_fmrs(location, default_rent):
    if location != None:
        url = f'{settings.HUD_BASE_URL}/statedata/{settings.STATE_CODE}?year={str(settings.FMR_YEAR)}'
        status_code, data = make_request(url)

        # format location
        location = location.upper().replace(" ", "").replace("-", "")

        # format county names you get in data (ex: "Salinas, CA MSA" would be formatted to "SALINASCOUNTY")
        def format_county_name(input_string):
            return input_string.upper().replace(" ", "").replace("-", "")
        
        # if api stadus code is 200, data will be analyzed 
        if status_code == 200:
            for county in data["data"]["counties"]:
                if location == format_county_name(county["county_name"]):
                    efficiency = county["Efficiency"]
                    one_bedroom = county["One-Bedroom"]
                    two_bedroom = county["Two-Bedroom"]
                    three_bedroom = county["Three-Bedroom"]
                    four_bedroom = county["Four-Bedroom"]

                    # Fmrs found for the location
                    print("Fmrs found for the location")
                    return efficiency, one_bedroom, two_bedroom, three_bedroom, four_bedroom
                
            # Location "{location}" is not included in the data (location does not match a formatted county)
            print(f'Location "{location}" is not included in the data (location does not match a formatted county)')
            efficiency = default_rent
            one_bedroom = default_rent
            two_bedroom = default_rent
            three_bedroom = default_rent
            four_bedroom = default_rent
            return efficiency, one_bedroom, two_bedroom, three_bedroom, four_bedroom
        
        else:
        # If status code is not 200, all returned values will be set to default rent
            #print(' Status code is not 200')
            efficiency = default_rent
            one_bedroom = default_rent
            two_bedroom = default_rent
            three_bedroom = default_rent
            four_bedroom = default_rent
            return efficiency, one_bedroom, two_bedroom, three_bedroom, four_bedroom
    else:
    # If location is nonetype, all returned values will be set to default rent
        #print(' location is nonetype')
        efficiency = default_rent
        one_bedroom = default_rent
        two_bedroom = default_rent
        three_bedroom = default_rent
        four_bedroom = default_rent
        return efficiency, one_bedroom, two_bedroom, three_bedroom, four_bedroom

# Retrieves CA zip code fmrs if available, if not available it will return the CA county's fmrs - location and zips MUST BE CALIFORNIA!
# uses the hudfmrsca folder to search for fmrs by zip code
# param x location: location string used to retrieve official section 8 fmrs (fair market rents)
# param x zip: zip code of location
# param x default_rent: if no fmrs are found for the location, a default_rent (number) is returned
def hud_location_fmrs2(location, zip, default_rent):
    if (location != None) or (zip != None):
        # Make all location characters lowercase and remove whitespace and dashes
        location = location.lower().replace(" ", "").replace("-", "")
        hud_folder_path = f'C:\\Users\\ayele\\realestate\\all_scraper_1.6\\hudfmrsca\\hudfmrsca{str(settings.FMR_YEAR)}'
        try:
            # List the files in the specified folder
            files_in_folder = os.listdir(hud_folder_path)

            # Loop through the file names in the folder
            for file_name in files_in_folder:
                # Format name of file (example: santaclaracounty.html ----> santaclaracounty)
                split_parts =file_name.split(".")
                if len(split_parts) > 1:
                    formatted_file_name = split_parts[0]

                # Check if the input CA location (CA county) matches any formatted file name
                if location == formatted_file_name:
                    # If input location matches a CA county with zipcodes, enter the html file and try to find the zip's fmrs if it has any
                    with open(f'C:\\Users\\ayele\\realestate\\all_scraper_1.6\\hudfmrsca\\hudfmrsca{str(settings.FMR_YEAR)}\\{file_name}', 'r', encoding='utf8') as html_file:
                            content = html_file.read()
                            soup = BeautifulSoup(content, 'lxml')

                            # Find the table with the class 'big_table'
                            table = soup.find('table', class_='big_table')

                            # Find and extract the table body
                            tbody = table.find('tbody')
                            rows = tbody.find_all('tr')
                            # Iterate through each row in the table body to check if any row contains the inputted CA zip
                            for row in rows:
                                zip_code = row.find('th').a.text
                                if zip_code == str(zip):
                                    efficiency = row.find_all('td')[0].text
                                    one_bedroom = row.find_all('td')[1].text
                                    two_bedroom = row.find_all('td')[2].text
                                    three_bedroom = row.find_all('td')[3].text
                                    four_bedroom = row.find_all('td')[4].text

                                    # Inputted CA zipcode contains fmr data
                                    # print('Provided zipcode contains fmr data')
                                    return efficiency, one_bedroom, two_bedroom, three_bedroom, four_bedroom
                            # Inputted CA zipcode for inputted CA location does not contain fmr data
                            # print('Inputted CA zipcode for inputted CA location does not contain fmr data')
                            return hud_location_fmrs(location, default_rent)

            # CA location does not have zip fmr data or inputted CA zip is not included in any location data- will get general CA county fmrs from hud_location_fmrs()
            # print('Location does not have zip fmr data or zip is not included in any location data- will get general county fmrs from hud_location_fmrs()')
            return hud_location_fmrs(location, default_rent)
        except FileNotFoundError:
            # Error locating folder
            #print('error locating folder')
            return hud_location_fmrs(location, default_rent)
    else:
        # Either location or zip are nonetype
        # print('Either location or zip are nonetype')
        return hud_location_fmrs(location, default_rent)

# Retrieves settings.STATE_CODE zip code fmrs if available, if not available it will return the setttings.STATE_CODE county's fmrs - location and zips DO NOT HAVE TO BE CALIFORNIA!
# uses playwright to manuever through huduser.gov website
# param x location: location string used to retrieve official section 8 fmrs (fair market rents)
# param x zip: zip code of location
# param x default_rent: if no fmrs are found for the location, a default_rent (number) is returned
def hud_location_fmrs3(location, zip, default_rent):
    # if location and zip isn't nonetype
    if (location != None) or (zip != None):

        # Format location
        location = location.upper().replace(" ", "").replace("-", "")

        # Function to return formatted state from inputted state code (example: "CA" ----> "California - CA")
        def get_state_name(state_code):
            state_mapping = {
                "AL": "Alabama",
                "AK": "Alaska",
                "AZ": "Arizona",
                "AR": "Arkansas",
                "CA": "California",
                "CO": "Colorado",
                "CT": "Connecticut",
                "DE": "Delaware",
                "DC": "District of Columbia",
                "FL": "Florida",
                "GA": "Georgia",
                "HI": "Hawaii",
                "ID": "Idaho",
                "IL": "Illinois",
                "IN": "Indiana",
                "IA": "Iowa",
                "KS": "Kansas",
                "KY": "Kentucky",
                "LA": "Louisiana",
                "ME": "Maine",
                "MD": "Maryland",
                "MA": "Massachusetts",
                "MI": "Michigan",
                "MN": "Minnesota",
                "MS": "Mississippi",
                "MO": "Missouri",
                "MT": "Montana",
                "NE": "Nebraska",
                "NV": "Nevada",
                "NH": "New Hampshire",
                "NJ": "New Jersey",
                "NM": "New Mexico",
                "NY": "New York",
                "NC": "North Carolina",
                "ND": "North Dakota",
                "OH": "Ohio",
                "OK": "Oklahoma",
                "OR": "Oregon",
                "PA": "Pennsylvania",
                "PR": "Puerto Rico",
                "RI": "Rhode Island",
                "SC": "South Carolina",
                "SD": "South Dakota",
                "TN": "Tennessee",
                "TX": "Texas",
                "UT": "Utah",
                "VT": "Vermont",
                "VA": "Virginia",
                "WA": "Washington",
                "WV": "West Virginia",
                "WI": "Wisconsin",
                "WY": "Wyoming",
            }
            
            state_name = state_mapping.get(state_code)
            if state_name is not None:
                return f"{state_name} - {state_code}"
            else:
                return None
        
        # Will close browser when code is finished
        with sync_playwright() as p:
            # browser object
            browser = p.chromium.launch(headless=True, slow_mo=500)
            
            # Page object
            page = browser.new_page()
            
            # Go to page
            page.goto(f'https://www.huduser.gov/portal/datasets/fmr/fmrs/FY{settings.FMR_YEAR}_code/select_geography_sa.odn', timeout= 240000)
            page.wait_for_load_state('load')

            # Select the your settings.STATE_CODE state from options
            page.select_option('select[name=STATES]', label = get_state_name(settings.STATE_CODE))
            page.wait_for_load_state('load')
                        
            # Find the "countyselect" select element by id.
            select_element = page.locator('select[id=countyselect]')

            # Find all county options
            options = select_element.locator('option').all()

            for option in options:
                # Save option text
                option_text = option.text_content()

                # Format option text to compare with location
                formatted_option_text = option_text.upper().replace(" ", "").replace("-", "")
            
                # Remove the ",STATECODE" form the option text
                formatted_option_text = formatted_option_text.split(f',{settings.STATE_CODE}')[0]

                # Select the option if the option text is equal to the location
                if formatted_option_text == location:
                    page.select_option('select[id=countyselect]', label = option_text)
                    
                    # Once option is selected, click the "Next Page..." button
                    page.click('input[name=SubmitButton]')
                    page.wait_for_load_state('load')

                    # Save the html of the new page for parsing
                    html_text = page.content()
                
                    soup = BeautifulSoup(html_text, 'lxml')

                    # Find the table with the class 'big_table'
                    table = soup.find('table', class_='big_table')

                    # Find and extract the table body
                    tbody = table.find('tbody')
                    rows = tbody.find_all('tr')
                    # Iterate through each row in the table body to check if any row contains the inputted zip
                    for row in rows:
                        zip_code = row.find('th').a.text
                        if zip_code == str(zip):
                            efficiency = row.find_all('td')[0].text
                            one_bedroom = row.find_all('td')[1].text
                            two_bedroom = row.find_all('td')[2].text
                            three_bedroom = row.find_all('td')[3].text
                            four_bedroom = row.find_all('td')[4].text

                            # Inputted zipcode contains fmr data
                            #print('Provided zipcode contains fmr data')
                            return efficiency, one_bedroom, two_bedroom, three_bedroom, four_bedroom
                    # Inputted zip is not included in location data- will get general county fmrs from hud_location_fmrs()
                    #print('Inputted zip is not included in location data- will get general county fmrs from hud_location_fmrs()')
                    return hud_location_fmrs(location, default_rent)

            # location does not match options - will try with hud_location_fmrs()
            #print('location does not match options - will try with hud_location_fmrs()')
            return hud_location_fmrs(location, default_rent) 
    else:
        # Either location or zip are nonetype
        #print('Either location or zip are nonetype')
        return hud_location_fmrs(location, default_rent)

# TESTING
#print(hud_location_fmrs3("SANTACLARACOUNTY", 95124, "1100"))
#

# Asynchronous version of hud_location_fmrs3(location, zip, defualt_rent) 
# param x location: location string used to retrieve official section 8 fmrs (fair market rents)
# param x zip: zip code of location
# param x default_rent: if no fmrs are found for the location, a default_rent (number) is returned
async def async_hud_location_fmrs3(location, zip, default_rent):
    # if location and zip isn't nonetype
    if (location != None) or (zip != None):

        # Format location
        location = location.upper().replace(" ", "").replace("-", "")

        # Function to return formatted state from inputted state code (example: "CA" ----> "California - CA")
        def get_state_name(state_code):
            state_mapping = {
                "AL": "Alabama",
                "AK": "Alaska",
                "AZ": "Arizona",
                "AR": "Arkansas",
                "CA": "California",
                "CO": "Colorado",
                "CT": "Connecticut",
                "DE": "Delaware",
                "DC": "District of Columbia",
                "FL": "Florida",
                "GA": "Georgia",
                "HI": "Hawaii",
                "ID": "Idaho",
                "IL": "Illinois",
                "IN": "Indiana",
                "IA": "Iowa",
                "KS": "Kansas",
                "KY": "Kentucky",
                "LA": "Louisiana",
                "ME": "Maine",
                "MD": "Maryland",
                "MA": "Massachusetts",
                "MI": "Michigan",
                "MN": "Minnesota",
                "MS": "Mississippi",
                "MO": "Missouri",
                "MT": "Montana",
                "NE": "Nebraska",
                "NV": "Nevada",
                "NH": "New Hampshire",
                "NJ": "New Jersey",
                "NM": "New Mexico",
                "NY": "New York",
                "NC": "North Carolina",
                "ND": "North Dakota",
                "OH": "Ohio",
                "OK": "Oklahoma",
                "OR": "Oregon",
                "PA": "Pennsylvania",
                "PR": "Puerto Rico",
                "RI": "Rhode Island",
                "SC": "South Carolina",
                "SD": "South Dakota",
                "TN": "Tennessee",
                "TX": "Texas",
                "UT": "Utah",
                "VT": "Vermont",
                "VA": "Virginia",
                "WA": "Washington",
                "WV": "West Virginia",
                "WI": "Wisconsin",
                "WY": "Wyoming",
            }
            
            state_name = state_mapping.get(state_code)
            if state_name is not None:
                return f"{state_name} - {state_code}"
            else:
                return None
        
        # Will close browser when code is finished
        async with async_playwright() as p:
            # browser object
            browser = await p.chromium.launch(headless=True, slow_mo=500)
            
            # Page object
            page = await browser.new_page()
            
            # Go to page
            await page.goto(f'https://www.huduser.gov/portal/datasets/fmr/fmrs/FY{settings.FMR_YEAR}_code/select_geography_sa.odn', timeout= 240000)
            await page.wait_for_load_state('load')

            # Select the your settings.STATE_CODE state from options
            await page.select_option('select[name=STATES]', label = get_state_name(settings.STATE_CODE))
            await page.wait_for_load_state('load')
                        
            # Find the "countyselect" select element by id.
            #select_element = page.wait_for_selector('select[id=countyselect]')

            # Find the "countyselect" select element by id.
            countyselect_selector = 'select[id=countyselect]'

            # Wait for the element to appear.
            select_element = await page.wait_for_selector('select[id=countyselect]')

            # Get the textContent of all option elements within the select.
            options = await select_element.evaluate('(element) => Array.from(element.querySelectorAll("option"), option => option.textContent)')

            # Now 'options' contains the text content of all option elements.
            for option in options:
                formatted_option_text = option.upper().replace(" ", "").replace("-","")
            
                # Remove the ",STATECODE" form the option text
                formatted_option_text = formatted_option_text.split(f',{settings.STATE_CODE}')[0]

                # Select the option if the option text is equal to the location
                if formatted_option_text == location:
                    await page.select_option('select[id=countyselect]', label = option)
                    
                    # Once option is selected, click the "Next Page..." button
                    await page.click('input[name=SubmitButton]')
                    await page.wait_for_load_state('load')

                    # Save the html of the new page for parsing
                    html_text = await page.content()
                
                    soup = BeautifulSoup(html_text, 'lxml')

                    # Find the table with the class 'big_table'
                    table = soup.find('table', class_='big_table')

                    # Find and extract the table body
                    tbody = table.find('tbody')
                    rows = tbody.find_all('tr')
                    # Iterate through each row in the table body to check if any row contains the inputted zip
                    for row in rows:
                        zip_code = row.find('th').a.text
                        if zip_code == str(zip):
                            efficiency = row.find_all('td')[0].text
                            one_bedroom = row.find_all('td')[1].text
                            two_bedroom = row.find_all('td')[2].text
                            three_bedroom = row.find_all('td')[3].text
                            four_bedroom = row.find_all('td')[4].text

                            # Inputted zipcode contains fmr data
                            #print('Provided zipcode contains fmr data')
                            #print(efficiency)
                            return efficiency, one_bedroom, two_bedroom, three_bedroom, four_bedroom
                    # Inputted zip is not included in location data- will get general county fmrs from hud_location_fmrs()
                    #print('Inputted zip is not included in location data- will get general county fmrs from hud_location_fmrs()')
                    return hud_location_fmrs(location, default_rent)

            # location does not match options - will try with hud_location_fmrs()
            #print('location does not match options - will try with hud_location_fmrs()')             
            return hud_location_fmrs(location, default_rent)
        
    else:
        # Either location or zip are nonetype
        #print('Either location or zip are nonetype')
        return hud_location_fmrs(location, default_rent)