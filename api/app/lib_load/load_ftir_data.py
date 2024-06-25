import datetime
import os


def load_ftir_data(data_path, dict_body):
    try:
        if os.path.exists(data_path):
            dict_body['FTIR ID'] = os.path.basename(
                data_path).rsplit('.', 1)[0]
            read_data = False
            curve_head = []
            with open(data_path, "r", encoding='utf-8') as file:
                lines = file.readlines()
                for line in lines:
                    if '##' in line:
                        line = line.strip()[2:]
                        curve_head = line.split('\t')
                        break
            if curve_head == []:
                curve_head = ['Wavenumber/cm^-1', 'Absorbance/A']
            with open(data_path, "r", encoding='utf-8') as file:
                lines = file.readlines()
                for line in lines:
                    if line.strip() == '#DATA':
                        read_data = True
                        continue
                    if read_data:
                        line = line.strip()
                        if line != "" and '##' not in line:
                            if ':' not in line:
                                for i, point in enumerate(line.split("\t")):
                                    dict_body['Curve'][curve_head[i]].append(
                                        point.strip())
                            elif ':' in line:
                                key, value = line.split(":", 1)
                                key = key.strip()
                                value = value.strip()
                                # if key in dict_body.keys():
                                dict_body[key] = value
            with open('log/log_load.txt', 'a+') as file:
                file.write(
                    f"{datetime.datetime.now()} SUCCESS ON LOADING CRYOMICRO DATA: {os.path.basename(data_path)} \n")

        else:
            with open('log/log_load.txt', 'a+') as file:
                file.write(
                    f"{datetime.datetime.now()} NOT FOUND: {os.path.basename(data_path)} \n")

    except Exception as e:
        with open('log/log_load.txt', 'a+') as file:
            file.write(
                f"{datetime.datetime.now()} ERROR ON LOADING FTIR DATA: {os.path.basename(data_path)}: {e} \n")

    finally:
        return dict_body
