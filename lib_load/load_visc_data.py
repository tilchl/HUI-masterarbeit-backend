import datetime
import os


def load_visc_data(data_path, dict_body):
    try:
        with open('log\log_load.txt', 'a+') as file:
            file.write(
                f"{datetime.datetime.now()} SUCCESS ON LOADING VISC DATA: {os.path.basename(data_path)} \n")

    except Exception as e:
        with open('log\log_load.txt', 'a+') as file:
            file.write(
                f"{datetime.datetime.now()} ERROR ON LOADING VISC DATA: {os.path.basename(data_path)} \n")

    finally:
        return dict_body
