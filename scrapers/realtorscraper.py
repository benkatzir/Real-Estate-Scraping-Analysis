from playwright.async_api import async_playwright
import asyncio
from bs4 import BeautifulSoup
import requests
import csv 
import sys
sys.path.append('C:\\Users\\ayele\\realestate\\all_scraper_1.6')
import settings
import wscrape
import hudapi
import proxyservices
import time

# PLAYWRIGHT HEAVY SCRAPER
# Special scraper for page needing scroll to render html
# Uses asynchronous playwright functions to manipulate page

# Will use proxies for playwright headless browser if True in scraper settings
PLAYWRIGHT_PROXIES_USE = settings.REALTOR_PLAYWRIGHT_PROXIES_USE
# Will use proxy service specified in scraper settings for playwright headless browser
PLAYWRIGHT_PROXIES_SERVICE = settings.REALTOR_PLAYWRIGHT_PROXIES_SERVICE
# Will use fake useragents for playwright headless browser if True in scraper settings
PLAYWRIGHT_USERAGENTS_USE = settings.REALTOR_PLAYWRIGHT_USERAGENTS_USE

# If this is true, script will use proxies when using request.get() method - proxyservices.service_proxy_request()
REQUEST_GET_PROXIES_USE = settings.REALTOR_REQUEST_GET_PROXIES_USE
# Will use proxy service specified in scraper settings for request.get() method
REQUEST_GET_PROXIES_SERVICE = settings.REALTOR_REQUEST_GET_PROXIES_SERVICE

async def get_realtor_data(page, listing_url, csv_writer):
    response = await page.goto(listing_url, timeout= 180000)
    status_code = response.status

    # Locate the outer <div> with the id "Property Details"
    property_details_div = await page.wait_for_selector('div[id="Property Details"]')

    # Locate the <div> with class "chevron-status-wrapper" within "Property Details"
    chevron_status_div = await property_details_div.wait_for_selector('div.chevron-status-wrapper')

    # Click on the element
    await chevron_status_div.click()
    time.sleep(3)
    listing_html_text = await page.content()
    individual_listing = BeautifulSoup(listing_html_text, 'lxml')

    property_description = wscrape.if_nonetype_str(wscrape.verify_not_nonetype(individual_listing.find('p', class_ = 'LDPPropertyDetailsstyles__StyledParagraph-sc-kcy9ll-8 gnQdBG'), 'obj.text')) + wscrape.if_nonetype_str(wscrape.verify_not_nonetype(individual_listing.find('span', class_ = 'LDPPropertyDetailsstyles__HiddenDescription-sc-kcy9ll-6 DTScl'), 'obj.text'))
    
    address = wscrape.verify_not_nonetype(individual_listing.find('h1', class_='LDPHomeFactsstyles__H1-sc-11rfkby-3 ibiqDI'), 'obj.text')
    purchase_price = wscrape.verify_not_nonetype(individual_listing.find('div', class_ = 'Pricestyles__StyledPrice-rui__btk3ge-0 bvgLFe LDPListPricestyles__StyledPrice-sc-1m24xh0-1 jyBxDQ'), 'obj.text')
    units = wscrape.find_units(property_description, 2)
    county = settings.location_assign(settings.location)
    zip = wscrape.extract_zipcode(address)
    effiency, one_bedroom, two_bedroom, three_bedroom, four_bedroom = await hudapi.async_hud_location_fmrs3(county, zip, settings.DEFAULT_FMR)

    csv_writer.writerow([listing_url, address, purchase_price, units, county, zip, effiency, one_bedroom, two_bedroom, three_bedroom, four_bedroom])
    print(f"{listing_url}, {address}, {purchase_price}, {units}, {county}, {zip}, {effiency}, {one_bedroom}, {two_bedroom}, {three_bedroom}, {four_bedroom}")


