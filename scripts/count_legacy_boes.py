import re


with open('./scripts/output-new.txt', 'r') as f:
    # Read the file into a list of lines
    lines = f.readlines()
    map = {}
    current_character = None
    for line in lines:
        if re.fullmatch(r'-[\w\s\'\-\:]+.\*\w+\*\d+\n', line):
            continue
        elif re.fullmatch(r'-[\w\s\'\-\:]+.\*\d+\n', line):
            lines_split = line.split("*")
            item = lines_split[0]
            if len(item.split(" ")) >= 4:
                map[current_character] += int(lines_split[1])
        else:
            current_character = line
            map[current_character] = 0
    print(map)
