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
    # source list
    #   `coinmarketcap`
    #   `binance`
    #   `kraken`
    gbiManager.calculate_gbi(['coinmarketcap', 'binance', 'kraken'])
    print(gbiManager.gbi)
    client = MongoClient('localhost', 27017)
    insert()
