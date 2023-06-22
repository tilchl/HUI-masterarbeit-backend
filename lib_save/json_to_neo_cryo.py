import datetime
from py2neo import Relationship, Node

def json_to_neo_cryo(graph, dict_body):
    try:
        experiment_node = Node('Experiment',**{k.replace(' ', '_'): str(v) if isinstance(v, dict) else v for k, v in dict_body['Experiment'].items()})
        pre_data_node = Node('PreData', **{k.replace(' ', '_'): str(v) if isinstance(v, dict) else v for k, v in dict_body['PreData'].items()})
        post_data_node = Node('PostData', **{k.replace(' ', '_'): str(v) if isinstance(v, dict) else v for k, v in dict_body['PostData'].items()})

        relation_pre_exp = Relationship(pre_data_node, "Pre_Data_Of_Experiment", experiment_node)
        relation_exp_post = Relationship(experiment_node, "Post_Data_Of_Experiment", post_data_node)

        graph.create(relation_pre_exp)
        graph.create(relation_exp_post)

        ID = dict_body['Experiment']["Experiment ID"]

        with open('log\log_save.txt', 'a+') as file:
            file.write(f"{datetime.datetime.now()} SUCCESS ON SAVING {ID} \n")

    except Exception as e:
        with open('log\log_save.txt', 'a+') as file:
            file.write(f"{datetime.datetime.now()} ERROR ON SAVING{ID}: {e} \n")
