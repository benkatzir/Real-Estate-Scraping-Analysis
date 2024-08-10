from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import requests
import csv 
import sys
sys.path.append('C:\\Users\\ayele\\realestate\\all_scraper_1.6')
import settings
import wscrape
import hudapi
import time
import proxyservices
import asyncio
import pyautogui

# PLAYWRIGHT HEAVY SCRAPER
# HEADLESS BROWSER MUST BE FALSE!! USES PYAUTOGUI ON FIRST PAGE, AFTER FIRST PAGE YOU CAN MOVE OFF THE WINDOW
# Special scraper for page needing scroll to render html
# Uses asynchronous playwright functions to manipulate page

# Will use proxies for playwright headless browser if True in scraper settings
PLAYWRIGHT_PROXIES_USE = settings.FLYHOMES_PLAYWRIGHT_PROXIES_USE
# Will use proxy service specified in scraper settings for playwright headless browser
PLAYWRIGHT_PROXIES_SERVICE = settings.FLYHOMES_PLAYWRIGHT_PROXIES_SERVICE
# Will use fake useragents for playwright headless browser if True in scraper settings
PLAYWRIGHT_USERAGENTS_USE = settings.FLYHOMES_PLAYWRIGHT_USERAGENTS_USE

# After the page is loaded in chromium browser, this function goes to the website,
#  scrolls to the bottom, gets the html of the page, and then parses it with beatifulsoup4
# If the page was loaded correctly (not blocked), the function will exicute, if not there will be an error and the
# program will try to load the page 2 more times

async def get_individual_listing_data(page, listing_url, csv_writer):
    response = await page.goto(listing_url, timeout= 180000)
    status_code = response.status

    # Locate the element containing the property details
    property_details_div = await page.wait_for_selector('div.css-aq0c2l.css-11zz26w')

    try:
        # Locate the the read more
        p_tag = await property_details_div.wait_for_selector('p.css-1gujn1c')
        # Click on the element
        await p_tag.click()
        time.sleep(3)
        listing_html_text = await page.content()
    except Exception as e:
        time.sleep(3)
        listing_html_text = await page.content()
    
    individual_listing = BeautifulSoup(listing_html_text, 'lxml')

    property_description = wscrape.if_nonetype_str(wscrape.verify_not_nonetype(individual_listing.find('div', class_ = 'css-aq0c2l css-11zz26w'), 'obj.text'))
    
    address = wscrape.if_nonetype_str(wscrape.verify_not_nonetype(individual_listing.find('span', class_='css-1j0ry2j'), 'obj.text')) + wscrape.if_nonetype_str(wscrape.verify_not_nonetype(individual_listing.find('span', class_='css-1rlz2t3'), 'obj.text'))
    purchase_price = wscrape.verify_not_nonetype(individual_listing.find('div', class_='css-154fcil css-rls330'), 'obj.span.text')
    units = wscrape.find_units(property_description, 2)
    county = settings.location_assign(settings.location)
    zip = wscrape.extract_zipcode(address)
    effiency, one_bedroom, two_bedroom, three_bedroom, four_bedroom = await hudapi.async_hud_location_fmrs3(county, zip, settings.DEFAULT_FMR)
    
    csv_writer.writerow([listing_url, address, purchase_price, units, county, zip, effiency, one_bedroom, two_bedroom, three_bedroom, four_bedroom])
    print(f"{listing_url}, {address}, {purchase_price}, {units}, {county}, {zip}, {effiency}, {one_bedroom}, {two_bedroom}, {three_bedroom}, {four_bedroom}")

async def get_flyhomes_data(page, on_page_num, items_scraped, next_page_url, csv_writer):
    
    # Go to page with all the listings
    response = await page.goto(next_page_url)
    status_code = response.status
    
    # There is an anti scraping popup on all listings pages - will have to use pyautogui to exit out of it
    # wait for popup to load
    time.sleep(10)

    #click on the side of the page to exit out of the popup
    pyautogui.click(1500, 460)

    #OR you can click directly on the X element of the popup - Note that these coordinates might change if they change the popup
    #pyautogui.click(1230, 250)

    # Find the element to click using a selector (this is so playwright can start scrolling)
    element_to_click = await page.wait_for_selector('div.css-ufb669')

    # If the element_to_click was found, this means that the website was loaded successfully without
    # being blocked. If page loads successfully, record in csv and print out the page details
    print(f'PAGE {next_page_url}, STATUS CODE {str(status_code)}, FLYHOMES.COM, ITEMS SCRAPED {items_scraped}, PAGE {on_page_num}, PAGE {on_page_num}, PAGE {on_page_num}, PAGE {on_page_num}, PAGE {on_page_num}, PAGE {on_page_num}, PAGE {on_page_num}')
    csv_writer.writerow([f'PAGE {next_page_url}', f'STATUS CODE {str(status_code)}', f'FLYHOMES.COM', f'ITEMS SCRAPED {items_scraped}', f'PAGE {on_page_num}', f'PAGE {on_page_num}', f'PAGE {on_page_num}',f'PAGE {on_page_num}', f'PAGE {on_page_num}', f'PAGE {on_page_num}', f'PAGE {on_page_num}'])
    
    # Click the element
    await element_to_click.click()

    # Scroll to bottom
    await wscrape.scroll_to_bottom(page)
    await page.wait_for_load_state('load')
    
    # Sleep for 5 seconds to ensure all html has been rendered
    time.sleep(5)

    # Start parsing the listings
    html_text = await page.content()
    if html_text is not None:
        soup = BeautifulSoup(html_text, 'lxml')
        listing_url_containers = soup.find_all('a', {'data-testid' : 'search-results-grid-card'})
    
        for listing_url_container in listing_url_containers:
            try:
                if listing_url_container != None:
                    listing_url = "https://www.flyhomes.com" + listing_url_container.get('href')
                    await get_individual_listing_data(page, listing_url, csv_writer)
            except Exception as e:
                csv_writer.writerow(['ERROR REQUESTING LISTING', 'ERROR REQUESTING LISTING', 'ERROR REQUESTING LISTING', 'ERROR REQUESTING LISTING', 'ERROR REQUESTING LISTING', 'ERROR REQUESTING LISTING', 'ERROR REQUESTING LISTING', 'ERROR REQUESTING LISTING', 'ERROR REQUESTING LISTING', 'ERROR REQUESTING LISTING', 'ERROR REQUESTING LISTING'])
                print(f"ERROR REQUESTING LISTING, ERROR REQUESTING LISTING, ERROR REQUESTING LISTING, ERROR REQUESTING LISTING, ERROR REQUESTING LISTING, ERROR REQUESTING LISTING, ERROR REQUESTING LISTING, ERROR REQUESTING LISTING, ERROR REQUESTING LISTING, ERROR REQUESTING LISTING, ERROR REQUESTING LISTING")
                print({e})
            
        items_scraped += 1

