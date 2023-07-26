import os
from fastapi import FastAPI, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import json
import urllib.parse
from lib_save import connect_to_db
from lib_build import BuildDatabase, BuildDataStore
from data_to_db import FeedIntoNeo4j
from data_receiver import data_receiver, dict_to_txt

app = FastAPI()

# Allow cross domain requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return 'success'


GRAPH_CRYO = connect_to_db('cryo')
GRAPH_CPA = connect_to_db('cpa')


@app.get("/freeQueryCryo/{query}")
def freeQueryCryo(query):
    query = urllib.parse.unquote(query)
    return GRAPH_CRYO.run(query).data()


@app.get("/freeQueryCpa/{query}")
def freeQueryCpa(query):
    query = urllib.parse.unquote(query)
    return GRAPH_CPA.run(query).data()


@app.get("/cleanDatabase/{db_id}")
def cleanDatabase(db_id):
    if db_id == 'cryo':
        BuildDatabase(GRAPH_CRYO, 'cryo').delete_all()
    elif db_id == 'cpa':
        BuildDatabase(GRAPH_CPA, 'cpa').delete_all()
    return f'SUCCESS: DATABASE {db_id} CLEANED'


@app.get("/initDatabase/{db_id}")
def initDatabase(db_id):
    if db_id == 'cryo':
        cleanDatabase('cryo')
        BuildDatabase(GRAPH_CRYO, 'cryo').add_constraint()
    elif db_id == 'cpa':
        cleanDatabase('cpa')
        BuildDatabase(GRAPH_CPA, 'cpa').add_constraint()
    return f'SUCCESS: DATABASE {db_id} INIT'


@app.get("/connectDatabase/{db_id}")
def connectDatabase(db_id):
    if db_id == 'cryo':
        return BuildDatabase(GRAPH_CRYO, 'cryo').query_all()
    elif db_id == 'cpa':
        return BuildDatabase(GRAPH_CPA, 'cpa').query_all()


@app.get("/findIsolatedNodes/{db_id}")
def findIsolatedNodes(db_id):
    if db_id == 'cryo':
        return BuildDatabase(GRAPH_CRYO, 'cryo').find_isolated_nodes()
    elif db_id == 'cpa':
        return BuildDatabase(GRAPH_CPA, 'cpa').find_isolated_nodes()


@app.get("/buildDataStore/{store_name}")
def buildDataStore(store_name):
    return BuildDataStore(store_name).create_data_store_folder()


@app.get("/deleteDataStore/{store_name}")
def deleteDataStore(store_name):
    return BuildDataStore(store_name).delete_folder()


@app.get("/deleteOneType/")
def deleteOneType(store_name, data_type):
    return BuildDataStore(store_name).delete_one_type(data_type)


@app.get("/buildOneType/")
def buildOneType(store_name, data_type):
    return BuildDataStore(store_name).create_one_type(data_type)


@app.get("/cleanLog/{log_id}")
def cleanLog(log_id):
    try:
        file_path = f'log/{log_id}.txt'
        with open(file_path, 'w') as file:
            file.truncate(0)
        return (f"Cleared file: {file_path}")
    except Exception as e:
        return 'error'


@app.get("/seeLog/{log_id}")
def seeLog(log_id):
    pass


@app.post("/fileUpload/")
async def fileUpload(files: list[UploadFile], data_type, data_store):
    res = []
    if data_type == 'CPA':
        for file in files:
            file_name = "/".join(file.filename.split("/")[-3:])
            upload_result = data_receiver(f'{data_store}/{data_type}/{file_name}', await file.read(), data_type)
            res.append({'file_name': file_name, 'result': upload_result,
                       'neo4j': 'waiting' if upload_result == 'success' else 'undo'})
        return str(res)
    else:
        for file in files:
            upload_result = data_receiver(f'{data_store}/{data_type}/{file.filename}', await file.read(), data_type)
            res.append({'file_name': file.filename, 'result': upload_result,
                       'neo4j': 'waiting' if upload_result == 'success' else 'undo'})
        return str(res)


@app.post("/fileCreate/")
async def fileCreate(files: list[UploadFile], data_type, data_store):
    res = []
    if data_type == 'CPA':
        for file in files:
            file_name = "/".join(file.filename.split("/")[-3:])
            upload_result = data_receiver(f'{data_store}/{data_type}/{file_name}', dict_to_txt(await file.read(), data_type, file_name), data_type)
            res.append({'file_name': file_name, 'result': upload_result,
                       'neo4j': 'waiting' if upload_result == 'success' else 'undo'})
        return str(res)
    else:
        for file in files:
            upload_result = data_receiver(f'{data_store}/{data_type}/{file.filename}', dict_to_txt(await file.read(), data_type, file.filename), data_type)
            res.append({'file_name': file.filename, 'result': upload_result,
                       'neo4j': 'waiting' if upload_result == 'success' else 'undo'})
        return str(res)


