import os
from fastapi import FastAPI, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import json
import urllib.parse
from lib_save import connect_to_db
from lib_build import BuildDatabase, BuildDataStore
from data_to_db import feed_into_neo4j
from data_receiver import data_receiver

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
async def fileUpload(file: UploadFile, data_type):
    contents = await file.read()
    return data_receiver(f'data_store/{data_type}/{file.filename}', contents)

@app.post("/feedInNeo/")
async def feedInNeo(data_type):
    return feed_into_neo4j(data_type)


# print(FeedIntoNeo4j('predata', 'data_store\pre_data\EQ20220824A1-Pre1.txt').feed_to_neo4j())
# print(FeedIntoNeo4j('postdata', 'data_store\post_data\EQ20220824-3c-LN2-4-4.txt').feed_to_neo4j())
# print(FeedIntoNeo4j('exp', 'data_store\exp\experiment_1.txt').feed_to_neo4j())

# print(FeedIntoNeo4j('cpa', 'data_store\cpa\CPA1').feed_to_neo4j())
# print(FeedIntoNeo4j('process', 'data_store\process\Prozess1.txt').feed_to_neo4j())