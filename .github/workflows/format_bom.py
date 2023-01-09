print('-FORMATTING BOM .csv')

import csv, collections

def write_part_to_csv(name, this_part, old_part, writer):
    writer.writerow({
        'type': this_part['type'],
        'category': old_part.get('category', ''),
        'cad_name': name,
        'amount': this_part['amount'],
        'single_price': old_part.get('single_price', '---'),
        'price': old_part.get('price', '---'),
        'link': old_part.get('link', '---'),
        'alt_link': old_part.get('alt_link', '---'),
        'note': old_part.get('note', this_part['note'])})

in_csv = {}
try:
    with open('./Parts/bom.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            if row['type'] != '':
                in_csv[row['cad_name']] = row
except:
    pass

parts = in_csv

# create csv
csvfile = open('./Parts/bom.csv', 'w', newline='')
fieldnames = ['type', 'category', 'cad_name', 'amount',
                'single_price', 'price', 'link', 'alt_link', 'note']
writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',')

writer.writeheader()

categories = {}
for part in in_csv:
    if in_csv[part]['category'] not in categories and in_csv[part]['category'] != '':
        categories[in_csv[part]['category']] = in_csv[part]['type']
categories = collections.OrderedDict(
    sorted(categories.items()))  # sort cats

parts = collections.OrderedDict(sorted(parts.items()))  # sort parts

# printed parts with category
for category in categories:
    if categories[category] == 'printed':
        for part in parts:
            if parts[part]['type'] == 'printed' and part in in_csv and in_csv[part]['category'] == category:
                write_part_to_csv(part, parts[part], in_csv.get(part, {}), writer)

# printed parts without category
for part in parts:
    if parts[part]['type'] == 'printed':
        if part in in_csv and in_csv[part]['category'] != '': continue
        write_part_to_csv(part, parts[part], in_csv.get(part, {}), writer)


# empty row
writer.writerow({})

# mechanical parts with category
for category in categories:
    if categories[category] == 'mechanical':
        for part in parts:
            if parts[part]['type'] == 'mechanical' and part in in_csv and in_csv[part]['category'] == category:
                write_part_to_csv(part, parts[part], in_csv.get(part, {}), writer)

# mechanical parts without category
for part in parts:
    if parts[part]['type'] == 'mechanical':
        if part in in_csv and in_csv[part]['category'] != '': continue
        write_part_to_csv(part, parts[part], in_csv.get(part, {}), writer)

csvfile.close()