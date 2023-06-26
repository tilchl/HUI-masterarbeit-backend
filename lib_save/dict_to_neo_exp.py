import datetime
from py2neo import Node, Relationship

def dict_to_neo_exp(graph, dict_body):
    try:
        ID = dict_body["Experiment ID"]
        experiment_node = Node('Experiment',**{k.replace(' ', '_'): str(v) if isinstance(v, dict) else v for k, v in dict_body.items()})
        graph.create(experiment_node)

        predata_node = graph.nodes.match('PreData', Sample_ID = dict_body['PreData Sample ID']).first()
        postdata_node = graph.nodes.match('PostData', Sample_ID = dict_body['PostData Sample ID']).first()
        experiment_node = graph.nodes.match('Experiment', Experiment_ID = dict_body['Experiment ID']).first()
        graph.create(Relationship(predata_node, 'pre_data_of_experiment', experiment_node))
        graph.create(Relationship(postdata_node, 'post_data_of_experiment', experiment_node))

        with open('log/log_save.txt', 'a+') as file:
            file.write(f"{datetime.datetime.now()} SUCCESS ON SAVING {ID} \n")
        return 'success'

    except Exception as e:
        with open('log/log_save.txt', 'a+') as file:
            file.write(f"{datetime.datetime.now()} ERROR ON SAVING {ID}: {e} \n")
        if 'already exists' in str(e):
            return 'exists'
        else:
            return 'error'
