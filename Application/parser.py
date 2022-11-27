import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# Authorize the API
scope = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file'
]
file_name = './Application/mist-highpass-65645aa69059.json'
creds = ServiceAccountCredentials.from_json_keyfile_name(file_name, scope)
client = gspread.authorize(creds)


class Parser:
    def __init__(self) -> None:
        sheet = client.open('Mist Guild - Illidan Reagent Tracker').sheet1
        reagent_df = pd.DataFrame(sheet.get_all_records())

    def update_reagent_count(self, character, item, count):
        idx = self.reagent_df.index[self.reagent_df['Character']
                                    == character][0]
        self.reagent_df.at[idx, item] = count
        self.sheet.update(
            [self.reagent_df.columns.values.tolist()] + self.reagent_df.values.tolist())
