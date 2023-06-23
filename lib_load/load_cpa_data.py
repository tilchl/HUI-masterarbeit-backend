from .load_cryomicro_data import load_cryomicro_data
from .load_dsc_data import load_dsc_data
from .load_ftir_data import load_ftir_data
from .load_osmo_data import load_osmo_data
from .load_visc_data import load_visc_data

import datetime
import os


def get_path(cpa_dir_path):
    return {
        'dsc': (cpa_dir_path + '/' if '/' in cpa_dir_path else '\\') + 'DSC' + os.listdir((cpa_dir_path + '/' if '/' in cpa_dir_path else '\\') + 'DSC')[0], 
        'ftir': (cpa_dir_path + '/' if '/' in cpa_dir_path else '\\') + 'DSC' + os.listdir((cpa_dir_path + '/' if '/' in cpa_dir_path else '\\') + 'FTIR')[0], 
        'osmo': (cpa_dir_path + '/' if '/' in cpa_dir_path else '\\') + 'DSC' + os.listdir((cpa_dir_path + '/' if '/' in cpa_dir_path else '\\') + 'OSMO')[0], 
        'cryomicro': (cpa_dir_path + '/' if '/' in cpa_dir_path else '\\') + 'DSC' + os.listdir((cpa_dir_path + '/' if '/' in cpa_dir_path else '\\') + 'CRYOMICRO')[0], 
        'visc': (cpa_dir_path + '/' if '/' in cpa_dir_path else '\\') + 'DSC' + os.listdir((cpa_dir_path + '/' if '/' in cpa_dir_path else '\\') + 'VISC')[0], 
    }

def load_cpa_data(cpa_dir_path, dict_body):
    try:
        cpa_id = cpa_dir_path.rsplit('/' if '/' in cpa_dir_path else '\\', 1)[1]
        dict_body["Center Node"]["CPA ID"] = cpa_id
        paths = get_path(cpa_dir_path)
        load_dsc_data(paths['dsc'], dict_body["DSC"])
        load_ftir_data(paths['ftir'], dict_body["FTIR"])
        load_osmo_data(paths['osmo'], dict_body["Osmolality"])
        load_cryomicro_data(paths['cryomicro'], dict_body["Cryomicroscopy"])
        load_visc_data(paths['visc'], dict_body["Viscosity"])

        with open('log\log_load.txt', 'a+') as file:
            file.write(
                f"{datetime.datetime.now()} SUCCESS ON LOADING CPA DATA: {cpa_id} \n")

    except Exception as e:
        with open('log\log_load.txt', 'a+') as file:
            file.write(
                f"{datetime.datetime.now()} ERROR ON LOADING CPA DATA: {cpa_id}: {e} \n")

    finally:
        return dict_body