@app.get("/feedInNeo/")
def feedInNeo(data_type, file_name, data_store):
    try:
        if data_type == 'CPA':
            return FeedIntoNeo4j(data_type, f'{data_store}/{data_type}/{file_name}').feed_to_neo4j()
        elif data_type == 'Experiment':
            return FeedIntoNeo4j(data_type, f'{data_store}/{data_type}/{file_name}').feed_to_neo4j()
        else:
            return FeedIntoNeo4j(data_type, f'{data_store}/{data_type}/{file_name}').feed_to_neo4j()

    except Exception as e:
        return 'error'


UNIQUE_ID = {
    'PreData': 'Sample_ID',
    'PostData': 'Sample_ID',
    'Experiment': 'Experiment_ID',
    'Process': 'Process_ID',
    'CPA': 'CPA_ID',
    'DSC': 'DSC_ID',
    'FTIR': 'FTIR_ID',
    'Cryomicroscopy': 'Cryomicroscopy_ID',
    'Osmolality': 'Osmolality_ID',
    'Viscosity': 'Viscosity_ID',
}


@app.get("/queryOneType/")
def queryOneType(data_type):
    query = f"MATCH (p:{data_type}) RETURN COLLECT(p.{UNIQUE_ID[data_type]}) AS idList"
    if data_type in ['PreData', 'PostData', 'Experiment']:
        result = GRAPH_CRYO.run(query).data()
    else:
        result = GRAPH_CPA.run(query).data()

    return str(sorted(result[0]['idList'])).replace("'", '"')


@app.get("/queryOneNode/")
def queryOneNode(data_type, ID):
    query = f'MATCH (p:{data_type}) WHERE p.{UNIQUE_ID[data_type]} = "{ID}" RETURN p'
    if data_type in ['PreData', 'PostData', 'Experiment']:
        result = GRAPH_CRYO.run(query).data()
    else:
        result = GRAPH_CPA.run(query).data()
    return result[0]['p']


@app.get("/duplicateCheck/")
def duplicateCheck(data_type, ID):
    query = f'MATCH (p:{data_type}) WHERE p.{UNIQUE_ID[data_type]} = "{ID}" RETURN COUNT(p) > 0'
    if data_type in ['PreData', 'PostData', 'Experiment']:
        result = GRAPH_CRYO.run(query).data()
    else:
        result = GRAPH_CPA.run(query).data()
    return result[0]["COUNT(p) > 0"]


@app.get("/queryOneExperiment/{ID}")
def queryOneExperiment(ID):
    query = f'MATCH(experiment: Experiment)\
              WHERE experiment.Experiment_ID = "{ID}"\
              OPTIONAL MATCH (experiment: Experiment)<-[:versuch_of_experiment]-(second: Versuch)\
              OPTIONAL MATCH (second)<-[:probe_of_versuch*..1]-(third:Probe)\
              WITH experiment, second, COLLECT(DISTINCT third) as thirdNodes\
              RETURN experiment, COLLECT({{versuch: second, probes: thirdNodes}}) as child'
    result = GRAPH_CRYO.run(query).data()
    return result[0]

@app.get("/queryOneCPA/{ID}")
def queryOneCPA(ID):
    query = f"MATCH (cpa:CPA {{CPA_ID: '{ID}'}})\
              OPTIONAL MATCH (cpa:CPA {{CPA_ID: '{ID}'}})-[*..1]->(c)\
              WITH cpa, c,\
                CASE labels(c)[0]\
                    WHEN 'DSC' THEN c.DSC_ID\
                    WHEN 'FTIR' THEN c.FTIR_ID\
                    WHEN 'Cryomicroscopy' THEN c.Cryomicroscopy_ID\
                    WHEN 'Osmolality' THEN c.Osmolality_ID\
                    WHEN 'Viscosity' THEN c.Viscosity_ID\
                END AS attribute_value\
              RETURN cpa, COLLECT({{class: labels(c)[0], unique_id:attribute_value}}) AS child"
    
    
    result = GRAPH_CPA.run(query).data()
    return result[0]
