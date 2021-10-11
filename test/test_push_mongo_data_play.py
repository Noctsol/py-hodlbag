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

from library import environment as ev

################### CONFIG ###################

env = ev.Environment("./secrets.env")
env.load()

AMOUNT = 10000
BATCHES = 500
TOTAL = int(AMOUNT * BATCHES)
COLLECTION_NAME = "random_data"

################### functions ###################

def rand_sentence():
    ''' Generating random setences to use '''
    nouns = ["We", "I", "The tiger", "Malphie", "He" , "She", "Brother", "Dad", "African Warlord", "Child Solja", "Your Mom"]
    verbs_pre = ["was", "is", "are", "were", "isn't", "wasn't"]
    verbs = ["pooping", "eating", "slapping", "touching", "sleeping", "jumping", "killing", "loving", "squatting"]
    adjectives = ["aggressively", "loudly", "progressively", "happily", "slowly but surely", "frustratingly", "stupidly", "freakishly"]

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
        yield lst[item: item + chunk_n]

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
jsons_lst = []
for i in range(TOTAL):
    json_dict = {
        "quantity": random.randint(1,1000000),
        "price": rand_float(20, 3000000),
        "description": rand_sentence()
    }

    jsons_lst.append(json_dict)

# Splitting list of json documents into chunks
batched_json = list(chunks(jsons_lst, AMOUNT))


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
