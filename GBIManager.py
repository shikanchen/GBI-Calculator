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

    def calculate_gbi(self, sources):
        product = [x.strip().split(',')[0] for x in open(self.base)]

        # source list
        # source `coinmarketcap`
        # source `binance`
        for source in sources:
            eval('self.source_{}({})'.format(source, product))

    def source_coinmarketcap(self, product):
        ftmp = open(self.tmp, 'w')
        data_ticker = json.loads(urllib.request.urlopen('https://api.coinmarketcap.com/v1/ticker/').read())
        data = [x for x in data_ticker if x['symbol'] in product]
        time = int(json.loads(urllib.request.urlopen('https://api.coinmarketcap.com/v1/global/').read())['last_updated'])
        weighted_avg = 0
        for d in data:
            cap_usd = float(d['market_cap_usd'])
            for d2 in [x.strip().split(',') for x in open(self.base)]:
                if d['symbol'] == d2[0]:
                    ratio = float(d2[1])
            ftmp.write(','.join([d['symbol'],str(cap_usd*ratio), d['total_supply']]) + '\n')
            weighted_avg += cap_usd * ratio
        ftmp.close()
        print(d2)
        self.gbi['coinmarketcap'] = time, weighted_avg / self.get_weighted_base() * 1000

    def source_binance(self, product):
        weighted_avg = 0
        for p in product:
            if p == 'BTC':
                d2 = list(filter(lambda x: x[0] == p, [x.strip().split(',') for x in open(self.base)]))[0]
                print(d2)
                ratio = float(d2[1])
                BTC_price =json.loads(urllib.request.urlopen('https://api.binance.com/api/v1/trades?symbol='+p+'USDT').read())[-1]['price']
                BTC_price = float(BTC_price)
                qty = json.loads(urllib.request.urlopen('https://api.binance.com/api/v1/ticker/24hr?symbol='+p+'USDT').read())['volume']
                print(qty)
                cap_usd = BTC_price * float(qty)
                weighted_avg += cap_usd * ratio
                continue

            try:
                qty = json.loads(
                    urllib.request.urlopen('https://api.binance.com/api/v1/ticker/24hr?symbol=' + p + 'BTC').read())[
                    'volume']
                price = json.loads(urllib.request.urlopen('https://api.binance.com/api/v1/trades?symbol='+p+'BTC').read())[-1]['price']
            except HTTPError:
                for t in [x.strip().split(',') for x in open(self.tmp)]:
                    if t[0] == p:
                        weighted_avg += float(t[1])
                continue

            for t in [x.strip().split(',') for x in open(self.tmp)]:
                if p == t[0]:
                    cap_usd = float(price) * BTC_price * float(t[2])
            for d2 in [x.strip().split(',') for x in open(self.base)]:
                if p == d2[0]:
                    ratio = float(d2[1])
            weighted_avg += cap_usd * ratio
            time = json.loads(urllib.request.urlopen('https://api.binance.com/api/v1/trades?symbol='+p+'BTC').read())[-1]['time']
        self.gbi['binance'] = time, weighted_avg / self.get_weighted_base() * 1000