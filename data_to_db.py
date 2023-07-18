import datetime
import os
import pandas as pd
from lib_load import load_cpa_data, load_pre_data, load_post_data, load_process_data, load_config_data
from lib_save import dict_to_neo_process, dict_to_neo_cpa, dict_to_neo_predata, dict_to_neo_postdata, dict_to_neo_exp, connect_to_db


GRAPH_CRYO = connect_to_db('cryo')
GRAPH_CPA = connect_to_db('cpa')


class FeedIntoNeo4j:
    def __init__(self, data_type, data_path):
        self.data_type = data_type
        self.data_path = data_path

    def load_one(self):
        if self.data_type == 'cpa':
            config_data = load_config_data(self.data_type)
            loaded_data = load_cpa_data(self.data_path, config_data)
        elif self.data_type == 'process':
            config_data = load_config_data(self.data_type)
            loaded_data = load_process_data(self.data_path, config_data)
        elif self.data_type == 'pre_data':
            config_data = load_config_data(self.data_type)
            loaded_data = load_pre_data(self.data_path, config_data)
        elif self.data_type == 'post_data':
            config_data = load_config_data(self.data_type)
            loaded_data = load_post_data(self.data_path, config_data)

        return loaded_data

    def feed_to_neo4j(self):
        loaded_data = self.load_one()
        if self.data_type == 'cpa':
            return dict_to_neo_cpa(GRAPH_CPA, loaded_data)
        elif self.data_type == 'process':
            return dict_to_neo_process(GRAPH_CPA, loaded_data)
        elif self.data_type == 'pre_data':
            return dict_to_neo_predata(GRAPH_CRYO, loaded_data)
        elif self.data_type == 'post_data':
            return dict_to_neo_postdata(GRAPH_CRYO, loaded_data)


    def load_and_feed_experiment(self):
        try:
            df = pd.read_csv(self.data_path, sep=',', header=0)
            with open(f'log/log_{os.path.basename(self.data_path).split(".")[0]}.txt', 'w') as file:
                    file.write(
                        "Experiment ID,CPA ID,Process ID,PreData Sample ID,PostData Sample ID,result\n")

            infos = []
            for index, row in df.iterrows():
                config_data = load_config_data(self.data_type)
                config_data["Experiment ID"] = row['Experiment']
                config_data["CPA ID"] = row['CPA']
                config_data["Process ID"] = row['Process']
                config_data["PreData Sample ID"] = row['PreData Sample']
                config_data["PostData Sample ID"] = row['PostData Sample']

                with open('log/log_load.txt', 'a+') as file:
                    file.write(
                        f"{datetime.datetime.now()} SUCCESS ON LOADING EXP DATA: {row['Experiment']} \n")
                    
                feed_to_neo_result = dict_to_neo_exp(GRAPH_CRYO, config_data)
                with open(f'log/log_{os.path.basename(self.data_path).split(".")[0]}.txt', 'a+') as file:
                    file.write(
                        f"{row['Experiment']},{row['CPA']},{row['Process']},{row['PreData Sample']},{row['PostData Sample']},{feed_to_neo_result} \n")

                infos.append(feed_to_neo_result)
            
            if all(element == 'success' for element in infos):
                return 'success'
            else:

                return 'see-error-detail'

        except Exception as e:
            with open('log/log_load.txt', 'a+') as file:
                file.write(
                    f"{datetime.datetime.now()} ERROR ON LOADING EXP DATA: {os.path.basename(self.data_path)}: {e} \n")

            return 'error'
