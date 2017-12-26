import urllib.request
import json

def get_data(start=""):
    product =[x.strip() for x in open('product')]

    data_ticker = json.loads(urllib.request.urlopen('https://api.coinmarketcap.com/v1/ticker/?start'+start).read())
    data_global = json.loads(urllib.request.urlopen('https://api.coinmarketcap.com/v1/global/').read())
    data_available_ticker = [x for x in data_ticker if x['name'] in product]
    return data_global['total_market_cap_usd'], data_available_ticker

if __name__ == "__main__":
    total_market_cap_usd, data = get_data()
    print("Total Market Cap:",total_market_cap_usd)
    gbi = []
    for d in data:
        price = float(d['price_usd'])
        supply = float(d['total_supply'])
        value = price*supply
        ratio = value/total_market_cap_usd
        print('{:<20}${:<30}{:.2f}%'.format(d['name'], value, ratio*100))
        gbi.append(price*ratio)

    # GBI of base year is 1000
    gbi = sum(list(map(lambda x: (float(x['price_usd'])**2)*float(x['total_supply'])/total_market_cap_usd, data)))

    #TODO calculated gbi conflicts with the real gbi, find the cause
    print('GBI:', gbi)
