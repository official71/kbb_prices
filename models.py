import os
import bs4
import urllib
from bs4 import BeautifulSoup
from urlparse import urljoin


def div_class_left(tag):
    return isinstance(tag, bs4.element.Tag) and tag.has_attr('class') and tag['class'] == ['left']

def div_class_model_image(tag):
    return isinstance(tag, bs4.element.Tag) and tag.has_attr('class') and tag['class'] == ['model-image']

'''
Get dictionary of all models of makes from kbb
'''
def list_all_models(base_url, all_makes):
    all_models = {}

    for make in all_makes:
        url = urljoin(base_url, make)
        try:
            page = urllib.urlopen(url)
        except:
            print("Failed to open url: {}".format(url))
            continue

        ll = [] # list of all models of given make, each entry in list is a dictionary

        soup = BeautifulSoup(page, 'lxml')
        all_div = soup.find_all('div', {'class': 'model-year-wrapper'})
        for div in all_div:
            model = ''
            image = ''
            for dv in div.div.contents:
                if div_class_left(dv):
                    model = dv.a['href'].split('/')[-2]
                if div_class_model_image(dv):
                    image = 'https:' + dv.img['src']
                
            dd = {} # dictionary representing a single model
            if model:
                dd['name'] = model
                dd['image'] = image
                ll.append(dd)

        all_models[make] = ll

    return all_models

'''
Save images of all models
'''
def save_model_images(all_models, img_dir):
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)

    for make in all_models:
        make_dir = img_dir + make
        if not os.path.exists(make_dir):
            os.makedirs(make_dir)

        for model in all_models[make]:
            img_url = model.get('image')
            if not img_url is None:
                fmt = img_url.split('.')[-1]
                if not fmt in ['jpg', 'png']:
                    print("Unsupported file format: {}".format(fmt))
                    continue
                fname = make_dir + '/' + model['name'] + '.' + fmt
                print("Saving image file to {}".format(fname))
                urllib.urlretrieve(img_url, fname)



