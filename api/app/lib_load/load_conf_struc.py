import json

struc_paths = {
    'CPA': 'conf/struc_cpa.json',
    'Process': 'conf/struc_process.json',
    'PreData': 'conf/struc_predata.json',
    'PostData': 'conf/struc_postdata.json'
}


def load_config_data(data_type):
    with open(struc_paths[data_type], 'r') as f:
        data = json.load(f)
    return data
