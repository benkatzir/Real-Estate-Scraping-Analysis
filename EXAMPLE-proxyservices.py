import requests
from random import randint
from urllib.parse import urlencode
import json
import urllib.parse
from scrapingbee import ScrapingBeeClient

#SCRAPOPS.IO------------------------------------------------------------------

# Scrapeops API settup:
SCRAPEOPS_API_KEY = 'YOUR_SCRAPEOPS_API_KEY'

# ScrapeOps proxy configuration (PLAYWRIGHT)
SCRAPEOPS_PROXY_USERNAME = 'scrapeops.headless_browser_mode=false'
SCRAPEOPS_PROXY_PASSWORD = SCRAPEOPS_API_KEY
SCRAPEOPS_PROXY_SERVER = 'proxy.scrapeops.io'
SCRAPEOPS_PROXY_SERVER_PORT = '5353'


# Get scrapeops fake user agent
def get_scrapeops_user_agent():
    # Get headers list
    response = requests.get('http://headers.scrapeops.io/v1/browser-headers?api_key=' + SCRAPEOPS_API_KEY)
    header_list = response.json().get('result', [])

    # Choose a random header
    random_index = randint(0, len(header_list)-1)
    return header_list[random_index]['user-agent']

# Get scrapeops fake browser header
def get_scrapeops_browser_header():
    # Get headers list
    response = requests.get('http://headers.scrapeops.io/v1/browser-headers?api_key=' + SCRAPEOPS_API_KEY)
    header_list = response.json().get('result', [])

    # Choose a random header
    random_index = randint(0, len(header_list)-1)
    return header_list[random_index]

# Make a request through scrapeops proxy API
def scrapeops_proxy_request(url):
    try:
        proxy_params = {
        'api_key': '{api_key}'.format(api_key = SCRAPEOPS_API_KEY),
        'url': '{url}'.format(url=url), 
        'render_js': 'true',
        'country': 'us',
        }
        return requests.get(url='https://proxy.scrapeops.io/v1/', params=urlencode(proxy_params), timeout=120)
    except Exception as e:
        return requests.get(url)

# Make a request through scrapeops proxi API with sessions
def scrapeops_proxy_request2(url, requests_session=None):
    try:
        proxy_params = {
        'api_key': '{api_key}'.format(api_key = SCRAPEOPS_API_KEY),
        'url': '{url}'.format(url=url), 
        'render_js': True,
        'country': 'us',
        }
        if requests_session != None:
            return requests_session.get(url='https://proxy.scrapeops.io/v1/', params=urlencode(proxy_params), timeout=120)
        else:
            return requests.get(url='https://proxy.scrapeops.io/v1/', params=urlencode(proxy_params), timeout=120)
    except Exception as e:
        if requests_session != None:
            return requests_session.get(url)
        else:
            return requests.get(url)

# Make a request through scrapeops proxy API to scroll page
# and wait until returning html (js instructions for scrapeops
# api's headless browser documentation: https://scrapeops.io/docs/proxy-aggregator/advanced-functionality/javascript-scenario/)
def scrapeops_proxy_request3(url, scroll_pixels):
    try:
        #wait to send html back
        js_scenario = {
            "instructions": [
            {"wait": 3000}
            ]
        }
        js_scenario_string = json.dumps(js_scenario)
        encoded_js_scenario = urllib.parse.quote(js_scenario_string)

        proxy_params = {
        'api_key': '{api_key}'.format(api_key = SCRAPEOPS_API_KEY),
        'url': '{url}'.format(url=url), 
        'scroll': scroll_pixels,
        'render_js': True,
        'js_scenario' : encoded_js_scenario,
        'country': 'us',
        }
        return requests.get(url='https://proxy.scrapeops.io/v1/', params=urlencode(proxy_params), timeout=120)
    except Exception as e:
        return requests.get(url)

# Make a request through scrapeops proxy API if use_proxies is true, else use regular request.get(url) function
def scrapeops_proxy_request4(url, use_proxies):
    if use_proxies == True:
        try:
            proxy_params = {
            'api_key': '{api_key}'.format(api_key = SCRAPEOPS_API_KEY),
            'url': '{url}'.format(url=url), 
            'render_js': 'true',
            'country': 'us',
            }
            return requests.get(url='https://proxy.scrapeops.io/v1/', params=urlencode(proxy_params), timeout=120)
        except Exception as e:
            return requests.get(url)
    else:
        return requests.get(url)

# Get scrapeops proxy for playwright
def get_scrapeops_proxy(use_proxies):
    if use_proxies:
        scrapeops_proxy = {
            'server' : 'http://{PROXY_SERVER}:{PROXY_SERVER_PORT}'.format(PROXY_SERVER = SCRAPEOPS_PROXY_SERVER, PROXY_SERVER_PORT = SCRAPEOPS_PROXY_SERVER_PORT),
            'username' : '{PROXY_USERNAME}'.format(PROXY_USERNAME = SCRAPEOPS_PROXY_USERNAME),
            'password': '{PROXY_PASSWORD}'.format(PROXY_PASSWORD = SCRAPEOPS_PROXY_PASSWORD)
        }
        return scrapeops_proxy
    else:
        return None

#OXYLABS.IO-------------------------------------------------------------------------

# Oxylabs proxy configuration (PLAYWRIGHT)
OXYLABS_PROXY_USERNAME = 'YOUR_OXYLABS_PROXY_USERNAME'
OXYLABS_PROXY_PASSWORD = 'YOUR_OXYLABS_PROXY_PASSWORD'
OXYLABS_PROXY_SERVER = 'us-pr.oxylabs.io'
OXYLABS_PROXY_SERVER_PORT = '10000'

