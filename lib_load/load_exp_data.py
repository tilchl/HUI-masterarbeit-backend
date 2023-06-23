import datetime
import os


def load_exp_data(data_path, dict_body):
    try:
        experiment_id = (data_path.rsplit('/' if '/' in data_path else '\\', 1)[1]).rsplit('.', 1)[0]
        dict_body["Experiment ID"] = experiment_id
        with open(data_path, "r", encoding='utf-8') as file:
            lines = file.readlines()
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
                f"{datetime.datetime.now()} SUCCESS ON LOADING EXP DATA: {experiment_id} \n")

    except Exception as e:
        with open('log\log_load.txt', 'a+') as file:
            file.write(
                f"{datetime.datetime.now()} ERROR ON LOADING EXP DATA: {experiment_id}: {e} \n")

    finally:
        return dict_body
