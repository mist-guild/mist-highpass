import sys
import re
import os
import requests
import json
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# Authorize the API
scope = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file'
]
file_name = resource_path('./mist-highpass-65645aa69059.json')
creds = ServiceAccountCredentials.from_json_keyfile_name(file_name, scope)
client = gspread.authorize(creds)


class Parser:
    def __init__(self) -> None:
        self.sheet = client.open('Mist Guild - Illidan Reagent Tracker').sheet1
        self.reagent_df = pd.DataFrame(self.sheet.get_all_records())
        self.__check_and_fix_blank()

    def __check_and_fix_blank(self):
        # TODO: Populate the sheet with the correct headers
        if self.reagent_df.empty:
            self.reagent_df = self.reagent_df.append(
                {'Character': "Remove Me"}, ignore_index=True)

    def __update_reagent_count(self, character, item, count):
        # get index
        idx = self.reagent_df.index[self.reagent_df['Character']
                                    == character][0]

        # ghetto log
        print(f"Updating {character} {item} to {count}")
        print("Index: ", idx)
        print("--------------------")

        # update dataframe
        if self.reagent_df.at[idx, item] == 0 or self.reagent_df.at[idx, item] is None:
            self.reagent_df.at[idx, item] = count
        else:
            self.reagent_df.at[idx, item] = int(
                self.reagent_df.at[idx, item]) + int(count)

    def __add_character(self, character):
        self.reagent_df = self.reagent_df.append(
            {'Character': character}, ignore_index=True)
        self.reagent_df = self.reagent_df.fillna(0)

    def __build_and_send_update_request(self):
        reagent_json = self.reagent_df.to_dict(orient='records')
        for character_json in reagent_json:
            requests.put(f"https://mistguild.pythonanywhere.com/reagent/{character_json['Character']}",
                         data=json.dumps(character_json),
                         headers={'Content-Type': 'application/json'})

    def __publish_updates(self):
        self.__build_and_send_update_request()
        self.sheet.update(
            [self.reagent_df.columns.values.tolist()] + self.reagent_df.values.tolist())

    def validate_input(self, input):
        # base case
        if input == "":
            return False, "Empty input!"

        # iterate through and validate
        input = input.splitlines()
        for line in input:
            if not re.fullmatch(r'-[\w\s\'\-\:]+.\*\w+\*\d+', line) and not re.fullmatch(r'-[\w\s\'\-\:]+.\*\d+', line) and not re.fullmatch(r'[A-Za-zŽžÀ-ÿ]{1,12}', line):
                return False, line
        return True, "success"

    def parse(self, input):
        input = input.splitlines()
        current_character = None
        with open("ignored.txt", 'w') as f:
            for line in input:
                line_split = line.split('*')
                item = line_split[0][1:]

                if re.fullmatch(r'-[\w\s\'\-\:]+.\*\w+\*\d+', line):
                    # reformat reagent
                    item = f"{item} - {line_split[1]}"
                    count = line_split[2]

                    # update reagent count
                    if item in self.reagent_df.columns:
                        self.__update_reagent_count(
                            current_character, item, count)
                        continue
                    f.write(f"{line}\n")
                elif re.fullmatch(r'-[\w\s\'\-\:]+.\*\d+', line):
                    # get count
                    count = line_split[1]

                    # update reagent count
                    if item in self.reagent_df.columns:
                        self.__update_reagent_count(
                            current_character, item, count)
                        continue
                    f.write(f"{line}\n")
                else:
                    # assign new character
                    current_character = line
                    if current_character not in self.reagent_df['Character'].values:
                        self.__add_character(current_character)
                        continue
                    f.write(f"{line}\n")
        self.__publish_updates()
