from bs4 import BeautifulSoup
import re
import requests
from random import randint
from urllib.parse import urlencode
import settings
import io
from PIL import Image
import numpy as np
import time

# find the number of units from a property description string, if not found default number is returned
# param x description: string description of a property
# param x default: number to return if number of units is not found from property description
# returns string number representing the number of units
def find_units(description, default):

    # Check for value in input
    if description == None:
        return default # if no description to search for units return the default units specified
    
    # Capitalize the input before working
    input_string = description.upper()

    # Check if function has found units
    #found_units= False

    # Property subtypes
    single_subtype = ['SINGLEFAMILY', 'SINGLE-FAMILY', 'SINGLE FAMILY']
    duplex_subtype = ['DUPLEX', 'DU-PLEX', 'DU PLEX', '2PLEX', '2-PLEX', '2 PLEX', 'TWOPLEX', 'TWO-PLEX', 'TWO PLEX', 'HALFPLEX', 'HALF-PLEX', 'HALF PLEX', 'HPLEX', 'H-PLEX', 'H PLEX', '1/2PLEX', '1/2-PLEX', '1/2 PLEX']
    triplex_subtype = ['TRIPLEX', 'TRI-PLEX', 'TRI PLEX', '3PLEX', '3-PLEX', '3 PLEX', 'THREEPLEX', 'THREE-PLEX', 'THREE PLEX']
    quadplex_subtype = ['QUADPLEX, QUAD-PLEX, QUAD PLEX', 'QUADRUPLEX', 'QUADRU-PLEX', 'QUADRU PLEX', '4PLEX', '4-PLEX', '4 PLEX', 'FOURPLEX', 'FOUR-PLEX', 'FOUR PLEX']
    fiveplex_subtype =['5PLEX', '5-PLEX', '5 PLEX', 'FIVEPLEX', 'FIVE-PLEX', 'FIVE PLEX']
    
    # Check if any of the property subtypes are mentioned in description
    i=0
    for i in range(len(single_subtype)):
        if (single_subtype[i] in input_string): #and found_units==False:
            return 1
    for i in range(len(duplex_subtype)):
        if (duplex_subtype[i] in input_string):# and found_units==False:
            return 2
    for i in range(len(triplex_subtype)):
        if (triplex_subtype[i] in input_string):# and found_units==False:
            return 3
    for i in range(len(quadplex_subtype)):
        if (quadplex_subtype[i] in input_string):# and found_units==False:
            return 4
    for i in range(len(fiveplex_subtype)):
        if (fiveplex_subtype[i] in input_string):# and found_units==False:
            return 5

    numbers = ['20', '19', '18', '17', '16', '15', '14', '13', '12', '11', '10', '9', '8', '7', '6', '5', '4', '3', '2', '1']

    # Check for mentions of multiple units (1-20)
    number_units = ['20 UNIT', '19 UNIT', '18 UNIT', '17 UNIT', '16 UNIT', '15 UNIT', '14 UNIT', '13 UNIT', '12 UNIT', '11 UNIT', '10 UNIT', '9 UNIT', '8 UNIT', '7 UNIT', '6 UNIT', '5 UNIT', '4 UNIT', '3 UNIT', '2 UNIT', '1 UNIT']
    number_units_dashed = ['20-UNIT', '19-UNIT', '18-UNIT', '17-UNIT', '16-UNIT', '15-UNIT', '14-UNIT', '13-UNIT', '12-UNIT', '11-UNIT', '10-UNIT', '9-UNIT', '8-UNIT', '7-UNIT', '6-UNIT', '5-UNIT', '4-UNIT', '3-UNIT', '2-UNIT', '1-UNIT']
    written_units = ['TWENTY UNIT', 'NINETEEN UNIT', 'EIGHTEEN UNIT', 'SEVENTEEN UNIT', 'SIXTEEN UNIT', 'FIFTEEN UNIT', 'FOURTEEN UNIT', 'THIRTEEN UNIT', 'TWELVE UNIT', 'ELEVEN UNIT', 'TEN UNIT', 'NINE UNIT', 'EIGHT UNIT', 'SEVEN UNIT', 'SIX UNIT', 'FIVE UNIT', 'FOUR UNIT', 'THREE UNIT', 'TWO UNIT', 'ONE UNIT']
    written_units_dashed = ['TWENTY-UNIT', 'NINETEEN-UNIT', 'EIGHTEEN-UNIT', 'SEVENTEEN-UNIT', 'SIXTEEN-UNIT', 'FIFTEEN-UNIT', 'FOURTEEN-UNIT', 'THIRTEEN-UNIT', 'TWELVE-UNIT', 'ELEVEN-UNIT', 'TEN-UNIT', 'NINE-UNIT', 'EIGHT-UNIT', 'SEVEN-UNIT', 'SIX-UNIT', 'FIVE-UNIT', 'FOUR-UNIT', 'THREE-UNIT', 'TWO-UNIT', 'ONE-UNIT']
    for i in range(len(numbers)):
        if (number_units[i] in input_string) or (number_units_dashed[i] in input_string) or (written_units[i] in input_string) or (written_units_dashed[i] in input_string):
            return numbers[i]


    # Check for mentions of multiple homes (1-20)
    number_homes = ['20 HOME', '19 HOME', '18 HOME', '17 HOME', '16 HOME', '15 HOME', '14 HOME', '13 HOME', '12 HOME', '11 HOME', '10 HOME', '9 HOME', '8 HOME', '7 HOME', '6 HOME', '5 HOME', '4 HOME', '3 HOME', '2 HOME', '1 HOME']
    number_homes_dashed = ['20-HOME', '19-HOME', '18-HOME', '17-HOME', '16-HOME', '15-HOME', '14-HOME', '13-HOME', '12-HOME', '11-HOME', '10-HOME', '9-HOME', '8-HOME', '7-HOME', '6-HOME', '5-HOME', '4-HOME', '3-HOME', '2-HOME', '1-HOME']
    written_homes = ['TWENTY HOME', 'NINETEEN HOME', 'EIGHTEEN HOME', 'SEVENTEEN HOME', 'SIXTEEN HOME', 'FIFTEEN HOME', 'FOURTEEN HOME', 'THIRTEEN HOME', 'TWELVE HOME', 'ELEVEN HOME', 'TEN HOME', 'NINE HOME', 'EIGHT HOME', 'SEVEN HOME', 'SIX HOME', 'FIVE HOME', 'FOUR HOME', 'THREE HOME', 'TWO HOME', 'ONE HOME']
    written_homes_dashed = ['TWENTY-HOME', 'NINETEEN-HOME', 'EIGHTEEN-HOME', 'SEVENTEEN-HOME', 'SIXTEEN-HOME', 'FIFTEEN-HOME', 'FOURTEEN-HOME', 'THIRTEEN-HOME', 'TWELVE-HOME', 'ELEVEN-HOME', 'TEN-HOME', 'NINE-HOME', 'EIGHT-HOME', 'SEVEN-HOME', 'SIX-HOME', 'FIVE-HOME', 'FOUR-HOME', 'THREE-HOME', 'TWO-HOME', 'ONE-HOME']
    for i in range(len(numbers)):
        if (number_homes[i] in input_string) or (number_homes_dashed[i] in input_string) or (written_homes[i] in input_string) or (written_homes_dashed[i] in input_string):
            return numbers[i]

    # Check for mentions of multiple apartments (1-20)
    number_apartments = ['20 APARTMENT', '19 APARTMENT', '18 APARTMENT', '17 APARTMENT', '16 APARTMENT', '15 APARTMENT', '14 APARTMENT', '13 APARTMENT', '12 APARTMENT', '11 APARTMENT', '10 APARTMENT', '9 APARTMENT', '8 APARTMENT', '7 APARTMENT', '6 APARTMENT', '5 APARTMENT', '4 APARTMENT', '3 APARTMENT', '2 APARTMENT', '1 APARTMENT']
    number_apartments_dashed = ['20-APARTMENT', '19-APARTMENT', '18-APARTMENT', '17-APARTMENT', '16-APARTMENT', '15-APARTMENT', '14-APARTMENT', '13-APARTMENT', '12-APARTMENT', '11-APARTMENT', '10-APARTMENT', '9-APARTMENT', '8-APARTMENT', '7-APARTMENT', '6-APARTMENT', '5-APARTMENT', '4-APARTMENT', '3-APARTMENT', '2-APARTMENT', '1-APARTMENT']
    written_apartments = ['TWENTY APARTMENT', 'NINETEEN APARTMENT', 'EIGHTEEN APARTMENT', 'SEVENTEEN APARTMENT', 'SIXTEEN APARTMENT', 'FIFTEEN APARTMENT', 'FOURTEEN APARTMENT', 'THIRTEEN APARTMENT', 'TWELVE APARTMENT', 'ELEVEN APARTMENT', 'TEN APARTMENT', 'NINE APARTMENT', 'EIGHT APARTMENT', 'SEVEN APARTMENT', 'SIX APARTMENT', 'FIVE APARTMENT', 'FOUR APARTMENT', 'THREE APARTMENT', 'TWO APARTMENT', 'ONE APARTMENT']
    written_apartments_dashed = ['TWENTY-APARTMENT', 'NINETEEN-APARTMENT', 'EIGHTEEN-APARTMENT', 'SEVENTEEN-APARTMENT', 'SIXTEEN-APARTMENT', 'FIFTEEN-APARTMENT', 'FOURTEEN-APARTMENT', 'THIRTEEN-APARTMENT', 'TWELVE-APARTMENT', 'ELEVEN-APARTMENT', 'TEN-APARTMENT', 'NINE-APARTMENT', 'EIGHT-APARTMENT', 'SEVEN-APARTMENT', 'SIX-APARTMENT', 'FIVE-APARTMENT', 'FOUR-APARTMENT', 'THREE-APARTMENT', 'TWO-APARTMENT', 'ONE-APARTMENT']
    for i in range(len(numbers)):
        if (number_apartments[i] in input_string) or (number_apartments_dashed[i] in input_string) or (written_apartments[i] in input_string) or (written_apartments_dashed[i] in input_string):
            return numbers[i]


    # Check for mentions of one unit, home, appartment, townhouse, or condo
    unit = " UNIT"
    if unit in input_string:
        return 1    
    home = " HOME"
    if home in input_string:
        return 1    
    apartment = "APARTMENT"
    if apartment in input_string:
        return 1    
    townhouse = ["TOWNHOUSE", "TOWN-HOUSE", "TOWN HOUSE", "TOWNHOME", "TOWN-HOME", "TOWN HOME"]
    for i in range(len(townhouse)):
        if townhouse[i] in input_string:
            return 1        
    condo = [" CONDO", "CONDOMINIUM"]
    for i in range(len(condo)):
        if condo[i] in input_string:
            return 1

    return default # if number of units hasn't been found

