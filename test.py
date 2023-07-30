import random
from data_to_db import FeedIntoNeo4j
from main import *

# cleanLog('log_build')
# cleanLog('log_load')
# cleanLog('log_save')
# cleanLog('log_upload')

# deleteDataStore('data_store')
# buildDataStore('data_store')

# cleanDatabase('cpa')
# initDatabase('cpa')
# cleanDatabase('cryo')
# initDatabase('cryo')


# print(FeedIntoNeo4j('predata', 'data_store\pre_data\EQ20220824A1-Pre1.txt').feed_to_neo4j())
# print(FeedIntoNeo4j('postdata', 'data_store\post_data\EQ20220824-3c-LN2-4-4.txt').feed_to_neo4j())
# print(FeedIntoNeo4j('exp', 'data_store\exp\experiment_1.txt').feed_to_neo4j())

# print(FeedIntoNeo4j('cpa', 'data_store\cpa\CPA1').feed_to_neo4j())
# print(FeedIntoNeo4j('process', 'data_store\process\Prozess1.txt').feed_to_neo4j())

import numpy as np
from scipy.stats import f_oneway
from statsmodels.stats.multicomp import pairwise_tukeyhsd

def perform_anova(daten):
    keys = list(daten.keys())
    data =list(daten.values())
  
    result = {}

    # ANOVA
    f_statistic, p_value = f_oneway(*data)

    result["F-statistic"] = f_statistic
    result["p-value"] = p_value

    # Tukey's HSD
    tukey_results = pairwise_tukeyhsd(np.concatenate(data), np.repeat(keys, [len(d) for d in data]), 0.05)

    result["Tukey HSD"] = tukey_results

    return result


daten = {
    'data_A': np.random.normal(np.random.uniform(0, 10), np.random.uniform(1, 3), 10),
'data_B': np.random.normal(np.random.uniform(0, 10), np.random.uniform(1, 3), 10),
'data_C': np.random.normal(np.random.uniform(0, 10), np.random.uniform(1, 3), 10)
}

result = perform_anova(daten)
print(result['Tukey HSD'])


from scipy.stats import ttest_ind


def independent_ttest(data1, data2, alpha=0.05):
    t_statistic, p_value = ttest_ind(data1, data2)
    
    is_significant = p_value < alpha
    
    return t_statistic, p_value, is_significant

print(independent_ttest(daten['data_A'], daten['data_B']))