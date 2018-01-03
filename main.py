from GBIManager import *
from pymongo import MongoClient

def insert():
    data = {
        'bgi': json.dumps(gbiManager.gbi)
    }
    result = client.gbi.coinmarketcap.insert_one(data)
    print('inserted id: {}'.format(result.inserted_id))

if __name__ == "__main__":
    fbase = 'base'
    gbiManager = GBIManager(fbase)
    gbiManager.calculate_gbi()
    print(gbiManager.gbi)
    client = MongoClient('localhost', 27017)
    insert()