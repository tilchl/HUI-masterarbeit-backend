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
            cpa_id = self.data_path.split('/')[2]
            child = self.data_path.split('/')[3]
            loaded_data = load_cpa_data(self.data_path, config_data, cpa_id, child)
        elif self.data_type == 'Process':
            config_data = load_config_data(self.data_type)
            loaded_data = load_process_data(self.data_path, config_data)
        elif self.data_type == 'PreData':
            config_data = load_config_data(self.data_type)
            loaded_data = load_pre_data(self.data_path, config_data)
        elif self.data_type == 'PostData':
            config_data = load_config_data(self.data_type)
            loaded_data = load_post_data(self.data_path, config_data)
        elif self.data_type == 'ExperimentCreate':
            loaded_data = load_exp_data(self.data_path)
        elif self.data_type == 'ExperimentUpload':
            if self.data_path.rsplit('.', 1)[-1] == 'json':
                loaded_data = load_exp_data(self.data_path)
            else:
                if self.data_path.split('/')[4].lower() == 'predata' or self.data_path.split('/')[5].lower() == 'predata':
                    config_data = load_config_data('PreData')
                    loaded_data = load_pre_data(self.data_path, config_data)
                if self.data_path.split('/')[5].lower() == 'postdata':
                    config_data = load_config_data('PostData')
                    loaded_data = load_post_data(self.data_path, config_data)
                if self.data_path.split('/')[5].lower() in ['process', 'prozess']:
                    config_data = load_config_data('Process')
                    loaded_data = load_process_data(self.data_path, config_data)
                if self.data_path.split('/')[5].lower() == 'cpa':
                    config_data = load_config_data('CPA')
                    cpa_id = self.data_path.split('/')[6]
                    child = self.data_path.split('/')[7]
                    loaded_data = load_cpa_data(self.data_path, config_data, cpa_id, child)
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
        elif self.data_type == 'ExperimentCreate':
            experiment_id = os.path.basename(self.data_path).rsplit(".",1)[0]
            return dict_to_neo_expriment(GRAPH_CRYO, loaded_data, experiment_id)
        elif self.data_type == 'ExperimentUpload':
            if self.data_path.rsplit('.', 1)[-1] == 'json':
                experiment_id = os.path.basename(self.data_path).rsplit(".",1)[0]
                return dict_to_neo_expriment(GRAPH_CRYO, loaded_data, experiment_id)
            else:
                if self.data_path.split('/')[4].lower() == 'predata' or self.data_path.split('/')[5].lower() == 'predata':
                    return dict_to_neo_predata(GRAPH_CRYO, loaded_data)
                if self.data_path.split('/')[5].lower() == 'postdata':
                    return dict_to_neo_postdata(GRAPH_CRYO, loaded_data)
                if self.data_path.split('/')[5].lower() in ['process', 'prozess']:
                    return dict_to_neo_process(GRAPH_CPA, loaded_data)
                if self.data_path.split('/')[5].lower() == 'cpa':
                    child = self.data_path.split('/')[7]
                    return dict_to_neo_cpa(GRAPH_CPA, loaded_data, child)
