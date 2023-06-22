import os


def load_ftir_data(data_path, json_body):
    json_body['File_name'] = os.path.basename(data_path)
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
                    json_body["Curve"]["Wavenumber/cm^-1"].append(wn.strip())
                    json_body["Curve"]["Spectral intensity/A"].append(si.strip())

    return json_body
