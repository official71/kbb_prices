import re
import bs4
import urllib
from bs4 import BeautifulSoup
from urlparse import urljoin, urlparse, parse_qs
from utils import cprint

def div_class_vehicle_style_container(tag):
    return isinstance(tag, bs4.element.Tag) and tag.has_attr('class') and 'vehicle-styles-container' in tag['class']

def div_class_vehicle_style_head(tag):
    return isinstance(tag, bs4.element.Tag) and tag.has_attr('class') and 'vehicle-styles-head' in tag['class'] and not 'not-sure' in tag['class']

def div_class_vehicle_style_body(tag):
    return isinstance(tag, bs4.element.Tag) and tag.has_attr('class') and 'vehicle-styles-body' in tag['class']

def page_not_found(soup):
    try:
        return not re.match('Sorry,', str(soup.find('h1').text)) is None
    except:
        return False

def list_all_styles(all_models, base_url, years):
    '''
    - all_styles {make: models}
        - models [model1, model2, ...]
            - model {name: 'name', year: styles}
                - styles [style1, style2, ...]
                    - style {'name', 'id', 'attr1', 'attr2', ...}
    '''
    all_styles = {}

    for make in all_models:
        models = []

        for m in all_models[make]:
            model_name = m.get('name')

            model = {}
            model['name'] = model_name
            for year in years:
                url = '{}{}/{}/{}/styles/?intent=buy-used'.format(base_url, make, model_name, year)
                try:
                    page = urllib.urlopen(url)
                except:
                    cprint("Failed to open url: {}".format(url), 'err')
                    continue

                soup = BeautifulSoup(page, 'lxml')
                if page_not_found(soup):
                    cprint("Model {} {} {} does not exist".format(year, make, model_name), 'r')
                    continue

                cprint("Retrive style for {} {} {}".format(year, make, model_name), 'g')
                styles = []

                style_containers = soup.find_all('div', {'class': 'vehicle-styles-container'})
                for sc in style_containers:
                    style = {}

                    for t in sc.contents:
                        if div_class_vehicle_style_head(t):
                            link = t.a['href']
                            style['url'] = link
                            style['name'] = t.div.text.strip(' \r\n\t')
                            style['id'] = parse_qs(urlparse(link).query)['vehicleid'][0]
                        if div_class_vehicle_style_body(t):
                            for tr in t.table.find_all('tr'):
                                tds = tr.find_all('td')
                                style[tds[0].text] = tds[1].text

                    if not style.get('name') is None:
                        styles.append(style)
                model[year] = styles
            models.append(model)
        all_styles[make] = models

    return all_styles