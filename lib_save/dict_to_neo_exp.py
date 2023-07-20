import datetime
from py2neo import Node, Relationship
import os

def dict_to_neo_probe(graph, dict_body, versuch):
    try:
        ID = dict_body["Sample ID"]
        probe_node = Node('Probe',**{k.replace(' ', '_'): str(v) if isinstance(v, dict) else v for k, v in dict_body.items()})
        graph.create(probe_node)

        versuch_node = graph.nodes.match('Versuch', Versuch_ID = versuch).first()
        predata_node = graph.nodes.match('PreData', Sample_ID = dict_body['PreData ID']).first()
        postdata_node = graph.nodes.match('PostData', Sample_ID = dict_body['PostData ID']).first()
        probe_node = graph.nodes.match('Probe', Sample_ID = dict_body['Sample ID']).first()
        graph.create(Relationship(probe_node, 'probe_of_versuch', versuch_node))
        graph.create(Relationship(predata_node, 'pre_data_of_probe', probe_node))
        graph.create(Relationship(postdata_node, 'post_data_of_probe', probe_node))

        with open('log/log_save.txt', 'a+') as file:
            file.write(f"{datetime.datetime.now()} SUCCESS ON SAVING PROBE {ID} \n")
        return 'success'

    except Exception as e:
        with open('log/log_save.txt', 'a+') as file:
            file.write(f"{datetime.datetime.now()} ERROR ON SAVING PROBE {ID}: {e} \n")
        if 'already exists' in str(e):
            return 'exists'
        else:
            return 'error'

def dict_to_neo_expriment(graph, dict_body, experiment_id):
    try:
        with open(f'log/log_exps/log_{experiment_id}.txt', 'w') as file:
                file.write(
                    "Versuch ID,Sample ID,CPA ID,Process ID,PreData ID,PostData ID,result\n")

        infos = []
        for versuch in dict_body:
            experiment_node = Node('Experiment',Experiment_ID = experiment_id)
            versuch_node = Node('Versuch',Versuch_ID = dict_body[versuch]['Versuche ID'])
            graph.create(experiment_node)
            graph.create(versuch_node)
            
            experiment_node = graph.nodes.match('Experiment', Experiment_ID = experiment_id).first()
            versuch_node = graph.nodes.match('Versuch', Versuch_ID = dict_body[versuch]['Versuche ID']).first()
            graph.create(Relationship(versuch_node, 'versuch_of_experiment', experiment_node))


            for probe in dict_body[versuch]:
                if probe == 'Versuche ID':
                    continue
                else:
                    with open('log/log_load.txt', 'a+') as file:
                        file.write(
                            f"{datetime.datetime.now()} SUCCESS ON LOADING PROBE DATA: {dict_body[versuch][probe]['Sample ID']} \n")
                    
                    feed_to_neo_result = dict_to_neo_probe(graph, dict_body[versuch][probe], dict_body[versuch]['Versuche ID'])
                    with open(f'log/log_exps/log_{experiment_id}.txt', 'a+') as file:
                        file.write(
                            f"{versuch},{dict_body[versuch][probe]['Sample ID']},{dict_body[versuch][probe]['CPA ID']},{dict_body[versuch][probe]['Process ID']},{dict_body[versuch][probe]['PreData ID']},{dict_body[versuch][probe]['PostData ID']},{feed_to_neo_result} \n")

                    infos.append(feed_to_neo_result)
        
        if all(element == 'success' for element in infos):
            return 'success'
        else:
            return 'see-error-detail'

    except Exception as e:
       with open('log/log_load.txt', 'a+') as file:
           file.write(
               f"{datetime.datetime.now()} ERROR ON LOADING EXP DATA: {experiment_id}: {e} \n")
    
       return 'error'