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

# If this is true, script will use proxies when using request.get() method - proxyservices.service_proxy_request()
REQUEST_GET_PROXIES_USE = settings.COMPASS_REQUEST_GET_PROXIES_USE
# Will use proxy service specified in scraper settings for request.get() method
REQUEST_GET_PROXIES_SERVICE = settings.COMPASS_REQUEST_GET_PROXIES_SERVICE

with open('data.csv', 'a', newline='', encoding = 'utf8') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Url', 'Address', 'Purchase Price', 'Units', 'County', 'Zip', 'Efficiency', 'One-Bedroom', 'Two-Bedroom', 'Three-Bedroom', 'Four-Bedroom'])

    base_link = settings.compass_url
    next_page_url = base_link
    next_page_request = proxyservices.service_proxy_request(next_page_url, REQUEST_GET_PROXIES_SERVICE, REQUEST_GET_PROXIES_USE)
    html_text = next_page_request.text
    status_code = (next_page_request).status_code
    

    number_of_pages = settings.compass_pages
    on_page_num = 1 # do not change
    items_scraped = 0 # do not change

    print("Url, Address, Purchase Price, Units, County, Zip, Efficiency, One-Bedroom, Two-Bedroom, Three-Bedroom, Four-Bedroom")

    for page in range(number_of_pages):
        print(f'PAGE {next_page_url}, STATUS CODE {str(status_code)}, COMPASS.COM, ITEMS SCRAPED {items_scraped}, PAGE {on_page_num}, PAGE {on_page_num}, PAGE {on_page_num}, PAGE {on_page_num}, PAGE {on_page_num}, PAGE {on_page_num}, PAGE {on_page_num}')
        csv_writer.writerow([f'PAGE {next_page_url}', f'STATUS CODE {str(status_code)}', f'COMPASS.COM', f'ITEMS SCRAPED {items_scraped}', f'PAGE {on_page_num}', f'PAGE {on_page_num}', f'PAGE {on_page_num}',f'PAGE {on_page_num}', f'PAGE {on_page_num}', f'PAGE {on_page_num}', f'PAGE {on_page_num}'])
        soup = BeautifulSoup(html_text, 'lxml')

        listings = soup.find_all('div', class_ = 'uc-listingPhotoCard uc-listingCard uc-listingCard-has-photo')

        for listing in listings:
            try:
                listing_url = "https://www.compass.com" + listing.find('h2', class_ = 'uc-listingCard-title truncate-overflow-text').a.get('href')
                
                
                listing_html_text = proxyservices.service_proxy_request(listing_url, REQUEST_GET_PROXIES_SERVICE, REQUEST_GET_PROXIES_USE).text
                individual_listing = BeautifulSoup(listing_html_text, 'lxml')
                property_description = wscrape.if_nonetype_str(wscrape.verify_not_nonetype(individual_listing.find('span', class_ ='sc-kZmPBK faqVNH'), "obj.text")) + wscrape.if_nonetype_str((wscrape.verify_not_nonetype(individual_listing.find('span', class_ ='sc-kZmPBK bRQuXd'), "obj.text")))
                address = wscrape.if_nonetype_str(wscrape.verify_not_nonetype(individual_listing.find('p', class_ = 'summary__StyledAddress-e4c4ok-8 iLsMEa textIntent-title1'), "obj.text")) + ", " + wscrape.if_nonetype_str(wscrape.verify_not_nonetype(individual_listing.find('span', class_='summary__StyledAddressSubtitle-e4c4ok-9 cINUCs'), "obj.text"))
                purchase_price = wscrape.verify_not_nonetype(individual_listing.find('div', {'data-tn' : 'listing-page-summary-price'}), "obj.div.div.text")
                units = wscrape.find_units(property_description, 2)
                county = settings.location_assign(settings.location)
                zip = wscrape.extract_zipcode(address)
                effiency, one_bedroom, two_bedroom, three_bedroom, four_bedroom = hudapi.hud_location_fmrs3(county, zip, settings.DEFAULT_FMR)
                print(effiency)
                csv_writer.writerow([listing_url, address, purchase_price, units, county, zip, effiency, one_bedroom, two_bedroom, three_bedroom, four_bedroom])
                print(f"{listing_url}, {address}, {purchase_price}, {units}, {county}, {zip}, {effiency}, {one_bedroom}, {two_bedroom}, {three_bedroom}, {four_bedroom}")
            except Exception as e:
                csv_writer.writerow(['ERROR REQUESTING LISTING', 'ERROR REQUESTING LISTING', 'ERROR REQUESTING LISTING', 'ERROR REQUESTING LISTING', 'ERROR REQUESTING LISTING', 'ERROR REQUESTING LISTING', 'ERROR REQUESTING LISTING', 'ERROR REQUESTING LISTING', 'ERROR REQUESTING LISTING', 'ERROR REQUESTING LISTING', 'ERROR REQUESTING LISTING'])
                print(f"ERROR REQUESTING LISTING, ERROR REQUESTING LISTING, ERROR REQUESTING LISTING, ERROR REQUESTING LISTING, ERROR REQUESTING LISTING, ERROR REQUESTING LISTING, ERROR REQUESTING LISTING, ERROR REQUESTING LISTING, ERROR REQUESTING LISTING, ERROR REQUESTING LISTING, ERROR REQUESTING LISTING")
                print({e})

            items_scraped +=1

        on_page_num += 1
        if on_page_num <= number_of_pages:
            next_page = f"/start={str(items_scraped)}"
            next_page_url = base_link + next_page
            next_page_request = proxyservices.service_proxy_request(next_page_url, REQUEST_GET_PROXIES_SERVICE, REQUEST_GET_PROXIES_USE)
            html_text = next_page_request.text
            status_code = (next_page_request).status_code