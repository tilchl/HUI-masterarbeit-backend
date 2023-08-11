from typing import Any, Dict
import pandas
from scipy.stats import ttest_ind
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from scipy.stats import f_oneway
import ast
import os
import numpy as np
from scipy import stats
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
    result = GRAPH_CRYO.run(query).data()[0]
    result['child'] = sorted(result['child'], key=lambda child: child['versuch']['Versuch_ID'])
    
    return result


@app.get("/queryOneCPA/{ID}")
def queryOneCPA(ID):
    query = f"""MATCH (cpa:CPA {{CPA_ID: '{ID}'}})\
              OPTIONAL MATCH (cpa:CPA {{CPA_ID: '{ID}'}})-[*..1]->(c)\
              WITH cpa, c,\
                CASE labels(c)[0]\
                    WHEN 'DSC' THEN c.DSC_ID\
                    WHEN 'FTIR' THEN c.FTIR_ID\
                    WHEN 'Cryomicroscopy' THEN c.Cryomicroscopy_ID\
                    WHEN 'Osmolality' THEN c.Osmolality_ID\
                    WHEN 'Viscosity' THEN c.Viscosity_ID\
                END AS attribute_value\
              RETURN cpa, COLLECT({{class: labels(c)[0], unique_id:attribute_value, properties: properties(c)}}) AS child"""
    result = GRAPH_CPA.run(query).data()[0]
    for child in result['child']:
        del child['properties']['Curve']
    
    return result


@app.post("/getMeanAndVariance/")
def getMeanAndVariance(req: Dict[Any, Any] = None):
    data = req['data']
    # data = urllib.parse.unquote(data)
    # data = ast.literal_eval(data)
    data = [float(item) for item in data]
    mean = np.mean(data)
    variance = np.var(data, ddof=1)
    standard_deviation = np.std(data, ddof=1)
    standard_error = standard_deviation / np.sqrt(len(data))
    confidence_level = 0.95
    n = len(data)
    confidence_interval = stats.t.interval(
        confidence_level, df=n-1, loc=mean, scale=standard_error)

    if n == 1:
        variance = standard_deviation = standard_error = 0.0000
        confidence_interval = (0.00, 0.00)
    return {
        "mean": f"{mean:.4f}",
        "variance": f"{variance:.4f}",
        "SD": f"{standard_deviation:.4f}",
        "SE": f"{standard_error:.4f}",
        f"CI {confidence_level * 100:.0f}%": f"[{confidence_interval[0]:.2f}, {confidence_interval[1]:.2f}]"
    }


@app.post("/buildColumn/")
def buildColumn(data: Dict[Any, Any] = None):
    predata, postdata, key = data['predata'], data['postdata'], data['key']
    # predata = urllib.parse.unquote(predata)
    # predata = ast.literal_eval(predata)
    # postdata = urllib.parse.unquote(postdata)
    # postdata = ast.literal_eval(postdata)

    query_pre = f"MATCH (n:PreData)\
              WHERE n.Sample_ID IN {str(predata)}\
              RETURN COLLECT(n.`{key}`) AS data"

    query_post = f"MATCH (n:PostData)\
              WHERE n.Sample_ID IN {str(postdata)}\
              RETURN COLLECT(n.`{key}`) AS data"

    result_pre = GRAPH_CRYO.run(query_pre).data()[0]['data']
    result_post = GRAPH_CRYO.run(query_post).data()[0]['data']

    return {
        "pre_data": getMeanAndVariance({'data': result_pre}),
        "post_data": getMeanAndVariance({'data': result_post}),
        "post/pre": getMeanAndVariance({'data': [f"{(float(item)*100)/float(np.mean([float(item) for item in result_pre])):.4f}" for item in result_post]})
    }


