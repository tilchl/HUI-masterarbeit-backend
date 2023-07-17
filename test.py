from data_to_db import FeedIntoNeo4j
from main import *

cleanLog('log_build')
cleanLog('log_load')
cleanLog('log_save')
cleanLog('log_upload')

# deleteDataStore('data_store')
# buildDataStore('data_store')

# cleanDatabase('cpa')
# cleanDatabase('cryo')
# initDatabase('cpa')
# initDatabase('cryo')


# print(FeedIntoNeo4j('predata', 'data_store\pre_data\EQ20220824A1-Pre1.txt').feed_to_neo4j())
# print(FeedIntoNeo4j('postdata', 'data_store\post_data\EQ20220824-3c-LN2-4-4.txt').feed_to_neo4j())
# print(FeedIntoNeo4j('exp', 'data_store\exp\experiment_1.txt').feed_to_neo4j())

# print(FeedIntoNeo4j('cpa', 'data_store\cpa\CPA1').feed_to_neo4j())
# print(FeedIntoNeo4j('process', 'data_store\process\Prozess1.txt').feed_to_neo4j())
