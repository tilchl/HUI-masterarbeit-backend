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

def load_process_data(data_path, json_body):
    with open(data_path, "r", encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            json_body[translate[key]] = value
    return json_body