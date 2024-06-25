import datetime
import os


def load_pre_data(data_path, dict_body):
    try:
        dict_body["Sample ID"] = os.path.basename(data_path).rsplit('.', 1)[0]
        with open(data_path, "r", encoding='utf-8') as file:
            lines = file.readlines()
            dict_body['Machine'] = lines[0].strip()
            for line in lines:
                line = line.strip()
                if line != "" and ':' in line:
                    key, value = line.split(":", 1)
                    key = key.strip()
                    value = value.strip()
                    # if key in dict_body.keys():
                    dict_body[key] = value

        with open('log/log_load.txt', 'a+') as file:
            file.write(
                f"{datetime.datetime.now()} SUCCESS ON LOADING PRE DATA: {os.path.basename(data_path)} \n")

    except Exception as e:
        with open('log/log_load.txt', 'a+') as file:
            file.write(
                f"{datetime.datetime.now()} ERROR ON LOADING PRE DATA: {os.path.basename(data_path)}: {e} \n")

    finally:
        return dict_body
