import datetime
import os

translate = {
    'Einfriergerät': 'Freezing device',
    'Abkühlrate': 'Cooling rate',
    'Konservierungsbehäler': 'Preservation container',
    'Lagerungstemp.': 'Storage temperature',
    'Lagerungsmedium': 'Storage medium',
    'Lagerungsdauer': 'Storage duration',
    'Auftautemp.': 'Thawing temperature',
    'Waschschritte': 'Washing steps',
    'Verdünnungsmedium': 'Dilution medium',
    'Veerdünnungsfaktor': 'Dilution factor'
}


def load_process_data(data_path, dict_body):
    try:
        dict_body["Process ID"] = os.path.basename(data_path).rsplit('.', 1)[0]
        with open(data_path, "r", encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if line != "" and ':' in line:
                    key, value = line.split(":", 1)
                    key = key.strip()
                    value = value.strip()
                    dict_body[translate[key]] = value

        with open('log\log_load.txt', 'a+') as file:
            file.write(
                f"{datetime.datetime.now()} SUCCESS ON LOADING PROCESS DATA: {os.path.basename(data_path)} \n")

    except Exception as e:
        with open('log\log_load.txt', 'a+') as file:
            file.write(
                f"{datetime.datetime.now()} ERROR ON LOADING PROCESS DATA: {os.path.basename(data_path)}: {e} \n")

    finally:
        return dict_body
