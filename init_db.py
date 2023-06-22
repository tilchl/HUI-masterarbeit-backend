from py2neo import Graph
import json


class Check:
    def __init__(self):
        self.config_account_path = 'development_cpa/config/config_account.json'
        self.graph = self.connect_to_db()
        
    def connect_to_db(self):
        with open(self.config_account_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        graph = Graph(data['profile'], password= data['password'])
        return graph
    
    def delete_all(self):
        self.graph.delete_all()

    def add_limit_cpa(self):
        self.graph.run(f'CREATE CONSTRAINT FOR (n: DSC) REQUIRE n.File_name IS UNIQUE')
        self.graph.run(f'CREATE CONSTRAINT FOR (n: FTIR) REQUIRE n.File_name IS UNIQUE')
        # self.graph.run(f'CREATE CONSTRAINT FOR (n: Cryomicroscopy) REQUIRE n.File_name IS UNIQUE')
        # self.graph.run(f'CREATE CONSTRAINT FOR (n: Osmolality) REQUIRE n.File_name IS UNIQUE')
        # self.graph.run(f'CREATE CONSTRAINT FOR (n: Viscosity) REQUIRE n.File_name IS UNIQUE')
        pass

    def add_limit_cryo(self):
        self.graph.run(f'CREATE CONSTRAINT FOR (n: PreData) REQUIRE n.sample_id IS UNIQUE')
        self.graph.run(f'CREATE CONSTRAINT FOR (n: PostData) REQUIRE n.sample_id IS UNIQUE')
        self.graph.run(f'CREATE CONSTRAINT FOR (n: Experiment) REQUIRE n.experiment_id IS UNIQUE')
    
    def query_all(self):
        node_counts = self.graph.run("MATCH (n) RETURN DISTINCT labels(n) AS label, count(*) AS count").data()
        print("node:")
        for result in node_counts:
            label = result['label'][0]
            count = result['count']
            print(f"{label} Node: {count}")

        relationship_counts = self.graph.run("MATCH ()-[r]->() RETURN DISTINCT type(r) AS type, count(*) AS count").data()
        print("\nrelation:")
        for result in relationship_counts:
            relationship_type = result['type']
            count = result['count']
            print(f"{relationship_type}: {count}")

Check().query_all()