from collections import defaultdict
import json


def get_style_table(make, model, data):
    years = [(2005 + i) for i in xrange(13)]
    all_styles = defaultdict(lambda: None)
    all_specs = defaultdict(int)

    '''
    Table 'Cars' as data
    (* Primary Keys)

    make (char) | model (char) | year (int) | vehicle_id (int) | style_name (char) | style_spec (char)            | price (int)
                |              |            |          *       |                   |                              |
    --------------------------------------------------------------------------------------------------------------------------
     "Jeep"     |   "Patriot"  |  2017      |       430823     |  "Sport Utility"  | "{"Engine(s)": "2.7 Liter"}" |    18000

    '''
    for item in data:
        year = item.year
        if not year in years:
            continue

        style_name = item.style_name
        try:
            specs = json.loads(item.style_spec)
            all_styles[style_name] = specs
            for spec in specs:
                all_specs[spec] += 1
        except:
            print("Failed to parse spec for style {}".format(style_name))

    first_row = ['Style']
    for spec in all_specs:
        first_row.append(spec)

    style_table = []
    for style in all_styles:
        row = [style]
        for spec in all_specs:
            if all_styles[style].get(spec) is None:
                row.append('N/A')
            else:
                row.append(all_styles[style][spec])
        style_table.append(row)

    style_table.sort(key=lambda x:x[0])
    return first_row, style_table