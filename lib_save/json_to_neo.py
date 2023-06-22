from py2neo import Graph, Relationship, Node

def json_to_neo(graph, json_body, exp_index):
    try:
        experiment_node = Node('Experiment',
                            experiment_id=exp_index,
                            CPA=json_body['CPA'],
                            Process=str(json_body['Process']))
        pre_data_node = Node('PreData', **{k: str(v) if isinstance(v, dict) else v for k, v in json_body['PreData'].items()}, sample_id=json_body['PreData']['Log']['Sample ID'])
        post_data_node = Node('PostData', **{k: str(v) if isinstance(v, dict) else v for k, v in json_body['PostData'].items()}, sample_id=json_body['PostData']['Log']['Sample ID'])

        relation_pre_exp = Relationship(pre_data_node, "Pre_Data_Of_Experiment", experiment_node)
        relation_exp_post = Relationship(experiment_node, "Post_Data_Of_Experiment", post_data_node)

        graph.create(relation_pre_exp)
        graph.create(relation_exp_post)
    except Exception as e:
        print(e) # should writed in log.txt
