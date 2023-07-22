import datetime
import os


def load_dsc_data(data_path, dict_body):
    try:
        if os.path.exists(data_path):
            with open(data_path, "r") as file:
                dict_body['DSC ID'] = os.path.basename(data_path).rsplit('.',1)[0]

                lines = file.readlines()
                for line in lines:
                    line = line.strip()
                    if line != "" and '#' not in line:
                        te, ti, dsc, sen, seg = line.split(";")
                        dict_body['Curve']["Temp./\u00b0C"].append(te.strip())
                        dict_body['Curve']["Time/min"].append(ti.strip())
                        dict_body['Curve']["DSC/(mW/mg)"].append(dsc.strip())
                        dict_body['Curve']["Sensit./(uV/mW)"].append(sen.strip())
                        dict_body['Curve']["Segment"].append(seg.strip())

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
