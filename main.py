import urllib.request
import json


def get_data():
    product = [x.strip().split(',')[0] for x in open(fbase)]
    data_ticker = json.loads(urllib.request.urlopen('https://api.coinmarketcap.com/v1/ticker/').read())
    data_available_ticker = [x for x in data_ticker if x['name'] in product]
    total_cap = sum([float(x['market_cap_usd']) for x in data_ticker if x['name'] in product])
    return total_cap, data_available_ticker


def get_weighted_base():
    base = 0
    for d in [x.strip().split(',') for x in open(fbase)]:
        base += float(d[2])*float(d[1])
    return base


def calculate_gbi():
    total_market_cap_usd, data = get_data()
    weighted_avg = 0
    for d in data:
        cap_usd = float(d['market_cap_usd'])
        for d2 in [x.strip().split(',') for x in open(fbase)]:
            if d['name'] == d2[0]:
                ratio = float(d2[1])
        weighted_avg += cap_usd * ratio
    return weighted_avg / get_weighted_base() * 1000


if __name__ == "__main__":
    fbase = 'base'
    gbi = calculate_gbi()
    # error range 1.5%
    print('GBI:', gbi)
