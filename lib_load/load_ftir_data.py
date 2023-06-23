import datetime
import os


def load_ftir_data(data_path, dict_body):
    try:
        dict_body['File ID'] = os.path.basename(data_path)
        read_data = False

        with open(data_path, "r", encoding='utf-8') as file:
            for line in file:
                if line.strip() == '#DATA':
                    read_data = True
                    continue
                if read_data:
                    line = line.strip()
                    if line != '':
                        wn, si = line.split()
                        dict_body["Curve"]["Wavenumber/cm^-1"].append(
                            wn.strip())
                        dict_body["Curve"]["Spectral intensity/A"].append(
                            si.strip())
            with open('log\log_load.txt', 'a+') as file:
                file.write(
                    f"{datetime.datetime.now()} SUCCESS ON LOADING FTIR DATA: {os.path.basename(data_path)} \n")

    except Exception as e:
        with open('log\log_load.txt', 'a+') as file:
            file.write(
                f"{datetime.datetime.now()} ERROR ON LOADING FTIR DATA: {os.path.basename(data_path)}: {e} \n")

    finally:
        return dict_body
