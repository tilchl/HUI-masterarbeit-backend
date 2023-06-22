from py2neo import Graph
import json
import pandas
import time
import copy
from .load_pre_post_data import load_pp_data
from .load_process import load_process_data
from ...lib_save.json_to_neo import json_to_neo


class FeedOneExp:
    def __init__(self, index, pre_data_path, post_data_path, process_path, cpa):
        self.config_account_path = 'development_cryo/config/config_account.json'
        self.config_cryo_db_path = 'development_cryo/config/config_cryo_db.json'
        self.index = index
        self.pre_data_path = pre_data_path
        self.post_data_path = post_data_path
        self.process_path = process_path
        self.cpa = cpa
        self.graph = self.connect_to_db()
        self.config_data = self.load_config_data()

    def connect_to_db(self):
        with open(self.config_account_path, 'r') as f:
            data = json.load(f)
        graph = Graph(data['profile'], password=data['password'])
        return graph

    def load_config_data(self):
        with open(self.config_cryo_db_path, 'r') as f:
            data = json.load(f)
        if data['PostData'] == '$PreData':
            data['PostData'] = copy.deepcopy(data['PreData'])
        return data

    def load_one_experiment(self):
        loaded_data = self.config_data
        loaded_data['PreData'] = load_pp_data(
            self.pre_data_path, self.config_data['PreData'])
        loaded_data['PostData'] = load_pp_data(
            self.post_data_path, self.config_data['PostData'])
        loaded_data['CPA'] = self.cpa
        loaded_data['Process'] = load_process_data(
            self.process_path, self.config_data['Process'])
        return loaded_data

    def feed_to_neo4j(self):
        loaded_data = self.load_one_experiment()
        json_to_neo(self.graph, loaded_data, self.index)


def get_continue_index(df, load_from):
    if load_from == 'start':
        return 0
    else:
        if len(df.index[df['index'] == load_from]) == 1:
            return (df.index[df['index'] == load_from])[0]
        else:
            return 'OverflowError'


def feed_all_exps(exps_log_path, load_from):
    experiments_df = pandas.read_csv(exps_log_path)

    continue_index = get_continue_index(experiments_df, load_from)

    if continue_index == 'OverflowError':
        print(f'\nError: {load_from} does not exist.\n')
    else:
        if continue_index == 0:
            first_exp = experiments_df['index'][0]
            print(f'\nStart: from {first_exp}.\n')
        else:
            print(f'\nContinue: from {load_from}.\n')
        start = time.perf_counter()
        overall_time = 0
        for i, line in experiments_df.iterrows():
            if i < continue_index:
                continue
            else:
                FeedOneExp(index=experiments_df['index'][i],
                           pre_data_path=experiments_df['pre_data'][i],
                           post_data_path=experiments_df['post_data'][i],
                           process_path=experiments_df['process'][i],
                           cpa=experiments_df['cpa'][i]).feed_to_neo4j()
                # progress bar
                finish = '▓' * int((i+1)*(50/len(experiments_df)))
                need_do = '-' * (50-int((i+1)*(50/len(experiments_df))))
                dur = time.perf_counter() - start
                overall_time = overall_time + dur
                print("\r{}/{}|{}{}|{:.2f}s".format((i+1), len(experiments_df),
                                                    finish, need_do, overall_time), end='', flush=True)

        dur = time.perf_counter() - start
        print('')
        print(f'\nEnd: overall time {dur:.2f}s, average time {overall_time/(i+1):.2f}s.\n')


from py2neo import Graph
import json
import os
import time
from .load_dsc_data import load_dsc_data
from .load_ftir_data import load_ftir_data
from .load_cryomicro_data import load_cryomicro_data
from .load_osmo_data import load_osmo_data
from .load_visc_data import load_visc_data
from ...lib_save.json_to_neo_cpa import json_to_neo


class FeedOneExp:
    def __init__(self, cpa_index, cpa_dir_path):
        self.config_account_path = 'development_cpa/config/config_account.json'
        self.config_cryo_db_path = 'development_cpa/config/config_cpa_db.json'
        self.cpa_dir_path = cpa_dir_path
        self.cpa_index = cpa_index
        self._path = self.get_paths()
        self.graph = self.connect_to_db()
        self.config_data = self.load_config_data()

    def connect_to_db(self):
        with open(self.config_account_path, 'r') as f:
            data = json.load(f)
        graph = Graph(data['profile'], password=data['password'])
        return graph

    def load_config_data(self):
        with open(self.config_cryo_db_path, 'r') as f:
            data = json.load(f)
        return data
    
    def get_paths(self):
        return {
            "dsc_path": f'{self.cpa_dir_path}/{self.cpa_index}/DSC/' + os.listdir(f'{self.cpa_dir_path}/{self.cpa_index}/DSC')[0],
            "ftir_path": f'{self.cpa_dir_path}/{self.cpa_index}/FTIR/' + os.listdir(f'{self.cpa_dir_path}/{self.cpa_index}/FTIR')[0],
            "cryomicro_path": '',
            "osmo_path": '',
            "visc_path": ''
        }

    def load_one_experiment(self):
        loaded_data = self.config_data
        loaded_data['CPA ID'] = self.cpa_index
        loaded_data['DSC'] = load_dsc_data(
            self._path['dsc_path'], self.config_data['DSC'])
        loaded_data['FTIR'] = load_ftir_data(
            self._path['ftir_path'], self.config_data['FTIR'])
        loaded_data['Cryomicroscopy'] = load_cryomicro_data(
            self._path['cryomicro_path'], self.config_data['Cryomicroscopy'])
        loaded_data['Osmolality'] = load_osmo_data(
            self._path['osmo_path'], self.config_data['Osmolality'])
        loaded_data['Viscosity'] = load_visc_data(
            self._path['visc_path'], self.config_data['Viscosity'])

        return loaded_data

    def feed_to_neo4j(self):
        loaded_data = self.load_one_experiment()
        json_to_neo(self.graph, loaded_data)


def feed_all_exps(cpa_dir_path):
    cpa_dirs = os.listdir(cpa_dir_path)
    print(f'\nStart: {len(cpa_dirs)} exist.')

    start = time.perf_counter()
    overall_time = 0
    for i, dir_name in enumerate(cpa_dirs):
        if i == 0:
            FeedOneExp(cpa_index=dir_name,
                        cpa_dir_path=cpa_dir_path).feed_to_neo4j()
        # progress bar
        finish = '▓' * int((i+1)*(50/len(cpa_dirs)))
        need_do = '-' * (50-int((i+1)*(50/len(cpa_dirs))))
        dur = time.perf_counter() - start
        overall_time = overall_time + dur
        print("\r{}/{}|{}{}|{:.2f}s".format((i+1), len(cpa_dirs),
                                            finish, need_do, overall_time), end='', flush=True)

    dur = time.perf_counter() - start
    print('')
    print(f'\nEnd: overall time {dur:.2f}s, average time {overall_time/(i+1):.2f}s.\n')
