import re
import os

def format_export():
    exp_file = open('export.txt','r')
    out_file = open('formatted_export.txt','w')
    
    count = 0
    items = {}
    qualities = {}
    for line in exp_file:
        if count == 0:
            count+=1
            continue
        
        line = line.split(',')
        qual = 'None'
        if 'Tier1' in line[1]:
            qual = 'Bronze'
        elif 'Tier2' in line[1]:
            qual = 'Silver'
        elif 'Tier3' in line[1]:
            qual = 'Gold'

        line[1] = re.sub('\|(.*?)\|a','', line[1]).strip()[1:-1]
        item = line[1].strip() + ' - ' + qual
        items[item] = int(line[0])

        money = int(line[0])
        copper = money % 100
        money //= 100
        silver = money % 100
        money //= 100

        out_file.write(f'{item:<50} {money:>10} {silver:>02} {copper:>02}\n')
        
        items[line[1]] = int(line[0])

    return items, qualities


def parse_mail(chars, items, qualities, file_name):
    mail = open(file_name, 'r')

    curChar = ''
    
    for line in mail:
        # If we have a name
        if not line.startswith('-'):
            curChar = line.strip()
            if curChar not in chars:
                chars[curChar] = {}
                chars[curChar]['money'] = 0

        # If we have an item
        elif line.startswith('-'):
            line = line.split('*')
            
            # Get the Name
            item_name = line[0][1:]

            # Get the Quantity and Quality
            quantity = 0
            quality = ' - None'
            if len(line) == 2:
                quantity = int(line[1])
            elif len(line) == 3:
                quality = ' - ' + line[1]
                quantity = int(line[2])
            item_name += quality

            # Check for BoEs
            if item_name in items:
                chars[curChar]['money'] += items[item_name] * quantity
            else:
                if item_name not in chars[curChar]:
                    chars[curChar][item_name] = 0
                chars[curChar][item_name] += quantity

    return chars


def write_to_file(chars):
    out = open('compiled.txt','w')        
    headers = '{0:<12} {1:<16}\t{2}\n'.format('Name', 'Gold', 'BoEs')
    out.write(headers)
    for char in chars:
        money = chars[char]['money']
        copper = money % 100
        money //= 100
        silver = money % 100
        money //= 100
        out.write(f'{char:<12} {money:>10} {silver:<02} {copper:<02}\t')
        for item in chars[char]:
            if item != 'money':
                out.write(item + ' (' + str(chars[char][item]) + '), ')
        out.write('\n')


if __name__ == '__main__':
    items, qualities = format_export()
    dir = os.curdir + '/data'
    chars = {}
    for file_name in os.listdir(os.curdir + '/data'):
        parse_mail(chars, items, qualities, os.curdir + '/data/'+file_name)
    write_to_file(chars)