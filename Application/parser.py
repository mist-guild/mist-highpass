import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint

# Authorize the API
scope = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file'
]
file_name = './Application/mist-highpass-65645aa69059.json'
creds = ServiceAccountCredentials.from_json_keyfile_name(file_name, scope)
client = gspread.authorize(creds)

#Fetch the sheet
sheet = client.open('Mist Guild - Illidan Reagent Tracker').sheet1
python_sheet = sheet.get_all_records()
print(len(python_sheet))

class Parser:
    pass
