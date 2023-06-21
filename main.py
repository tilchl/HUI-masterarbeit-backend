from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
from py2neo import Graph
import urllib.parse

app = FastAPI()

@app.get("/")
def read_root():
    return 'successfully connect to backend'


# Allow cross domain requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def connect_to_db(account_path):
    with open(account_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        graph_cryo = Graph(data['profile_cryo'], password= data['password_cryo'])
        graph_cpa = Graph(data['profile_cpa'], password= data['password_cpa'])
    return graph_cryo, graph_cpa

graph_cryo, graph_cpa = connect_to_db('account.json')


@app.get("/freeQueryCryo/{query}")
def freeQueryCryo(query):
    query = urllib.parse.unquote(query)
    res = graph_cryo.run(query).data()
    return res

@app.get("/freeQueryCpa/{query}")
def freeQueryCpa(query):
    query = urllib.parse.unquote(query)
    res = graph_cpa.run(query).data()
    return res