async def run_realtor_scraper():
    with open('data.csv', 'a', newline='', encoding = 'utf8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Url', 'Address', 'Purchase Price', 'Units', 'County', 'Zip', 'Efficiency', 'One-Bedroom', 'Two-Bedroom', 'Three-Bedroom', 'Four-Bedroom'])

        base_link = settings.realtor_url
        next_page_url = base_link
        next_page_request = proxyservices.service_proxy_request(next_page_url, REQUEST_GET_PROXIES_SERVICE, REQUEST_GET_PROXIES_USE)
        html_text = next_page_request.text
        status_code = (next_page_request).status_code
        

        number_of_pages = settings.realtor_pages
        on_page_num = 1 # do not change
        items_scraped = 0 # do not change

        # How many times do you want to try and load the listing page with playwright before terminating?
        get_listing_page_tries = 3
        listing_page_tries = 0 # do not change: this is to record the try number when trying to load the page correctly with playwright


        print("Url, Address, Purchase Price, Units, County, Zip, Efficiency, One-Bedroom, Two-Bedroom, Three-Bedroom, Four-Bedroom")

        for page in range(number_of_pages):
            print(f'PAGE {next_page_url}, STATUS CODE {str(status_code)}, REALTOR.COM, ITEMS SCRAPED {items_scraped}, PAGE {on_page_num}, PAGE {on_page_num}, PAGE {on_page_num}, PAGE {on_page_num}, PAGE {on_page_num}, PAGE {on_page_num}, PAGE {on_page_num}')
            csv_writer.writerow([f'PAGE {next_page_url}', f'STATUS CODE {str(status_code)}', f'REALTOR.COM', f'ITEMS SCRAPED {items_scraped}', f'PAGE {on_page_num}', f'PAGE {on_page_num}', f'PAGE {on_page_num}',f'PAGE {on_page_num}', f'PAGE {on_page_num}', f'PAGE {on_page_num}', f'PAGE {on_page_num}'])
            soup = BeautifulSoup(html_text, 'lxml')

            listings = soup.find_all('div', class_='BasePropertyCard_propertyCardWrap__Z5y4p')

            for listing in listings:
                async with async_playwright() as p:
                    i = 1
                    for i in range(get_listing_page_tries):
                        listing_page_tries +=1
                        try:
                            listing_url =  "https://www.realtor.com" + listing.find('a', class_='LinkComponent_anchor__0C2xC').get('href')
                            browser = await p.chromium.launch(headless=settings.realtor_headless, proxy= proxyservices.get_service_proxy(PLAYWRIGHT_PROXIES_SERVICE, PLAYWRIGHT_PROXIES_USE), slow_mo=500)
                            page = await browser.new_page(ignore_https_errors=True, user_agent= (proxyservices.get_scrapeops_user_agent() if PLAYWRIGHT_USERAGENTS_USE else None))
                            await get_realtor_data(page, listing_url, csv_writer)
                            break
                        except Exception as e:
                            print(e)
                            await browser.close()
                            for i in range(30, 0, -1):
                                print(f'\rFailed to load listing page ({str(listing_page_tries)}/{get_listing_page_tries} tries). Retrying in {i} seconds.\n', end='', flush=True)
                                time.sleep(1)  # Sleep for 1 second
                        
                    else:
                        print(f"ERROR LOADING LISTING PAGE {str(on_page_num)}, ERROR LOADING LISTING PAGE {str(on_page_num)}, ERROR LOADING LISTING PAGE {str(on_page_num)}, ERROR LOADING LISTING PAGE {str(on_page_num)}, ERROR LOADING LISTING PAGE {str(on_page_num)}, ERROR LOADING LISTING PAGE {str(on_page_num)}, ERROR LOADING LISTING PAGE {str(on_page_num)}, ERROR LOADING LISTING PAGE {str(on_page_num)}, ERROR LOADING LISTING PAGE {str(on_page_num)}, ERROR LOADING LISTING PAGE {str(on_page_num)}, ERROR LOADING LISTING PAGE {str(on_page_num)}")
                        csv_writer.writerow([f"ERROR LOADING LISTING PAGE {str(on_page_num)}", f"ERROR LOADING LISTING PAGE {str(on_page_num)}", f"ERROR LOADING LISTING PAGE {str(on_page_num)}", f"ERROR LOADING LISTING PAGE {str(on_page_num)}", f"ERROR LOADING LISTING PAGE {str(on_page_num)}", f"ERROR LOADING LISTING PAGE {str(on_page_num)}", f"ERROR LOADING LISTING PAGE {str(on_page_num)}", f"ERROR LOADING LISTING PAGE {str(on_page_num)}", f"ERROR LOADING LISTING PAGE {str(on_page_num)}", f"ERROR LOADING LISTING PAGE {str(on_page_num)}", f"ERROR LOADING LISTING PAGE {str(on_page_num)}"])
                        break

                items_scraped += 1    

            on_page_num += 1
            if on_page_num <= number_of_pages:
                next_page = f"/pg-{str(on_page_num)}"
                next_page_url = base_link + next_page
                next_page_request = proxyservices.service_proxy_request(next_page_url, REQUEST_GET_PROXIES_SERVICE, REQUEST_GET_PROXIES_USE)
                html_text = next_page_request.text
                status_code = (next_page_request).status_code

asyncio.run(run_realtor_scraper())