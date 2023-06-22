import datetime
import os


def load_pp_data(data_path, dict_body):
    try:
        with open(data_path, "r", encoding='utf-8') as file:
            lines = file.readlines()
            dict_body['Machine'] = lines[0].strip()
            for line in lines:
                line = line.strip()
                if line != "" and ':' in line:
                    key, value = line.split(":", 1)
                    key = key.strip()
                    value = value.strip()
                    if key in dict_body.keys():
                        dict_body[key] = value

        with open('log\log_load.txt', 'a+') as file:
            file.write(
                f"{datetime.datetime.now()} SUCCESS ON LOADING PP DATA: {os.path.basename(data_path)} \n")

    except Exception as e:
        with open('log\log_load.txt', 'a+') as file:
            file.write(
                f"{datetime.datetime.now()} ERROR ON LOADING PP DATA: {os.path.basename(data_path)} \n")

    finally:
        return dict_body
