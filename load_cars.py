import sqlite3
from config import *
from glob import glob
import json
import re


'''
Database:   (CARS_DATABASE) html/kbb_stats/db.sqlite3
Table:      (CARS_TABLE) overview_cars
Schema:

(* Primary Keys)

make (char) | year (int) | vehicle_id (int) | style_name (char) | style_spec (char)            | price (int) | model (char) 
            |            |          *       |                   |                              |             |               
--------------------------------------------------------------------------------------------------------------------------
 "Jeep"     |  2017      |       430823     |  "Sport Utility"  | "{"Engine(s)": "2.7 Liter"}" |    18000    |   "Patriot"  

'''

def load_file(fd, cursor):
    '''
    - all_styles {make: models}
        - models [model1, model2, ...]
            - model {name: 'name', year: styles}
                - styles [style1, style2, ...]
                    - style {'name', 'id', 'attr1', 'attr2', ...}
                             (this function adds 'price' attr to it)
    '''
    make = str(fd.name.split('/')[-1].split('.')[0])
    print("Loading data for make: {}".format(make))

    models = json.load(fd)
    for model in models:
        model_name = str(model['name'])
        print("...loading model: {}".format(model_name))
        for year in YEARS:
            if model.get(year) is None:
                continue
            for style in model[year]:
                style_name = ""
                style_spec = ""
                vehicle_id = 0
                price = 0
                for key in style:
                    if key == 'name':
                        style_name = purify(style[key])
                    elif key == 'id':
                        vehicle_id = int(style[key])
                    elif key == 'price':
                        price = price2int(style[key])
                    elif key == 'url':
                        pass
                    else:
                        style_spec += "\"{}\":\"{}\",".format(str(key).rstrip(':'), str(style[key]))

                style_spec = "{" + style_spec.rstrip(',') + "}"
                print("......loading {} {} {} ({})".format(year, model_name, style_name, vehicle_id))
                # print("              id: {}, price: {}, spec: {}".format(vehicle_id, price, style_spec))

                sql_str = "INSERT INTO {} VALUES ('{}', {}, {}, '{}', '{}', {}, '{}')".format(
                    CARS_TABLE, make, year, vehicle_id, style_name, style_spec, price, model_name)
                # print("......sqlcmd: {}".format(sql_str))
                try:
                    cursor.execute(sql_str)
                except:
                    print("......sqlcmd failed")


def purify(s):
    return re.sub(r"[']", "-", str(s))

def price2int(s):
    # sample input: "$53,600.00"
    # output: 53600
    return re.sub(r"\D", "", s.split('.')[0])


def main():
    conn = sqlite3.connect(CARS_DATABASE)
    try:
        cursor = conn.cursor()

        for fname in glob("{}*.json".format(PRICE_DIR)):
            with open(fname, 'r') as fd:
                load_file(fd, cursor)

        
        # cursor.execute("INSERT INTO {} VALUES ('m1', 'm2', 1999, 1111, 's', 'spec', 10000)".format(table))
        # cursor.execute("SELECT * FROM {}".format(table))
        # for r in cursor.fetchall():
        #     print r
        # cursor.execute("DELETE FROM {} WHERE make=\"m1\"".format(table))
        cursor.execute("SELECT * FROM {}".format(CARS_TABLE))
        for r in cursor.fetchall():
            print r

        conn.commit()

    finally:
        conn.close()

if __name__ == '__main__':
    main()