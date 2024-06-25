import datetime
import os


def load_osmo_data(data_path, dict_body):
    try:
        if os.path.exists(data_path):
            with open('log/log_load.txt', 'a+') as file:
                file.write(
                    f"{datetime.datetime.now()} SUCCESS ON LOADING OSMO DATA: {os.path.basename(data_path)} \n")
        else:
            with open('log/log_load.txt', 'a+') as file:
                file.write(
                    f"{datetime.datetime.now()} NOT FOUND: {os.path.basename(data_path)} \n")

    except Exception as e:
        with open('log/log_load.txt', 'a+') as file:
            file.write(
                f"{datetime.datetime.now()} ERROR ON LOADING OSMO DATA: {os.path.basename(data_path)}: {e} \n")

    finally:
        return dict_body
