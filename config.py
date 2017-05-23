BASE_URL = 'https://www.kbb.com/'
COMPARE_URL = 'https://www.kbb.com/compare-cars/overview/'

MODEL_JSON_FILE = 'data/models.json'
STYLE_JSON_FILE = 'data/styles.json'
PRICE_JSON_FILE = 'data/prices.json'

IMAGE_DIR = 'data/model_images/'
PRICE_DIR = 'data/prices/'

YEARS = ['2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017']

# database is created by django app, but we use load_cars.py to populate the data
CARS_DATABASE = 'html/kbb_stats/db.sqlite3'
CARS_TABLE = 'overview_cars'