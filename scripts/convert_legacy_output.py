import re
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file'
]
file_name = './scripts/mist-highpass-65645aa69059.json'
creds = ServiceAccountCredentials.from_json_keyfile_name(file_name, scope)
client = gspread.authorize(creds)

sheet = client.open('Mist Guild - Illidan Reagent Tracker').sheet1
reagent_df = pd.DataFrame(sheet.get_all_records())

with open('./scripts/output.txt', 'r') as legacy_output, open('./scripts/output-new.txt', 'w') as output:
    lines = legacy_output.readlines()
    for line in lines:
        if re.fullmatch('\w+', line):
            # name
            output.write(line)
        else:
            split_by_space = line.split(" ")
            if split_by_space[0] in ["-Bronze", "-Silver", "-Gold"]:
                # reagent
                quality = split_by_space[0].replace("-", "")
                # remove quality from line
                line = line.replace(f"{quality} ", "")
                split_by_star = line.split("*")
                output.write(f"{split_by_star[0]}*{quality}*{split_by_star[1]}")
            else:
                output.write(line)
