from utils.Decorators import timer
from dotenv import load_dotenv
from web3 import Web3
import requests
import json
import os

# TODO: Use graphql fragments(?) to make reserve queries dynamic (can look up multiple pools in one call)


class UniswapV2:
    load_dotenv()
    endpoint = os.getenv('WEB3_PROVIDER_GRAPHQL')

    def get_reserves(self, pool_addr):
        rawReserves = self.get_raw_reserves(pool_addr)
        parsedReserves = self.parse_reserves(rawReserves)
        return parsedReserves

    @timer
    def get_raw_reserves(self, pool_addr):
        # Returns pool reserves as of latest block
        query = """
        query getReserves($addr: Address!) {
          block {
            number
            pool: account(address: $addr) {
              reserve: storage(slot: "0x0000000000000000000000000000000000000000000000000000000000000008")
            }
          }
        }
        """
        variables = {'addr': pool_addr}
        resp = requests.post(self.endpoint, json={'query': query, 'variables': variables})
        json_data = json.loads(resp.text)
        reserves = json_data['data']['block']['pool']['reserve']
        return reserves

    def parse_reserves(self, reserves: str):
        if reserves is None:
            return None

        reserves = reserves.replace('0x', '')

        timestampRaw = reserves[0:8]
        reserve0Raw = reserves[8:36]
        reserve1Raw = reserves[36:64]

        timestamp = Web3.toInt(hexstr=timestampRaw)
        reserve0 = Web3.toInt(hexstr=reserve0Raw)
        reserve1 = Web3.toInt(hexstr=reserve1Raw)

        return {
            'timestamp': timestamp,
            'reserve0': reserve0,
            'reserve1': reserve1
        }
