import json

struc_paths = {
    'cpa': 'conf\struc_cpa.json',
    'process': 'conf\struc_process.json',
    'predata': 'conf\struc_predata.json',
    'postdata': 'conf\struc_postdata.json',
    'exp': 'conf\struc_exp.json'
}


def load_config_data(data_type):
    with open(struc_paths[data_type], 'r') as f:
        data = json.load(f)
    return data
