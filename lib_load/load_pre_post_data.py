def load_pp_data(data_path, json_body):
    with open(data_path, "r", encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            if line != "" and ':' in line:
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()

                if value:
                    if key == 'Analysis version':
                        json_body['Log']['User'][key] = value
                    elif 'Date' in key:
                        json_body['Log']['Time'][key] = value
                    else:
                        if key in json_body:
                            if value:
                                json_body[key] = value
                        else:
                            for category in json_body.values():
                                if category:
                                    if key in category:
                                        category[key] = value
                                
    return json_body