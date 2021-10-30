"""
Owner: Noctsol
Contributors: N/A
Date Created: 20211011

Summary:
    Quuick script to generate a collection and push to a db
"""
from pymongo import MongoClient
import sys
sys.path.append('.')

from library import environment as ev

def properties(some_obj):
    ''' '''
    dct = some_obj.__dict__
    for i in dct:
        print(f"{i} == {dct[i]}")
    print("\n"*3)

env = ev.Environment("./secrets.env")
env.load()

# Start up client
client = MongoClient(env.get("MONGO_CONN_STR"))

# Point to databse - multiple ways.....property access or dictionary access
dba = client.admin                # Property access to point to admin could also do db_admin=client["admin"]
dbch = client["cryptohodl"]     # Could also do client.cryptohodl

# Access collections
test_collection = dbch["Tests"]
test_collection = dbch.Tests


# Creating and dropping collection
collection_name = "zzzTest"

# Creating collection - doesn't work if it exists already - call lsit colelctions to see if it exists
# A collection object is returned that you can use
zzzTestsCollection = dbch.create_collection(collection_name)


# Dropping collection - returns None - will error out if it doesn't exist
dropstatus = dbch[collection_name].drop()



# Execute commands that don't have python code written for them I think
# You canb execute anything ehre I think https://docs.mongodb.com/manual/reference/command/
# Ah....Shell methods like show users are something else different compared to Database commands
serverStatusResult=dba.command("serverStatus")
users=dba.command("usersInfo")  # equivalent of show users i think?
print("\n",users,"\n")

print("----------------")
roles=dba.command({ 'rolesInfo': 1, 'showBuiltinRoles': True })

print("\n",roles,"\n")

print("----------------")
role=dba.command({
    'rolesInfo': {'role': 'userAdminAnyDatabase','db': 'admin'},
    'showPrivileges': True
})

print("\n",role,"\n")
print("----------------")




cryptohodl_collectetions = dbch.list_collection_names()
database_names = client.list_database_names()

print(database_names)
