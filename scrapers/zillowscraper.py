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

# PLAYWRIGHT HEAVY SCRAPER
# Special scraper for page needing scroll to render html
# Uses asynchronous playwright functions to manipulate page

# Will use proxies for playwright headless browser if True in scraper settings
PLAYWRIGHT_PROXIES_USE = settings.ZILLOW_PLAYWRIGHT_PROXIES_USE
# Will use proxy service specified in scraper settings for playwright headless browser
PLAYWRIGHT_PROXIES_SERVICE = settings.ZILLOW_PLAYWRIGHT_PROXIES_SERVICE
# Will use fake useragents for playwright headless browser if True in scraper settings
PLAYWRIGHT_USERAGENTS_USE = settings.ZILLOW_PLAYWRIGHT_USERAGENTS_USE

# If this is true, script will use proxies when using request.get() method - proxyservices.service_proxy_request()
REQUEST_GET_PROXIES_USE = settings.ZILLOW_REQUEST_GET_PROXIES_USE
# Will use proxy service specified in scraper settings for request.get() method
REQUEST_GET_PROXIES_SERVICE = settings.ZILLOW_REQUEST_GET_PROXIES_SERVICE


# After the page is loaded in chromium browser, this function goes to the website,
#  scrolls to the bottom, gets the html of the page, and then parses it with beatifulsoup4
# If the page was loaded correctly (not blocked), the function will exicute, if not there will be an error and the
# program will try to load the page 2 more times
async def get_zillow_data(page, on_page_num, items_scraped, next_page_url, csv_writer):
    
    # Go to page with all the listings
    response = await page.goto(next_page_url, timeout = 240000)
    status_code = response.status
    
    # Find the element to click using a selector (this is so playwright can start scrolling)
    element_to_click = await page.wait_for_selector('div.result-list-container')

    # If the element_to_click was found, this means that the website was loaded successfully without
    # being blocked. If page loads successfully, record in csv and print out the page details
    print(f'PAGE {next_page_url}, STATUS CODE {str(status_code)}, ZILLOW.COM, ITEMS SCRAPED {items_scraped}, PAGE {on_page_num}, PAGE {on_page_num}, PAGE {on_page_num}, PAGE {on_page_num}, PAGE {on_page_num}, PAGE {on_page_num}, PAGE {on_page_num}')
    csv_writer.writerow([f'PAGE {next_page_url}', f'STATUS CODE {str(status_code)}', f'ZILLOW.COM', f'ITEMS SCRAPED {items_scraped}', f'PAGE {on_page_num}', f'PAGE {on_page_num}', f'PAGE {on_page_num}',f'PAGE {on_page_num}', f'PAGE {on_page_num}', f'PAGE {on_page_num}', f'PAGE {on_page_num}'])
    
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
        listing_url_containers = soup.find_all('a', class_ = 'StyledPropertyCardDataArea-c11n-8-84-3__sc-yipmu-0 jnnxAW property-card-link')
    
        for listing_url_container in listing_url_containers:
            try:
                if listing_url_container != None:
                    listing_url = listing_url_container.get('href')
                    listing_html_text = proxyservices.service_proxy_request(listing_url, REQUEST_GET_PROXIES_SERVICE, REQUEST_GET_PROXIES_USE).text
                    individual_listing = BeautifulSoup(listing_html_text, 'lxml')                                    
                    property_description = wscrape.verify_not_nonetype(individual_listing.find('div', class_='Text-c11n-8-84-3__sc-aiai24-0 sc-cZFQFd hrfydd halcbu'), "obj.text")

                    address = wscrape.verify_not_nonetype(individual_listing.find('h1', class_ = 'Text-c11n-8-84-3__sc-aiai24-0 hrfydd'), "obj.text")
                    purchase_price = wscrape.verify_not_nonetype(individual_listing.find('span', {'data-testid' : 'price'}), "obj.span.text")
                    units = wscrape.find_units(property_description, 2)
                    county = settings.location_assign(settings.location)
                    zip = wscrape.extract_zipcode(address)
                    effiency, one_bedroom, two_bedroom, three_bedroom, four_bedroom = await hudapi.async_hud_location_fmrs3(county, zip, settings.DEFAULT_FMR)


                    csv_writer.writerow([listing_url, address, purchase_price, units, county, zip, effiency, one_bedroom, two_bedroom, three_bedroom, four_bedroom])
                    print(f"{listing_url}, {address}, {purchase_price}, {units}, {county}, {zip}, {effiency}, {one_bedroom}, {two_bedroom}, {three_bedroom}, {four_bedroom}")
            except Exception as e:
                csv_writer.writerow(['ERROR REQUESTING LISTING', 'ERROR REQUESTING LISTING', 'ERROR REQUESTING LISTING', 'ERROR REQUESTING LISTING', 'ERROR REQUESTING LISTING', 'ERROR REQUESTING LISTING', 'ERROR REQUESTING LISTING', 'ERROR REQUESTING LISTING', 'ERROR REQUESTING LISTING', 'ERROR REQUESTING LISTING', 'ERROR REQUESTING LISTING'])
                print(f"ERROR REQUESTING LISTING, ERROR REQUESTING LISTING, ERROR REQUESTING LISTING, ERROR REQUESTING LISTING, ERROR REQUESTING LISTING, ERROR REQUESTING LISTING, ERROR REQUESTING LISTING, ERROR REQUESTING LISTING, ERROR REQUESTING LISTING, ERROR REQUESTING LISTING, ERROR REQUESTING LISTING")
                print({e})
            
            items_scraped += 1

# Async function to run the scraper.
async def run_zillow_scraper():
    with open('data.csv', 'a', newline='', encoding = 'utf8') as csvfile:
        csv_writer = csv.writer(csvfile)
        print("Url, Address, Purchase Price, Units, County, Zip, Efficiency, One-Bedroom, Two-Bedroom, Three-Bedroom, Four-Bedroom")
        csv_writer.writerow(['Url', 'Address', 'Purchase Price', 'Units', 'County', 'Zip', 'Efficiency', 'One-Bedroom', 'Two-Bedroom', 'Three-Bedroom', 'Four-Bedroom'])

        base_link = settings.zillow_url
        next_page_url = base_link

        number_of_pages = settings.zillow_pages # how many pages will the program scrape?
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
                        browser = await p.chromium.launch(headless=settings.zillow_headless, proxy= proxyservices.get_service_proxy(PLAYWRIGHT_PROXIES_SERVICE, PLAYWRIGHT_PROXIES_USE), slow_mo=500)
                        page = await browser.new_page(ignore_https_errors=True, user_agent= (proxyservices.get_scrapeops_user_agent() if PLAYWRIGHT_USERAGENTS_USE else None))
                        await get_zillow_data(page, on_page_num, items_scraped, next_page_url, csv_writer)
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
                next_page = f"{str(on_page_num)}_p/"
                next_page_url = base_link + next_page

# run the run_scraper() function
asyncio.run(run_zillow_scraper())