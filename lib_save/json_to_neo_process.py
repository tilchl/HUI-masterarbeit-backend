from py2neo import Relationship, Node
import datetime


def json_to_neo_process(graph, dict_body):
    try:
        process_node = Node('Process', **{k.replace(' ', '_'): str(v) if isinstance(v, dict) else v for k, v in dict_body.items()})
        graph.create(process_node)

        ID = dict_body["Process ID"]

        with open('log\log_save.txt', 'a+') as file:
            file.write(f"{datetime.datetime.now()} SUCCESS ON SAVING {ID} \n")

    except Exception as e:
        with open('log\log_save.txt', 'a+') as file:
            file.write(f"{datetime.datetime.now()} ERROR ON SAVING{ID}: {e} \n")
