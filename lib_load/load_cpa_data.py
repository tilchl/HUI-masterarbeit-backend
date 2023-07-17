from .load_cryomicro_data import load_cryomicro_data
from .load_dsc_data import load_dsc_data
from .load_ftir_data import load_ftir_data
from .load_osmo_data import load_osmo_data
from .load_visc_data import load_visc_data

import datetime
import os


translate = {
    'dsc': 'DSC',
    'ftir': 'FTIR',
    'osmo': 'Osmolality',
    'cryomicro': 'Cryomicroscopy',
    'visc': 'Viscosity'
}


def path(cpa_dir_path, data_type):
    dir_path = cpa_dir_path + (f'/{translate[data_type]}' if '/' in cpa_dir_path else f'/{translate[data_type]}')
    if os.path.exists(dir_path):
        file_name = os.listdir(dir_path)[0]
    else:
        file_name = 'default.txt'
    return dir_path + ('/' if '/' in cpa_dir_path else '/') + file_name


def get_paths(cpa_dir_path):
   return {k: path(cpa_dir_path, k) for (k, v) in translate.items()}


def load_cpa_data(cpa_dir_path, dict_body):
    try:
        cpa_id = cpa_dir_path.rsplit('/' if '/' in cpa_dir_path else '/', 1)[1]
        dict_body["Center Node"]["CPA ID"] = cpa_id
        paths = get_paths(cpa_dir_path)
        dict_body["DSC"] = load_dsc_data(paths['dsc'], dict_body["DSC"])
        dict_body["FTIR"] = load_ftir_data(paths['ftir'], dict_body["FTIR"])
        dict_body["Osmolality"] = load_osmo_data(paths['osmo'], dict_body["Osmolality"])
        dict_body["Cryomicroscopy"] = load_cryomicro_data(paths['cryomicro'], dict_body["Cryomicroscopy"])
        dict_body["Viscosity"] = load_visc_data(paths['visc'], dict_body["Viscosity"])

        with open('log/log_load.txt', 'a+') as file:
            file.write(
                f"{datetime.datetime.now()} SUCCESS ON LOADING CPA DATA: {cpa_id} \n")
        return dict_body
    except Exception as e:
        with open('log/log_load.txt', 'a+') as file:
            file.write(
                f"{datetime.datetime.now()} ERROR ON LOADING CPA DATA: {cpa_id}: {e} \n")
        return 'error'