# Get oxylabs proxy for playwright
def get_oxylabs_proxy(use_proxies):
    if use_proxies:
        oxylabs_proxy = {
            'server' : 'http://{PROXY_SERVER}:{PROXY_SERVER_PORT}'.format(PROXY_SERVER = OXYLABS_PROXY_SERVER, PROXY_SERVER_PORT = OXYLABS_PROXY_SERVER_PORT),
            'username' : '{PROXY_USERNAME}'.format(PROXY_USERNAME = OXYLABS_PROXY_USERNAME),
            'password': '{PROXY_PASSWORD}'.format(PROXY_PASSWORD = OXYLABS_PROXY_PASSWORD)
        }
        return oxylabs_proxy
    else:
        return None

# Make a request through oxylabs proxy
def oxylabs_proxy_request(url, use_proxies):
    if use_proxies == True:
        try:
            return requests.get(url=url, proxies= get_oxylabs_proxy(), timeout=120)
        except Exception as e:
            return requests.get(url)
    else:
        return requests.get(url)

#IPROYAL.COM------------------------------------------------------------------------------------

# IProyal proxy configuration (PLAYWRIGHT)
IPROYAL_PROXY_USERNAME = 'YOUR_IPROYAL_PROXY_USERNAME'
IPROYAL_PROXY_PASSWORD = 'YOUR_IP_ROYAL_PPROXY_PASSWORD'
IPROYAL_PROXY_SERVER = 'geo.iproyal.com'
IPROYAL_PROXY_SERVER_PORT = '12321'

# Get iproyal proxy for playwright
def get_iproyal_proxy(use_proxies):
    if use_proxies:
        iproyal_proxy = {
            'server' : 'http://{PROXY_SERVER}:{PROXY_SERVER_PORT}'.format(PROXY_SERVER = IPROYAL_PROXY_SERVER, PROXY_SERVER_PORT = IPROYAL_PROXY_SERVER_PORT),
            'username' : '{PROXY_USERNAME}'.format(PROXY_USERNAME = IPROYAL_PROXY_USERNAME),
            'password': '{PROXY_PASSWORD}'.format(PROXY_PASSWORD = IPROYAL_PROXY_PASSWORD)
        }
        return iproyal_proxy
    else:
        return None

# Make a request through iproyal proxy
def iproyal_proxy_request(url, use_proxies):
    if use_proxies == True:
        try:
            return requests.get(url=url, proxies= get_iproyal_proxy(), timeout=120)
        except Exception as e:
            return requests.get(url)
    else:
        return requests.get(url)


# SCRAPINGBEE.COM-------------------------------------------------------------------------------

# Get scrapingbee proxy for playwright
SCRAPINGBEE_PROXY_USERNAME = 'YOUR_SCRAPINGbEE_PROXY_USERNAME'
SCRAPINGBEE_PROXY_PASSWORD = 'render_js=False&premium_proxy=False&stealth_proxy=False'
SCRAPINGBEE_PROXY_SERVER = 'proxy.scrapingbee.com'
SCRAPINGBEE_PROXY_SERVER_PORT = '8886'

# Get  scrapingbee proxy for playwright
def get_scrapingbee_proxy(use_proxies):
    if use_proxies:
        scrapingbee_proxy = {
            'server' : 'http://{PROXY_SERVER}:{PROXY_SERVER_PORT}'.format(PROXY_SERVER = SCRAPINGBEE_PROXY_SERVER, PROXY_SERVER_PORT = SCRAPINGBEE_PROXY_SERVER_PORT),
            'username' : '{PROXY_USERNAME}'.format(PROXY_USERNAME = SCRAPINGBEE_PROXY_USERNAME),
            'password': '{PROXY_PASSWORD}'.format(PROXY_PASSWORD = SCRAPINGBEE_PROXY_PASSWORD)
        }
        return scrapingbee_proxy
    else:
        return None

# Make a request through iproyal proxy
def scrapingbee_proxy_request(url, use_proxies):
    if use_proxies == True:
        try:  
            client = ScrapingBeeClient(api_key=SCRAPINGBEE_PROXY_USERNAME)
            params = {
                'premium_proxy': 'True',
                'stealth_proxy': 'True',
                'country_code': 'us',
                }
            response = client.get(url, params = urlencode(params))
            return response
        except Exception as e:
            return requests.get(url)
    else:
        return requests.get(url)


#CHOOSE PROXY SERVICE TO USE FOR REQUEST.GET() METHOD----------------------------------------------

def service_proxy_request(url, service, use_proxies):
    if service == 'scrapeops':
        return scrapeops_proxy_request4(url, use_proxies)
    elif service == 'oxylabs':
        return oxylabs_proxy_request(url, use_proxies)
    elif service == 'iproyal':
        return iproyal_proxy_request(url, use_proxies)
    elif service == 'scrapingbee':
        return scrapingbee_proxy_request(url, use_proxies)
    else:
        # If service is miss-spelled
        return requests.get(url)

#CHOOSE PROXY SERVICE TO USE FOR PLAYWRIGHT HEADLESS BROWSER----------------------------------------------

def get_service_proxy(service, use_proxies):
    if service == 'scrapeops':
        return get_scrapeops_proxy(use_proxies)
    elif service == 'oxylabs':
        return get_oxylabs_proxy(use_proxies)
    elif service == 'iproyal':
        return get_iproyal_proxy(use_proxies)
    elif service == 'scrapingbee':
        return get_scrapingbee_proxy(use_proxies)
    else:
        # If service is miss-spelled
        return None