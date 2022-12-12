

def gen_shopping_list():
    input_file = open('items.txt', 'r')
    out = open('list.txt', 'w')

    items = []
    for line in input_file:
        line = line.split('-')
        item = line[0].strip()
        if item not in items:
            items.append(item)

    # Setup the items list
    out.write('["items"] = {\n')
    count = 1
    for item in items:
        out.write('\t"' + item + ';;0;0;0;0;0;0;0;0;", -- [' + str(count) + ']\n')
        count += 1
    out.write('},\n')

    out.write('["name"] = "Mist Contest",\n')
    out.write('["isTemporary"] = false,')

    # Close files
    input_file.close()
    out.close()


if __name__ == '__main__':
    gen_shopping_list()