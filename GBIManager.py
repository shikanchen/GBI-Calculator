import urllib.request
import json


class GBIManager(object):
    def __init__(self, fname):
        self.base = fname

    def get_data(self):
        product = [x.strip().split(',')[0] for x in open(self.base)]
        data_ticker = json.loads(urllib.request.urlopen('https://api.coinmarketcap.com/v1/ticker/').read())
        data_available_ticker = [x for x in data_ticker if x['name'] in product]
        total_cap = sum([float(x['market_cap_usd']) for x in data_ticker if x['name'] in product])
        self.time = float(
            json.loads(urllib.request.urlopen('https://api.coinmarketcap.com/v1/global/').read())['last_updated'])
        return total_cap, data_available_ticker

    def get_weighted_base(self):
        base = 0
        for d in [x.strip().split(',') for x in open(self.base)]:
            base += float(d[2]) * float(d[1])
        return base

    def calculate_gbi(self):
        total_market_cap_usd, data = self.get_data()
        weighted_avg = 0
        for d in data:
            cap_usd = float(d['market_cap_usd'])
            for d2 in [x.strip().split(',') for x in open(self.base)]:
                if d['name'] == d2[0]:
                    ratio = float(d2[1])
            weighted_avg += cap_usd * ratio
        self.gbi = weighted_avg / self.get_weighted_base() * 1000
        return self.time, self.gbi
