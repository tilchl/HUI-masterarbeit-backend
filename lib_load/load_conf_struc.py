import json
import copy

CONFIG_STRUC_CPA_PATH = 'conf\struc_cpa.json'
CONFIG_STRUC_CRYO_PATH = 'conf\struc_cryo.json'
CONFIG_STRUC_PROCESS_PATH = 'conf\struc_process.json'


def load_config_data(data_type):
    if data_type == 'cryo':
        with open(CONFIG_STRUC_CRYO_PATH, 'r') as f:
            data = json.load(f)
        if data['PostData'] == '$PreData':
            data['PostData'] = copy.deepcopy(data['PreData'])

    elif data_type == 'cpa':
        with open(CONFIG_STRUC_CPA_PATH, 'r') as f:
            data = json.load(f)

    elif data_type == 'process':
        with open(CONFIG_STRUC_PROCESS_PATH, 'r') as f:
            data = json.load(f)

    return data
