from utils.Decorators import timer, timer_ns
from dotenv import load_dotenv
from web3 import Web3
import requests
import json
import os


class UniswapV2:
    load_dotenv()
    endpoint = os.getenv('WEB3_PROVIDER_GRAPHQL')

    @timer
    def get_reserves(self):
        # Returns pool reserves as of latest block
        query = """
        {
          block {
            number
            pool: account(address: "0xBb2b8038a1640196FbE3e38816F3e67Cba72D940") {
              reserve: storage(slot: "0x0000000000000000000000000000000000000000000000000000000000000008")
            }
          }
        }
        """

        resp = requests.post(self.endpoint, json={'query': query})
        json_data = json.loads(resp.text)
        reserves = json_data['data']['block']['pool']['reserve']
        return reserves

    @timer_ns
    def parse_reserves(self, reserves: str):
        reserves = reserves.replace('0x', '')

        timestampRaw = reserves[0:8]
        reserve0Raw = reserves[8:36]
        reserve1Raw = reserves[36:64]

        timestamp = Web3.toInt(hexstr=timestampRaw)
        reserve0 = Web3.toInt(hexstr=reserve0Raw)
        reserve1 = Web3.toInt(hexstr=reserve1Raw)

        return {
            'timestamp': timestamp,
            'reserve0' : reserve0,
            'reserve1' : reserve1
        }


uni = UniswapV2()
data = uni.get_reserves()
parsed_data = uni.parse_reserves(data)
print(parsed_data)

