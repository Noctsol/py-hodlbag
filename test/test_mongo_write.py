"""
Owner: Kevin B
Contributors: N/A
Date Created: 20211011

Summary:
    Quick script to generate a collection and push to a MONGO db. Wanted to test write speeds to a crappy mongo db cluster.
    It was insanely inpressive. It got drammatically slow with each added index, but write operations were still solid.
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

AMOUNT = 10000
BATCHES = 100
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

def rand_datetime():
    year = random.randint(1900, 2021)
    month = random.randint(1, 12)
    day = random.randint(1, 28)   # Almost wanted to write something to deal with this but ignored it
    hour = random.randint(1, 23)
    minute = random.randint(1, 59)
    second = random.randint(1, 59)

    return datetime(year, month, day, hour, minute, second, 505, tzinfo=timezone.utc)
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

# Generating json documents to upload
print("Generating Randomized Data")
jsons_lst = []
for i in range(TOTAL):
    json_dict = {
        "guid": hlp.make_uuid(),
        "inserted_datetime": datetime.utcnow(),
        "quantity": random.randint(1,1000000),
        "price": rand_float(20, 3000000),
        "description": rand_sentence(),
        "random_datetime": rand_datetime()
    }

    jsons_lst.append(json_dict)

# Splitting list of json documents into chunks
batched_json = chunks(jsons_lst, AMOUNT)

print("Inserting Data")

# Tracking time
start_batch = time.time()

# Uploading each chunk
for i in batched_json:
    start_i = time.time()
    # Use insert many instead of insert_one!
    rando.insert_many(i)
    end_i = time.time() - start_i
    print(f"Time for cycle:{round(end_i,2)}")

# Print out info at the end
end_time = time.time() - start_batch
print(f"Time for completion:{round(end_time,2)}")
print(f"Average time per transact:{round(end_time/len(jsons_lst), 6)}")
