import datetime
import os

def load_dsc_data(data_path, dict_body):
    try:
        if os.path.exists(data_path):
            dict_body['DSC ID'] = os.path.basename(data_path).rsplit('.',1)[0]
            curve_head = []
            with open(data_path, "r", encoding="utf-8", errors='replace') as file:
                lines = file.readlines()
                for line in lines:
                    if '##' in line:
                        line = line.strip()[2:]
                        curve_head = line.split(';')
                        break
            with open(data_path, "r", encoding="utf-8", errors='replace') as file:
                for line in lines:        
                    line = line.strip()
                    if line != "":
                        if ';' in line and '#' not in line:
                            for i, point in enumerate(line.split(";")):
                                dict_body['Curve'][curve_head[i].replace('\ufffd', '\u00b0')].append(point.strip())
                        elif ':' in line:
                            key, value = line.split(":", 1)
                            key = key.strip()
                            if key[0] == '#':
                                key = key[1:]
                            value = value.strip()
                            # if key in dict_body.keys():
                            dict_body[key] = value
                        

            with open('log/log_load.txt', 'a+') as file:
                file.write(
                    f"{datetime.datetime.now()} SUCCESS ON LOADING DSC DATA: {os.path.basename(data_path)} \n")
        else:
            with open('log/log_load.txt', 'a+') as file:
                file.write(
                    f"{datetime.datetime.now()} NOT FOUND: {os.path.basename(data_path)} \n")

    except Exception as e:
        with open('log/log_load.txt', 'a+') as file:
            file.write(
                f"{datetime.datetime.now()} ERROR ON LOADING DSC DATA: {os.path.basename(data_path)}: {e} \n")

    finally:
        return dict_body
