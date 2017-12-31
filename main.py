from GBIManager import *
from pymongo import MongoClient
import time

def insert():
    updated_time, gbi = gbiManager.calculate_gbi()
    data = {
        'updated_time': updated_time,
        'bgi': gbi
    }
    result = client.gbi.data.insert_one(data)
    print('inserted id: {}'.format(result.inserted_id))

if __name__ == "__main__":
    fbase = 'base'
    gbiManager = GBIManager(fbase)
    client = MongoClient('localhost', 27017)
    insert()