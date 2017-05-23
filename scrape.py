from utils import *
from config import *
from makes import list_all_makes
from models import list_all_models, save_model_images
from styles import list_all_styles
from prices import retrieve_prices_by_compare
import os

def main():
    print('base url: {}'.format(BASE_URL))
    # all_makes = list_all_makes(BASE_URL)
    
    # all_models = list_all_models(BASE_URL, all_makes)
    # dump_to_json(all_models, MODEL_JSON_FILE)
    all_models = load_from_json(MODEL_JSON_FILE)
    
    # save_model_images(all_models, IMAGE_DIR)
    
    # all_styles = list_all_styles(all_models, BASE_URL, YEARS)
    # dump_to_json(all_styles, STYLE_JSON_FILE)
    all_styles = load_from_json(STYLE_JSON_FILE)

    retrieve_prices_by_compare(all_styles, COMPARE_URL, YEARS, PRICE_DIR)
    # dump_to_json(all_styles, PRICE_JSON_FILE)


if __name__ == '__main__':
    main()