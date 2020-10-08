import dotenv
import os
import requests as request
import hmac
import time
import json
from datetime import datetime
import urllib
import hashlib
from pprint import pprint

dotenv.load_dotenv()
print(os.getenv('API_KEY'))

def get_lot_size_binance(symbol):
    print('Inside getLotsizeBinance')
    print(symbol)
    # looking for lot size
    url_avp = f'https://www.binance.com/fapi/v1/exchangeInfo?symbol={symbol}'
    current = request.get(url_avp).json()
    # pprint(current)
    filters_exist=list(filter(lambda x:x['symbol']==str(symbol),current['symbols']))[0]['filters']
    lot_size=list(filter(lambda x:x['filterType']=='LOT_SIZE',filters_exist))[0]
    print(lot_size)
    return lot_size

def get_quantity(symbol, amout_per_trade, match_price):
    quantity_init = amout_per_trade / match_price
    print('quantity_init: ')
    print(quantity_init)
    
    filters = get_lot_size_binance(symbol)
    print(filters)

    quantity = quantity_init - (quantity_init % float(filters['stepSize']))
    print('Quantity after dividing step size: ')
    print(quantity)

    quantity = float("{:.5f}".format(quantity))
    print('Final Quantity: ')
    print(quantity)
    
    return quantity

def buy(symbol, side):
    headers = {'Content-Type': 'application/json'}
    timestamp = request.get("https://fapi.binance.com/fapi/v1/time", headers=headers).json()['serverTime']
    request_url = "https://fapi.binance.com/fapi/v1/order?"
    querystring = urllib.parse.urlencode({
        "side": "BUY" if side == 'LONG' else 'SELL',
        "symbol": symbol,
        "type": "MARKET",
        "positionSide": side,
        "quantity": get_quantity(symbol, 15, 2.6393),
        "timestamp": str(timestamp)
    })

    signature = hmac.new(os.getenv('SECRET_KEY').encode('utf-8'), querystring.encode('utf-8'),
                        hashlib.sha256).hexdigest()

    request_url += querystring + '&signature=' + signature

    headers = {'Content-Type': 'application/json',
            'X-MBX-APIKEY': os.getenv('API_KEY')}
    res = request.post(request_url, headers=headers)
    print("==============================================================")
    print(headers)
    print(request_url)
    print(res.status_code)
    print("==============================================================")
    pprint(json.loads(res.text))
    if res.status_code == 200:
        res = json.loads(res.text)

        if res['status'] == 'NEW':
            print('=====================insert_buy=============================================')
            print("We bought that trade")
        else:
            return {"data": res.status_code}
        
def sell(symbol, side):
    headers = {'Content-Type': 'application/json'}
    timestamp = request.get("https://fapi.binance.com/fapi/v1/time", headers=headers).json()['serverTime']
    request_url = "https://fapi.binance.com/fapi/v1/order?"
    querystring = urllib.parse.urlencode({
        "side": "BUY" if side == 'SHORT' else 'SELL',
        "symbol": symbol,
        "type": "MARKET",
        "positionSide": side,
        "quantity": get_quantity(symbol, 15, 2.6393),
        "timestamp": str(timestamp)
    })

    signature = hmac.new(os.getenv('SECRET_KEY').encode('utf-8'), querystring.encode('utf-8'),
                        hashlib.sha256).hexdigest()

    request_url += querystring + '&signature=' + signature

    headers = {'Content-Type': 'application/json',
            'X-MBX-APIKEY': os.getenv('API_KEY')}
    res = request.post(request_url, headers=headers)
    print("==============================================================")
    print(headers)
    print(request_url)
    print(res.status_code)
    print("==============================================================")
    pprint(json.loads(res.text))
    if res.status_code == 200:
        res = json.loads(res.text)

        if res['status'] == 'NEW':
            print('=====================insert_buy=============================================')
            print("We bought that trade")
        else:
            return {"data": res.status_code}
        
if __name__ == '__main__':
    # buy(
    #     symbol='EOSUSDT',
    #     side='SHORT',
    # )
    sell(
        symbol='EOSUSDT',
        side='SHORT',
    )
    # get_lot_size_binance('EOSUSDT')
    # get_quantity('EOSUSDT', 15, 2.6393)