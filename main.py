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

def stop():
    stopped = True

if __name__ == "__main__":
    fbase = 'base'
    gbiManager = GBIManager(fbase)
    stopped = False
    client = MongoClient('localhost', 27017)

    while not stopped:
        insert()
        # insert a new set of data every 10 mins
        time.sleep(600)
