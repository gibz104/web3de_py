import requests
import json
from web3 import Web3


class Opensea:
    def __init__(self):
        self.api_link = 'https://api.opensea.io/api/v1/asset/'

    def get_asset_price(self, contract, id):
        asset_url = self.api_link + str(contract) + '/' + str(id)
        response = requests.request('GET', asset_url)
        print(response)
        asset = json.loads(response.text)

        n_orders = len(asset['orders'])

        if n_orders > 0:
            sell_orders = []
            for order in asset['orders']:
                if order['side'] == 1:
                    sell_orders.append(order)
            if len(sell_orders) > 0:
                current_price = str(Web3.fromWei(float(asset['orders'][-1]['current_price']), 'ether')) + ' ETH'
            else:
                current_price = 'Not Listed'
        else:
            current_price = 'Not Listed'

        return current_price
