from .load_cryomicro_data import load_cryomicro_data
from .load_dsc_data import load_dsc_data
from .load_ftir_data import load_ftir_data
from .load_osmo_data import load_osmo_data
from .load_visc_data import load_visc_data

import datetime
import os


functions = {
    'DSC': load_dsc_data,
    'FTIR': load_ftir_data,
    'Osmolality': load_osmo_data,
    'Cryomicroscopy': load_cryomicro_data,
    'Viscosity': load_visc_data
}


def load_cpa_data(data_path, dict_body, cpa_id, child):
    try:
        dict_body["Center Node"]["CPA ID"] = cpa_id
        dict_body[child] = functions[child](data_path, dict_body[child])

        with open('log/log_load.txt', 'a+') as file:
            file.write(
                f"{datetime.datetime.now()} SUCCESS ON LOADING CPA DATA: {cpa_id} \n")
        return dict_body
    except Exception as e:
        with open('log/log_load.txt', 'a+') as file:
            file.write(
                f"{datetime.datetime.now()} ERROR ON LOADING CPA DATA: {cpa_id}: {e} \n")
        return 'error'
