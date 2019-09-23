import re
from bs4 import BeautifulSoup
import urllib
from urllib.parse import urlparse
from selenium import webdriver
from bs4 import NavigableString
import json

browser = webdriver.Firefox(executable_path=r'C:\Users\Zprint\Downloads\geckodriver.exe')
browser.get('https://www.zomato.com/bangalore/8293-kr-puram')

html_text = browser.page_source
# make a soup out of html
soup = BeautifulSoup(html_text, 'lxml')

rest_details = dict()
name_anchor = soup.find("a", attrs={"class": "ui large header left"})
if name_anchor:
    rest_details['name'] = name_anchor.text.strip()
else:
    rest_details['name'] = ''

rating_div = soup.find("div", attrs={"class": re.compile("rating-for")})
if rating_div:
    rest_details['rating'] = rating_div.text.strip()[:-2]
else:
    rest_details['rating'] = 'N/A'  # default

area_div = soup.find("a",attrs={"class": re.compile("left grey-text fontsize3")})
if area_div:
    rest_details['area'] = area_div.text.strip()
else:
    rest_details['area'] = 'N/A'  # default

type_div = soup.find("a",attrs={"class": re.compile("grey-text fontsize3"),"title":"View all Quick Bites in "})
if type_div:
    rest_details['type'] = type_div.text.strip()
else:
    rest_details['type'] = 'N/A'  # default

reviews_div = soup.find("span",attrs={"class": re.compile("tooltip_formatted fbold")})
if reviews_div:
    rest_details['reviews'] = reviews_div.text.strip().split()[0]
else:
    rest_details['reviews'] = 'N/A'  # default

cuisines_div = soup.find("a",attrs={"class": "zred","title":"View all Chinese Restaurants in Bengaluru"})
if cuisines_div:
    rest_details['cuisines'] = cuisines_div.text.strip()
else:
    rest_details['cuisines'] = 'N/A'  # default

cost_for_two_div = soup.find("span",attrs={"aria-label": re.compile("for two people")})
if cost_for_two_div:
    rest_details['cost_for_two'] = cost_for_two_div.text.strip().split()[0]
else:
    rest_details['cost_for_two'] = 'N/A'  # default

geo_locale = soup.find("div", attrs={"class": "resmap-img"})
if geo_locale:
    geo_url = geo_locale.attrs['data-url']
    parsed_url = urlparse(geo_url)
    geo_arr = str(urllib.parse.parse_qs(parsed_url.query)['center']).split(',')
    rest_details['geo_location'] = [re.sub("[^0-9\.]", "", geo_arr[0]), re.sub("[^0-9\.]", "", geo_arr[1])]
if 'geo_location' not in rest_details:
    rest_details['geo_location'] = ['undefined', 'undefined']

print(rest_details)

browser.close()

