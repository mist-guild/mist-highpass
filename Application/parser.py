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

# Fetch the sheet
sheet = client.open('Mist Guild - Illidan Reagent Tracker').sheet1
reagent_df = pd.DataFrame(sheet.get_all_records())
idx = reagent_df.index[reagent_df['Character'] == 'based'][0]
reagent_df.at[idx,'item1']='new cascsac'
sheet.update([reagent_df.columns.values.tolist()] + reagent_df.values.tolist())


class Parser:
    def __init__(self) -> None:
        self.reagent_dictionary = sheet.get_all_records()