# Async function to run the scraper.
async def run_flyhomes_scraper():
    with open('data.csv', 'a', newline='', encoding = 'utf8') as csvfile:
        csv_writer = csv.writer(csvfile)
        print("Url, Address, Purchase Price, Units, County, Zip, Efficiency, One-Bedroom, Two-Bedroom, Three-Bedroom, Four-Bedroom")
        csv_writer.writerow(['Url', 'Address', 'Purchase Price', 'Units', 'County', 'Zip', 'Efficiency', 'One-Bedroom', 'Two-Bedroom', 'Three-Bedroom', 'Four-Bedroom'])

        base_link = settings.flyhomes_url
        next_page_url = base_link

        number_of_pages = settings.flyhomes_pages # how many pages will the program scrape?
        on_page_num = 1 # do not change: this is to record the page currently being scraped
        items_scraped = 0 # do not change
        
        # How many times do you want to try and load the page with playwright before terminating?
        get_page_tries = 3
        tries = 0 # do not change: this is to record the try number when trying to load the page correctly with playwright

        for page in range(number_of_pages):
            async with async_playwright() as p:
                i = 1
                for i in range(get_page_tries):
                    tries +=1
                    try:
                        browser = await p.chromium.launch(headless=settings.flyhomes_headless, proxy= proxyservices.get_service_proxy(PLAYWRIGHT_PROXIES_SERVICE, PLAYWRIGHT_PROXIES_USE), slow_mo=500)
                        page = await browser.new_page(ignore_https_errors=True, user_agent= (proxyservices.get_scrapeops_user_agent() if PLAYWRIGHT_USERAGENTS_USE else None))
                        await get_flyhomes_data(page, on_page_num, items_scraped, next_page_url, csv_writer)
                        break
                    except Exception as e:
                        print(e)
                        await browser.close()
                        for i in range(30, 0, -1):
                            print(f'\rFailed to load page ({str(tries)}/{get_page_tries} tries). Retrying in {i} seconds.\n', end='', flush=True)
                            time.sleep(1)  # Sleep for 1 second
                else:
                    print(f"ERROR LOADING PAGE {str(on_page_num)}, ERROR LOADING PAGE {str(on_page_num)}, ERROR LOADING PAGE {str(on_page_num)}, ERROR LOADING PAGE {str(on_page_num)}, ERROR LOADING PAGE {str(on_page_num)}, ERROR LOADING PAGE {str(on_page_num)}, ERROR LOADING PAGE {str(on_page_num)}, ERROR LOADING PAGE {str(on_page_num)}, ERROR LOADING PAGE {str(on_page_num)}, ERROR LOADING PAGE {str(on_page_num)}, ERROR LOADING PAGE {str(on_page_num)}")
                    csv_writer.writerow([f"ERROR LOADING PAGE {str(on_page_num)}", f"ERROR LOADING PAGE {str(on_page_num)}", f"ERROR LOADING PAGE {str(on_page_num)}", f"ERROR LOADING PAGE {str(on_page_num)}", f"ERROR LOADING PAGE {str(on_page_num)}", f"ERROR LOADING PAGE {str(on_page_num)}", f"ERROR LOADING PAGE {str(on_page_num)}", f"ERROR LOADING PAGE {str(on_page_num)}",f"ERROR LOADING PAGE {str(on_page_num)}", f"ERROR LOADING PAGE {str(on_page_num)}", f"ERROR LOADING PAGE {str(on_page_num)}"])
                    break

            on_page_num += 1
            if on_page_num <= number_of_pages:
                index = base_link.find('prop_type')
                next_page = f"page={str(on_page_num)}&"
                if index != -1:
                    next_page_url = base_link[:index] + f"page={str(on_page_num)}&" + base_link[index:]

# run the run_scraper() function
asyncio.run(run_flyhomes_scraper())