# Will return nonetype if object.attribute is an error or nonetype
# param x obj: the object with no attribute (ex: soup.find('div', class_ = 'listing-panel))
# param x attribute_str: the attribute appended to the object (example 'obj.a.text') - optional parameter
def verify_not_nonetype(obj, attribute_str=None):
    if obj != None:
        try:
            if attribute_str == None:
                return obj
            else:
                return eval(attribute_str, {"obj": obj})
        except Exception as e:
            return None
    else:
        return None
# example usage: verify_not_nonetype(listing_container, "obj.span.text")
# example usage: verify_not_nonetype(soup.find('a', class_ = 'redirect-to-listing'), 'obj.span[1].text')
# example usage: verify_not_nonetype(individual_listing.find('span', class_='Property-description-grid'), "obj[1].a.get('href')")

# replace nonetype value with a replacement value
def replace_if_nonetype(value, replacement):
    if value == None:
        return replacement
    else:
        return value

# Convert nonetype to string
# param x value: string or nonetype taken by the function
def if_nonetype_str(value):
    if value == None:
        return ''
    else:
        return value

# Remove all whitespace and newlines in a string    
# param x input_string: string to remove whitespace and newlines from
def remove_ws_nl(input_string):
    try:
        # Use regular expressions to replace all whitespace and newline characters with an empty string
        return re.sub(r'\s+', '', input_string)
    except Exception as e:
        return None

