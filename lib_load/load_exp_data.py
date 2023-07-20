import datetime
import os
import json


def load_exp_data(data_path):
    try:
        if os.path.exists(data_path):
            with open(data_path, 'r') as f:
                data = json.load(f)

            with open('log/log_load.txt', 'a+') as file:
                file.write(
                    f"{datetime.datetime.now()} SUCCESS ON LOADING EXP DATA: {os.path.basename(data_path)} \n")
            return data

        else:
            with open('log/log_load.txt', 'a+') as file:
                file.write(
                    f"{datetime.datetime.now()} NOT FOUND: {os.path.basename(data_path)} \n")
            return {}

    except Exception as e:
        with open('log/log_load.txt', 'a+') as file:
            file.write(
                f"{datetime.datetime.now()} ERROR ON LOADING EXP DATA: {os.path.basename(data_path)}: {e} \n")
        return {}