@app.post("/buildAnovaTable/")
def buildAnovaTable(data: Dict[Any, Any] = None):
    postdata, predata, key = data['postdata'],data['predata'], data['key']
    # postdata = urllib.parse.unquote(postdata)
    # postdata = ast.literal_eval(postdata)\\
    ppdata = {}
    for _key in list(postdata.keys()):
        su = []
        for i,p in enumerate(postdata[_key]):
            query_post = f"MATCH (n:PostData)\
                WHERE n.Sample_ID IN {str(p)}\
                RETURN COLLECT(n.`{key}`) AS data"
            query_pre = f"MATCH (n:PreData)\
                WHERE n.Sample_ID IN {str(predata[_key][i])}\
                RETURN COLLECT(n.`{key}`) AS data"
            postdata[_key][i] = GRAPH_CRYO.run(query_post).data()[0]['data']
            mean = np.mean([float(item) for item in GRAPH_CRYO.run(query_pre).data()[0]['data']])
            su.append([str((float(item)*100)/mean) for item in postdata[_key][i]])
        ppdata[_key] = su
    for _key in list(postdata.keys()):
        postdata[_key] = [item for sublist in postdata[_key] for item in sublist]
        ppdata[_key] = [item for sublist in ppdata[_key] for item in sublist]

    return {
        "post":anovaTest(str(postdata)),
        "post/pre":anovaTest(str(ppdata))
        }


@app.get("/anovaTest/{daten}")
def anovaTest(daten):
    daten = urllib.parse.unquote(daten)
    daten = ast.literal_eval(daten)
    # data_dict = ast.literal_eval(data_str)
    # print(data_dict)
    keys = list(daten.keys())
    data = list(daten.values())

    result = {}

    # ANOVA
    f_statistic, p_value = f_oneway(*data)

    result["F-statistic"] = round(f_statistic, 4)
    result["p-value"] = round(p_value, 4)
    # Tukey's HSD
    tukey_results = pairwise_tukeyhsd([float(n) for n in np.concatenate(data)], np.repeat(keys, [len(d) for d in data]), 0.05)
    df = pandas.DataFrame(
        data=tukey_results._results_table.data[1:], columns=tukey_results._results_table.data[0])
    result["Tukey HSD 0.05"] = list(df.to_dict(orient='index').values())
    result['Tukey Group'] = generate_tukey_subscripts(df)
    return result


def generate_tukey_subscripts(tukey_result_df):

    all_groups = list(set(tukey_result_df["group1"]).union(
        set(tukey_result_df["group2"])))
    gmeans = {}
    gmeans[all_groups[0]] = 0

    related_comparisons = tukey_result_df[(
        tukey_result_df["group1"] == all_groups[0])]
    related_comparisons_2 = tukey_result_df[(
        tukey_result_df["group2"] == all_groups[0])]

    for _, comparison in related_comparisons.iterrows():
        gmeans[comparison["group2"]] = 0 + comparison['meandiff']
    for _, comparison in related_comparisons_2.iterrows():
        gmeans[comparison["group1"]] = 0 - comparison['meandiff']

    sorted_groups = sorted(all_groups, key=lambda group: -gmeans[group])

    result_group = {}
    for group in sorted_groups:
        result_group[group] = ''
    letters = [chr(i) for i in range(ord('a'), ord('z')+1)]
    index = 0

    for i in range(len(sorted_groups)):
        result_group[sorted_groups[i]] += letters[index]
        for j in range(len(sorted_groups)):
            if i != j:
                # p_value = tukey_result_df[(tukey_result_df["group1"] == sorted_groups[i]) & (tukey_result_df["group2"] == sorted_groups[j]) |(tukey_result_df["group2"] == sorted_groups[i]) & (tukey_result_df["group1"] == sorted_groups[j])]['p-adj'].iloc[0]
                p_value = tukey_result_df.loc[
                    ((tukey_result_df["group1"]==sorted_groups[i]) & (tukey_result_df["group2"]==sorted_groups[j])) | ((tukey_result_df["group2"]==sorted_groups[i]) & (tukey_result_df["group1"]==sorted_groups[j])),
                    "p-adj"
                ].iloc[0]
                if p_value <= 0.05:
                    if p_value <= 0.01:
                        result_group[sorted_groups[j]] += letters[index].upper()
                    else:
                        result_group[sorted_groups[j]] += letters[index]
        if any(value == '' for value in result_group.values()):
            index += 1
        else:
            break

    return result_group

@app.get("/tTest/")
def tTest(data1, data2, alpha=0.05):
    t_statistic, p_value = ttest_ind(data1, data2)

    is_significant = p_value < alpha

    return {
        "t_statistic": t_statistic,
        "p_value": p_value,
        "is_significant": is_significant
    }
