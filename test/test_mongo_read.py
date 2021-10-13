"""
Owner: Kevin B
Contributors: N/A
Date Created: 20211011

Summary:
    Quick script used in tandem with the write version of this script to test how fast data pulls can be.
    Indexes were genewrated using mondodb compass
"""
from pymongo import MongoClient
import sys
import random
import time
sys.path.append('.')

from datetime import datetime, timezone

from library import environment as ev, helper

################### CONFIG ###################

env = ev.Environment("./secrets.env")
env.load()
hlp = helper.Helper()

AMOUNT = 100000
BATCHES = 50
TOTAL = int(AMOUNT * BATCHES)
COLLECTION_NAME = "random_data_three"

################### functions ###################

def rand_sentence():
    ''' Generating random setences to use '''
    nouns = ["We", "I", "The tiger", "Malphie", "He" , "She", "Brother", "Dad", "African Warlord", "Child Solja", "Your Mom", "Muh dog"]
    verbs_pre = ["was", "is", "are", "were", "isn't", "wasn't", "can't think of", "wants to be", "doesn't want to be"]
    verbs = ["pooping", "eating", "slapping", "touching", "sleeping", "jumping", "killing", "loving", "squatting"]
    adjectives = ["aggressively", "loudly", "progressively", "happily", "slowly but surely", "frustratingly", "stupidly", "freakishly", "peacefully"]

    noun = random.choice(nouns)
    prevb = random.choice(verbs_pre)
    verb = random.choice(verbs)
    adj = random.choice(adjectives)

    return f"{noun} {prevb} {verb} {adj}."

def rand_float(num1, num2, rounding=2):
    ''' Generates random float '''
    return round(random.uniform(num1,num2), rounding)

def chunks(a_list, chunk_n):
    """Yield successive n-sized chunks from lst. Stackoverflow"""
    for item in range(0, len(a_list), chunk_n):
        yield a_list[item: item + chunk_n]

def to_datetime(dt_string, date_format="%Y-%m-%d"):
    """ easy way to generate datetime using string"""
    return datetime.strptime(dt_string, date_format)

# Wonky function to execute queries
def find_gte(coll, key_a, gte_value, limit=100):
    """ Quick function to execute specific types of queries """
    result = coll.find({key_a: {'$gte': gte_value}}).limit(limit).explain()['executionStats']
    return result

# Wonky function to execute queries
def find_lte(coll, key_a, lte_value):
    """ Quick function to execute specific types of queries """
    return [doc for doc in coll.find({key_a: {'$lte': lte_value}})]

# Wonky function to execute queries
def find_gtelte(coll, key_a, gte_value, lte_value ):
    """ Quick function to execute specific types of queries """
    return coll.find({key_a: {'$gte': gte_value, '$lte': lte_value}})

# Quic function to time events
def timeit(sometimer=None):
    if sometimer is None:
        return time.time()
    else:
        return time.time() - sometimer
################### bODY ###################

# Start up client
client = MongoClient(env.get("MONGO_CONN_PLAY"))

# Point to databse - multiple ways.....property access or dictionary access
dbch = client["wewt"]     # Could also do client.cryptohodl

# Create Collection if it doesnt exist
lst = dbch.list_collection_names()
if COLLECTION_NAME not in lst:
    rando = dbch.create_collection(COLLECTION_NAME)
else:
    rando = dbch[COLLECTION_NAME]



# Testing datetimes
dt_gte_criteria = [
    [to_datetime("2021-01-01"),10],
    [to_datetime("2015-01-01"),100],
    [to_datetime("2010-01-01"),1000],
    [to_datetime("2005-01-01"),10000],
    [to_datetime("2005-01-01"),100000]
     ]

for i in dt_gte_criteria:
    a = timeit()
    # count = len(find_gte(rando, "random_datetime", i))
    explainjson = find_gte(rando, "random_datetime", i[0], limit=i[1])
    b = timeit(a)
    db_time = explainjson['executionTimeMillis']
    ping_time = round(b - (float(explainjson['executionTimeMillis'])/1000),5)
    print(f"gte datetime: TOTAL ROUNDTRIP: {round(b,5)} - PING: {ping_time} - DB TIME: {db_time} - Amountof Results: {explainjson['nReturned']}")

# dt_lte_criteria = [
#     to_datetime("1901-01-01"),
#     to_datetime("1905-01-01"),
#     to_datetime("1910-01-01"),
#     to_datetime("1910-01-01"),
#     ]

# for i in dt_lte_criteria:
#     a = timeit()
#     find_lte(rando, "random_datetime", i)
#     b = timeit(a)
#     print(f"lte datetime: {b}")


# Testing int searches


# Testing float searches


# Wild card test searches


# Muti condition searches


# Tracking time
start_batch = time.time()



# Print out info at the end
end_time = time.time() - start_batch
print(f"Time for completion:{round(end_time,2)}")
