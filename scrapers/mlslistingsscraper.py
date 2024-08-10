from bs4 import BeautifulSoup
import requests
import csv 
import sys
sys.path.append('C:\\Users\\ayele\\realestate\\all_scraper_1.6')
import settings
import wscrape
import hudapi
import proxyservices

# BS4 HEAVY SCRAPER
# Uses requests library to get page html content and then uses bs4 to parse it

# If this is true, script will use proxies when using request.get() method
REQUEST_GET_PROXIES_USE = settings.MLSLISTINGS_REQUEST_GET_PROXIES_USE
# Will use proxy service specified in scraper settings for request.get() method - proxyservices.service_proxy_request()
REQUEST_GET_PROXIES_SERVICE = settings.MLSLISTINGS_REQUEST_GET_PROXIES_SERVICE

with open('data.csv', 'a', newline='', encoding = 'utf8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Url', 'Address', 'Purchase Price', 'Units', 'County', 'Zip', 'Efficiency', 'One-Bedroom', 'Two-Bedroom', 'Three-Bedroom', 'Four-Bedroom'])

    base_link = settings.mlslistings_url
    next_page_url = base_link
    next_page_request = proxyservices.service_proxy_request(next_page_url, REQUEST_GET_PROXIES_SERVICE, REQUEST_GET_PROXIES_USE)
    html_text = next_page_request.text
    status_code = (next_page_request).status_code

    number_of_pages = settings.mlslistings_pages
    on_page_num = 1 # do not change
    items_scraped = 0 # do not change

    print("Url, Address, Purchase Price, Units, County, Zip, Efficiency, One-Bedroom, Two-Bedroom, Three-Bedroom, Four-Bedroom")

    for page in range(number_of_pages):
        print(f'PAGE {next_page_url}, STATUS CODE {str(status_code)}, MLSLISTINGS.COM, ITEMS SCRAPED {items_scraped}, PAGE {on_page_num}, PAGE {on_page_num}, PAGE {on_page_num}, PAGE {on_page_num}, PAGE {on_page_num}, PAGE {on_page_num}, PAGE {on_page_num}')
        csv_writer.writerow([f'PAGE {next_page_url}', f'STATUS CODE {str(status_code)}', f'MLSLISTINGS.COM', f'ITEMS SCRAPED {items_scraped}', f'PAGE {on_page_num}', f'PAGE {on_page_num}', f'PAGE {on_page_num}',f'PAGE {on_page_num}', f'PAGE {on_page_num}', f'PAGE {on_page_num}', f'PAGE {on_page_num}'])
        soup = BeautifulSoup(html_text, 'lxml')

        listing_url_containers = listing_urls = soup.find_all('h5', class_ = 'card-title font-weight-bold listing-address mb-25')
        
        for listing_url_container in listing_url_containers:
            try:
                if listing_url_container != None:
                    listing_url = listing_url_container.a.get('href')
                    listing_url = "https://www.mlslistings.com" + listing_url

                    listing_html_text = proxyservices.service_proxy_request(listing_url, REQUEST_GET_PROXIES_SERVICE, REQUEST_GET_PROXIES_USE).text
                    individual_listing = BeautifulSoup(listing_html_text, 'lxml')
                    property_description = wscrape.verify_not_nonetype(individual_listing.find('p', class_ = 'mb-0 font-size-midr line-height-xl'), "obj.text")
                                        
                    address = listing_url_container.text
                    purchase_price = wscrape.verify_not_nonetype(individual_listing.find('div', class_='col-lg-8 col-xl-8 col-xs-12 col sticky-col'), "obj.find_all('div', class_ = 'row basline-sticky')[1].div.h4.text.split(' ', 1)[0]")
                    units = wscrape.find_units(property_description, 2)
                    county = settings.location_assign(settings.location)
                    zip = wscrape.extract_zipcode(address)
                    effiency, one_bedroom, two_bedroom, three_bedroom, four_bedroom = hudapi.hud_location_fmrs3(county, zip, settings.DEFAULT_FMR)

                    csv_writer.writerow([listing_url, address, purchase_price, units, county, zip, effiency, one_bedroom, two_bedroom, three_bedroom, four_bedroom])
                    print(f"{listing_url}, {address}, {purchase_price}, {units}, {county}, {zip}, {effiency}, {one_bedroom}, {two_bedroom}, {three_bedroom}, {four_bedroom}")
            except Exception as e:
                csv_writer.writerow(['ERROR REQUESTING LISTING', 'ERROR REQUESTING LISTING', 'ERROR REQUESTING LISTING', 'ERROR REQUESTING LISTING', 'ERROR REQUESTING LISTING', 'ERROR REQUESTING LISTING', 'ERROR REQUESTING LISTING', 'ERROR REQUESTING LISTING', 'ERROR REQUESTING LISTING', 'ERROR REQUESTING LISTING', 'ERROR REQUESTING LISTING'])
                print(f"ERROR REQUESTING LISTING, ERROR REQUESTING LISTING, ERROR REQUESTING LISTING, ERROR REQUESTING LISTING, ERROR REQUESTING LISTING, ERROR REQUESTING LISTING, ERROR REQUESTING LISTING, ERROR REQUESTING LISTING, ERROR REQUESTING LISTING, ERROR REQUESTING LISTING, ERROR REQUESTING LISTING")
                print({e})

            items_scraped +=1

        on_page_num += 1
        if on_page_num <= number_of_pages:
            next_page = f"{str(on_page_num)}?view=list"
            next_page_url = base_link + next_page
            next_page_request = proxyservices.service_proxy_request(next_page_url, REQUEST_GET_PROXIES_SERVICE, REQUEST_GET_PROXIES_USE)
            html_text = next_page_request.text
            status_code = (next_page_request).status_code