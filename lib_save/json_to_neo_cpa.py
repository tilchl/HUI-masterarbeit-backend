from py2neo import Graph, Relationship, Node

def json_to_neo(graph, json_body):
    try:
        cpa_node = Node('CPA', cpa_id=json_body['CPA ID'])
        dsc_node = Node('DSC', **{k: str(v) if isinstance(v, dict) else v for k, v in json_body['DSC'].items()})
        ftir_node = Node('FTIR', **{k: str(v) if isinstance(v, dict) else v for k, v in json_body['FTIR'].items()})
        # cryomicro_node = Node('Cryomicroscopy', **{k: str(v) if isinstance(v, dict) else v for k, v in json_body['Cryomicroscopy'].items()})
        # osmo_node = Node('Osmolality', **{k: str(v) if isinstance(v, dict) else v for k, v in json_body['Osmolality'].items()})
        # visc_node = Node('Viscosity', **{k: str(v) if isinstance(v, dict) else v for k, v in json_body['Viscosity'].items()})
        cryomicro_node = Node('Cryomicroscopy')
        osmo_node = Node('Osmolality')
        visc_node = Node('Viscosity')

        graph.create(Relationship(cpa_node, "dsc_info", dsc_node))
        graph.create(Relationship(cpa_node, "ftir_info", ftir_node))
        graph.create(Relationship(cpa_node, "cryomicro_info", cryomicro_node))
        graph.create(Relationship(cpa_node, "osmo_info", osmo_node))
        graph.create(Relationship(cpa_node, "visc_info", visc_node))

    except Exception as e:
        print(e) # should writed in log.txt
