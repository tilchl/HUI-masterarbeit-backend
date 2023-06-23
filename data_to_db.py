from lib_load import load_cpa_data, load_exp_data, load_pre_data, load_post_data, load_process_data, load_config_data
from lib_save import dict_to_neo_process, dict_to_neo_cpa, dict_to_neo_predata, dict_to_neo_postdata, dict_to_neo_exp, connect_to_db


GRAPH_CRYO = connect_to_db('cryo')
GRAPH_CPA = connect_to_db('cpa')


class FeedIntoNeo4j:
    def __init__(self, data_type, data_path):
        self.data_type = data_type
        self.data_path = data_path

    def load_one_experiment(self):
        if self.data_type == 'cpa':
            config_data = load_config_data(self.data_type)
            loaded_data = load_cpa_data(self.data_path, config_data)
        elif self.data_type == 'process':
            config_data = load_config_data(self.data_type)
            loaded_data = load_process_data(self.data_path, config_data)
        elif self.data_type == 'predata':
            config_data = load_config_data(self.data_type)
            loaded_data = load_pre_data(self.data_path, config_data)
        elif self.data_type == 'postdata':
            config_data = load_config_data(self.data_type)
            loaded_data = load_post_data(self.data_path, config_data)
        elif self.data_type == 'exp':
            config_data = load_config_data(self.data_type)
            loaded_data = load_exp_data(self.data_path, config_data)

        return loaded_data

    def feed_to_neo4j(self):
        loaded_data = self.load_one_experiment()
        if self.data_type == 'cpa':
            dict_to_neo_cpa(GRAPH_CPA, loaded_data)
        elif self.data_type == 'process':
            dict_to_neo_process(GRAPH_CPA, loaded_data)
        elif self.data_type == 'predata':
            dict_to_neo_predata(GRAPH_CRYO, loaded_data)
        elif self.data_type == 'postdata':
            dict_to_neo_postdata(GRAPH_CRYO, loaded_data)
        elif self.data_type == 'exp':
            dict_to_neo_exp(GRAPH_CRYO, loaded_data)

FeedIntoNeo4j('cpa', 'data_store\cpa\CPA1').feed_to_neo4j()