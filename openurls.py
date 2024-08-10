import webbrowser
import settings

# Before running runner.py, run openurls.py to open all urls to verify they aren't outdated
# Before running openurls.py, in settings.py comment lines 25-26 and uncomment location = int

def open_urls(urls):
    for url in urls:
        webbrowser.open(url)
        print(f"{url}\n")

open_urls([
    settings.cbhomes_url,
    settings.compass_url,
    settings.homes_url,
    settings.mlslistings_url,
    settings.point2homes_url,
    settings.propertyshark_url,
    settings.redfin_url,
    settings.remax_url,
    settings.vanguard_url,
    settings.zerodown_url,
    settings.zillow_url,
    settings.investorlift_url,
    settings.realtor_url,
    settings.trulia_url,
    settings.rockethomes_url, 
    settings.flyhomes_url, 
    settings.movoto_url
    ])