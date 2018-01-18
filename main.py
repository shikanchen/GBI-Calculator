from GBIManager import *
from pymongo import MongoClient


def insert():
    data = {
        'cache': json.dumps(gbiManager.cache['latest_gbi']),
        'bgi': json.dumps(gbiManager.gbi)
    }
    result = client.gbi.insert_one(data)
    print('inserted id: {}'.format(result.inserted_id))


if __name__ == "__main__":
    fbase = 'base'
    gbiManager = GBIManager(fbase)
    gbiManager.calculate_gbi(['coinmarketcap', 'binance', 'kraken'])
    print(gbiManager.gbi)
    client = MongoClient('localhost', 27017)
    insert()