# get zipcode from address string
# param x address: address string extracted from html
def extract_zipcode(address):
    try:
        if address != None:
            # Define a regular expression pattern to match ZIP codes in various formats
            zip_pattern = r'\b[a-z]{2}\d{5}\b|\b\d{5}(?:-\d{4})?\b'

            # Remove all whitespaces and convert the address to lowercase
            address = ''.join(address.split()).lower()

            # Search for the ZIP code in the address using the pattern
            match = re.search(zip_pattern, address)

            # If a match is found, return the ZIP code; otherwise, return None
            if match:
                    # Use a regular expression to replace non-digit and non-dash characters with an empty string
                    return re.sub(r'[^0-9-]', '', match.group())
            else:
                return None
        else:
            return None
    except Exception as e:
        #print({e})
        return None


# PLAYWRIGHT HEAVY SCRAPER FUNCTIONS-----------------------------------------------------------------------------------

# Function to scroll to end of the page (determines if you are at the end by getting screenshot of page before the scroll and comparing it with screenshot after the scroll)
# utilizes pillow (for screenshots) and playwright libraries (scrolling)
# PLAYWRIGHT BROWSER CANNOT BE MINIMIZED TO TASKBAR - PLAYWRIGHT 
# BROWSER WINDOW MUST BE OPEN BUT YOU CAN BE ON A DIFFERENT WINDOW AT THE SAME TIME
# param x page: playwright page object
async def scroll_to_bottom(page):
    previous_mean = 0
    print('SCROLLING THE PAGE')
    while True:
        # Take the initial screenshot
        initial_screenshot_buffer = await page.screenshot()
        initial_screenshot = Image.open(io.BytesIO(initial_screenshot_buffer))
        initial_screenshot_array = np.array(initial_screenshot)

        # Scroll down
        await page.keyboard.down('ArrowDown')
        await page.keyboard.down('ArrowDown')
        time.sleep(3)

        # Capture a new screenshot
        new_screenshot_buffer = await page.screenshot()
        new_screenshot = Image.open(io.BytesIO(new_screenshot_buffer))
        new_screenshot_array = np.array(new_screenshot)

        # Calculate the absolute difference between the initial and new screenshots
        diff = np.abs(new_screenshot_array - initial_screenshot_array)

        # If the mean difference is 0 the page has reached the end
        print(f'previous mean: {previous_mean}')
        print(f'mean: {np.mean(diff)}')
        if np.mean(diff) == 0 or np.mean(diff) == previous_mean:
            break
        previous_mean = np.mean(diff)
    print('DONE SCROLLING THE PAGE')

