import re
import os
import urllib
from bs4 import BeautifulSoup
from urlparse import urljoin, urlparse, parse_qs
from utils import cprint, dump_to_json


def page_not_found(soup):
    try:
        return not re.match('Sorry,', str(soup.find('h1').text)) is None
    except:
        return False

def retrieve_prices_by_compare(all_styles, compare_url, years, out_dir):
    '''
    - all_styles {make: models}
        - models [model1, model2, ...]
            - model {name: 'name', year: styles}
                - styles [style1, style2, ...]
                    - style {'name', 'id', 'attr1', 'attr2', ...}
                             (this function adds 'price' attr to it)
    '''

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    for make in all_styles:
        models = all_styles[make]
        for model in models:
            model_name = model.get('name')
            if model_name is None:
                cprint("Empty model name in list for make {}".format(make), 'err')
                continue

            for year in years:
                styles = model.get(year)
                if styles is None:
                    continue
                for style in styles:
                    vehicle_id = style.get('id')
                    if vehicle_id is None:
                        if style.get('name') is None:
                            cprint("Empty vehicle id for {} {} {} UNKNOWN TYPE".format(year, make, model_name), 'r')
                        else:
                            cprint("Empty vehicle id for {} {} {} style {}".format(year, make, model_name, style['name']), 'r')
                        continue
                    
                    url = '{}{}-{}-{}-{}/'.format(compare_url, year, make, model_name, vehicle_id)
                    try:
                        page = urllib.urlopen(url)
                    except:
                        cprint("Failed to open url: {}".format(url), 'err')
                        continue

                    soup = BeautifulSoup(page, 'lxml')
                    if page_not_found(soup):
                        cprint("Compare page for {} {} {} {} does not exist".format(year, make, model_name, vehicle_id), 'r')
                        continue

                    for td in soup.find_all('td', {'class': ''}):
                        spans = td.find_all('span')
                        if len(spans) == 2 and spans[0].text == 'KBB Suggested Retail':
                            style['price'] = spans[1].text
                            cprint("Suggested price {} for {} {} {} style {}".format(style['price'], year, make, model_name, style['name']), 'g')
        cprint("Saving data for make {}".format(make), 'hi')
        out_file = out_dir + make + '.json'
        dump_to_json(all_styles[make], out_file)
