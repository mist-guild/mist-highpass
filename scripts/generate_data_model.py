import sys
import re
import os
import requests
import json
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

if __name__ == "__main__":
    # open txt file and write col to each line
    with open('./scripts/datamodel.txt', 'w') as f:
        for col in reagent_df.columns[1:]:
            col = col.lower()
            col = col.replace(' - ', '_')
            col = col.replace('-', '_')
            col = col.replace("'s", 's')
            col = col.replace(' ', '_')
            f.write(col + ' = db.Column(db.Integer, nullable=False)\n')
