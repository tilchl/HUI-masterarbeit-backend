import os


def load_dsc_data(data_path, json_body):
    with open(data_path, "r") as file:
        json_body['File_name'] = os.path.basename(data_path)
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            if line != "":
                if ':' in line:
                    key, value = line.split(":", 1)
                    key = key.strip()[1:]
                    value = value.strip()
                    json_body['Log'][key] = value
                else:
                    if '/' in line:
                        pass
                    else:
                        te, ti, dsc, sen, seg = line.split(";")
                        json_body['Curve']["Temp./\u00b0C"].append(te.strip())
                        json_body['Curve']["Time/min"].append(ti.strip())
                        json_body['Curve']["DSC/(mW/mg)"].append(dsc.strip())
                        json_body['Curve']["Sensit./(uV/mW)"].append(sen.strip())
                        json_body['Curve']["Segment"].append(seg.strip())

    return json_body
