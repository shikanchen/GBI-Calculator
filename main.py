import urllib.request
import json
from datetime import datetime


def get_data():
    product = [x.strip().split(',')[0] for x in open(fbase)]
    data_ticker = json.loads(urllib.request.urlopen('https://api.coinmarketcap.com/v1/ticker/').read())
    data_available_ticker = [x for x in data_ticker if x['name'] in product]
    total_cap = sum([float(x['market_cap_usd']) for x in data_ticker if x['name'] in product])

    print(datetime.fromtimestamp(int(data_ticker[0]['last_updated'])).strftime('%Y-%m-%d %H:%M:%S'))

    return total_cap, data_available_ticker


def get_weighted_base():
    total = sum([float(x.strip().split(',')[1]) for x in open(fbase)])
    base = 0
    for d in [float(x.strip().split(',')[1]) for x in open(fbase)]:
        base += d*d/total

    return base


def calculate_gbi():
    total_market_cap_usd, data = get_data()
    weighted_avg = 0
    for d in data:
        cap_usd = float(d['available_supply']) * float(d['price_usd'])
        ratio = cap_usd / total_market_cap_usd
        weighted_avg += cap_usd * ratio
    return weighted_avg / get_weighted_base() * 1000


if __name__ == "__main__":
    fbase = 'base'
    gbi = calculate_gbi()
    # TODO the cause could be that weight is calculated as independent of its corresponding value
    print('GBI:', gbi)
