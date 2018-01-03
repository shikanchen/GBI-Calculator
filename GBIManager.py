import datetime
import urllib.request
import json
from urllib.error import HTTPError


class GBIManager(object):
    def __init__(self, fname, tmp='tmp/'+str(datetime.date.today())):
        self.base = fname
        self.tmp = tmp
        self.gbi = {}

    def get_weighted_base(self):
        base = 0
        for d in [x.strip().split(',') for x in open(self.base)]:
            base += float(d[2]) * float(d[1])
        return base

    def calculate_gbi(self):
        product = [x.strip().split(',')[0] for x in open(self.base)]
        ftmp = open(self.tmp, 'w')
        # source `coinmarketcap`
        data_ticker = json.loads(urllib.request.urlopen('https://api.coinmarketcap.com/v1/ticker/').read())
        data = [x for x in data_ticker if x['symbol'] in product]
        time = float(
            json.loads(urllib.request.urlopen('https://api.coinmarketcap.com/v1/global/').read())['last_updated'])
        weighted_avg = 0
        for d in data:
            cap_usd = float(d['market_cap_usd'])
            for d2 in [x.strip().split(',') for x in open(self.base)]:
                if d['symbol'] == d2[0]:
                    ratio = float(d2[1])
            ftmp.write(d['symbol']+','+str(cap_usd * ratio)+'\n')
            weighted_avg += cap_usd * ratio
        ftmp.close()
        self.gbi['coinmarketcap'] = time, weighted_avg / self.get_weighted_base() * 1000
        # source `binance`
        for p in product:
            if p == 'BTC':
                ratio = float(d2[1])
                d =json.loads(urllib.request.urlopen('https://api.binance.com/api/v1/trades?symbol=' + p + 'USDT').read())[-1]
                BTC_price = float(d['price'])
                cap_usd = float(d['price']) * float(d['qty'])
                weighted_avg += cap_usd * ratio
                continue

            try:
                d = json.loads(urllib.request.urlopen('https://api.binance.com/api/v1/trades?symbol='+p+'BTC').read())[-1]
            except HTTPError:
                for t in [x.strip().split(',') for x in open(self.tmp)]:
                    if t[0] == p:
                        weighted_avg += float(t[1])
                continue

            cap_usd = float(d['price']) * BTC_price * float(d['qty'])
            for d2 in [x.strip().split(',') for x in open(self.base)]:
                if p == d2[0]:
                    ratio = float(d2[1])
            weighted_avg += cap_usd * ratio
            time = d['time']
        self.gbi['binance'] = time, weighted_avg / self.get_weighted_base() * 1000