# scrolls page faster on movoto individual listing
# param x page: playwright page object
async def movoto_scroll_individual_listing(page):
    # Scroll down
    for _ in range(8):
        await page.keyboard.down('ArrowDown')
        await page.keyboard.down('ArrowDown')
        await page.keyboard.down('ArrowDown')
        await page.keyboard.down('ArrowDown')

# find the number of units listed under the "# Of Units Total" span element on movoto individual listing pages
# param x individual_listing: beatifulsoup object for individual listing page
# returns # of units total listed on movoto.com page
def movoto_number_of_units_total(individual_listing):
    def format_text(input_string):
        return input_string.upper().replace(" ", "").replace("-","")

    span_elements =individual_listing.find_all('span')

    for span_element in span_elements:
        formatted_span_text = format_text(if_nonetype_str(verify_not_nonetype(span_element, 'obj.text')))
        if "#OFUNITSTOTAL" in formatted_span_text:
            number_of_units_total = verify_not_nonetype(span_element, "obj.find_next('b').text")
            return number_of_units_total
    else:
        return None
           
# Find if the phrase "comparables" or anything similar to that is in the input string
# param x input_string: input_string should be text from an html tag
# returns True if tag contains the text "comparables" or a similar phrase
def investorlift_comps_tag(input_string):
    phrases_for_comparables = ['COMPARABLE', 'SALESCOMP', 'COMPS', 'SALECOMP']

    i = 0
    for i in range(len(phrases_for_comparables)):
        if (phrases_for_comparables[i] in input_string): #and found_units==False:
            return True
    else:
        return False

# use the investorlift_comps_tage(input_string) function to loop through the
# text in all the tags in the selector containing property description info and return
# all the text from all the tags until a tag containing the text "comparables" or a similar phrase found
# takes a soup object for an html tag and returns the property description from text in other tags under the inputted tag
# param x obj: soup object
# param x attribute_str: optional, specific sub tag where the releavant html content is under
def investorlift_property_description_text_getter(obj, attribute_str = None):
    try:
        # Find the element that contains all the tags with the text
        if attribute_str == None:
            element = obj
        else:
            element = eval(attribute_str, {"obj": obj})
    

        # Initialize an empty string to store the extracted text
        all_text = ''

        # Iterate through all HTML tags within the element
        for tag in element.descendants:
            if tag.name:
                # Check if the tag contains a "comparables" phrase and cut off the loop if true
                if investorlift_comps_tag(tag.get_text().upper().replace("-", " ")):
                    break  # Exit the loop if the text is found
                all_text += tag.get_text() + ' '

        # Remove extra whitespaces and print the result
        all_text = ' '.join(all_text.split())
        return all_text
    except Exception as e:
        return None

# get all text under an html tag into one string
# takes a soup object for an html tag and returns the property description from text in other tags under the inputted tag
# param x obj: soup object
# param x attribute_str: optional, specific sub tag where the releavant html content is under
def get_all_text_under_tag(obj, attribute_str=None):
    try:
        # Find the element you want to extract all text from
        if attribute_str == None:
            element = obj
        else:
            element = eval(attribute_str, {"obj": obj})

        # Initialize an empty string to store the extracted text
        all_text = ''

        # Iterate through all HTML tags within the element
        for tag in element.descendants:
            if tag.name:
                all_text += tag.get_text() + ' '

        # Remove extra whitespaces and print the result
        all_text = ' '.join(all_text.split())
        return all_text
    except Exception as e:
        #print({e})
        return None
