import datetime
import os
import pandas as pd
from lib_load import load_cpa_data, load_pre_data, load_post_data, load_process_data, load_config_data, load_exp_data
from lib_save import dict_to_neo_process, dict_to_neo_cpa, dict_to_neo_predata, dict_to_neo_postdata, dict_to_neo_expriment, connect_to_db


GRAPH_CRYO = connect_to_db('cryo')
GRAPH_CPA = connect_to_db('cpa')


class FeedIntoNeo4j:
    def __init__(self, data_type, data_path):
        self.data_type = data_type
        self.data_path = data_path

    def load_one(self):
        if self.data_type == 'CPA':
            config_data = load_config_data(self.data_type)
            loaded_data = load_cpa_data(self.data_path, config_data)
        elif self.data_type == 'Process':
            config_data = load_config_data(self.data_type)
            loaded_data = load_process_data(self.data_path, config_data)
        elif self.data_type == 'PreData':
            config_data = load_config_data(self.data_type)
            loaded_data = load_pre_data(self.data_path, config_data)
        elif self.data_type == 'PostData':
            config_data = load_config_data(self.data_type)
            loaded_data = load_post_data(self.data_path, config_data)
        elif self.data_type == 'Experiment':
            loaded_data = load_exp_data(self.data_path)

        return loaded_data

    def feed_to_neo4j(self):
        loaded_data = self.load_one()
        if self.data_type == 'CPA':
            child = self.data_path.split('/')[3]
            return dict_to_neo_cpa(GRAPH_CPA, loaded_data, child)
        elif self.data_type == 'Process':
            return dict_to_neo_process(GRAPH_CPA, loaded_data)
        elif self.data_type == 'PreData':
            return dict_to_neo_predata(GRAPH_CRYO, loaded_data)
        elif self.data_type == 'PostData':
            return dict_to_neo_postdata(GRAPH_CRYO, loaded_data)
        elif self.data_type == 'Experiment':
            experiment_id = os.path.basename(self.data_path).rsplit(".",1)[0]
            return dict_to_neo_expriment(GRAPH_CRYO, loaded_data, experiment_id)
