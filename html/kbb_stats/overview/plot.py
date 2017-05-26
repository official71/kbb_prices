import matplotlib.pyplot as plt
import os
from collections import defaultdict
import re


def plot_data(make, model, data):
    years = [(2005 + i) for i in xrange(13)]
    all_prices = defaultdict(lambda: None)
    all_styles = defaultdict(lambda: None)

    '''
    Table 'Cars' as data
    (* Primary Keys)

    make (char) | model (char) | year (int) | vehicle_id (int) | style_name (char) | style_spec (char)            | price (int)
                |              |            |          *       |                   |                              |
    --------------------------------------------------------------------------------------------------------------------------
     "Jeep"     |   "Patriot"  |  2017      |       430823     |  "Sport Utility"  | "{"Engine(s)": "2.7 Liter"}" |    18000

    '''
    max_price = 0
    for item in data:
        year = item.year
        if not year in years:
            continue

        style_name = re.sub(r"[/]", "-", str(item.style_name))
        all_styles[style_name] = item.style_spec

        if all_prices[year] is None:
            styles = defaultdict(int)
            styles[style_name] = item.price
            all_prices[year] = styles
        else:
            all_prices[year][style_name] = item.price

        if item.price > max_price:
            max_price = item.price
    
    step = 1000
    while step <= 20000:
        if 10 * step >= max_price:
            break
        step += 1000
    price_ticks = range(0, step * (int(max_price) / int(step) + 1) + 1, step)

    all_img = []
    for style in all_styles:
        plot_file = "overview/static/overview/plot/{}_{}_{}.png".format(make, model, style)
        ret_fname = "overview/plot/{}_{}_{}.png".format(make, model, style)
        if os.path.isfile(plot_file):
            all_img.append(ret_fname)
            continue

        plt.clf()
        lst_prices = []
        for year in years:
            if all_prices[year] is None:
                lst_prices.append(0)
            else:
                lst_prices.append(all_prices[year][style])
        plt.scatter(years, lst_prices, label=all_styles[style])
        plt.xlabel('Year')
        plt.xticks([years[i] for i in xrange(0, len(years), 2)])
        plt.ylabel('KBB Suggested Price')
        plt.yticks(price_ticks)
        # plt.legend()
        plt.title(style)
        plt.grid(True)
        for a,b in zip(years, lst_prices):
            if b > 0:
                plt.text(a, b, "${}".format(b))

        plt.savefig(plot_file)

        if os.path.isfile(plot_file):
            all_img.append(ret_fname)

    all_img.sort()
    return all_img