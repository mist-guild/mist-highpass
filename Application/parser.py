import re
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Authorize the API
scope = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file'
]
file_name = './application/mist-highpass-65645aa69059.json'
creds = ServiceAccountCredentials.from_json_keyfile_name(file_name, scope)
client = gspread.authorize(creds)


class Parser:
    def __init__(self) -> None:
        self.sheet = client.open('Mist Guild - Illidan Reagent Tracker').sheet1
        self.reagent_df = pd.DataFrame(self.sheet.get_all_records())
        self.__check_and_fix_blank()

    def __update_reagent_count(self, character, item, count):
        idx = self.reagent_df.index[self.reagent_df['Character']
                                    == character][0]
        self.reagent_df.at[idx, item] = count

    def __check_and_fix_blank(self):
        # TODO: Populate the sheet with the correct headers
        if self.reagent_df.empty:
            self.reagent_df = self.reagent_df.append(
                {'Character': "Remove Me"}, ignore_index=True)

    def __add_character(self, character):
        self.reagent_df = self.reagent_df.append(
            {'Character': character}, ignore_index=True)
        self.reagent_df = self.reagent_df.fillna(0)
        self.__publish_updates()

    def __publish_updates(self):
        self.sheet.update(
            [self.reagent_df.columns.values.tolist()] + self.reagent_df.values.tolist())

    def validate_input(self, input):
        # base case
        if input == "":
            return False

        # iterate through and validate
        input = input.splitlines()
        for line in input:
            if not re.match('-[\w\s]+.\*\w+\*\d+', line) and not re.match('[A-Za-zŽžÀ-ÿ]{1,12}', line):
                return False, line
        return True, "success"

    def parse(self, input):
        # iterate through and parse
        input = input.splitlines()
        current_character = None
        for line in input:
            if re.match('-[\w\s]+.\*\w+\*\d+', line):
                # reformat reagent
                line_split = line.split('*')
                line_split[0] = line_split[0][1:]
                item = f"{line_split[0]} - {line_split[1]}"
                count = line_split[2]

                # update reagent count
                if item in self.reagent_df.columns:
                    print(item)
                    self.__update_reagent_count(current_character, item, count)
            else:
                current_character = line
                if current_character not in self.reagent_df['Character'].values:
                    self.__add_character(current_character)
        self.__publish_updates()
