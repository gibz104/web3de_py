from utils.Decorators import timer
from dotenv import load_dotenv
from web3 import Web3
import requests
import json
import os

# TODO: Use graphql fragments(?) to make reserve queries dynamic (can look up multiple pools in one call)
# TODO: return block number in addition to timestamp when getting reserves


class UniswapV2:
    load_dotenv()
    endpoint = os.getenv('WEB3_PROVIDER_GRAPHQL')

    def get_reserves(self, pool_addr):

        def get_raw_reserves():
            # Returns pool reserves as of latest block
            query = """
            query getReserves($addr: Address!) {
              block {
                number
                pool: account(address: $addr) {
                  # getReserves() storage slot
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

        def parse_reserves(reserves: str):
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

        rawReserves = get_raw_reserves()
        parsedReserves = parse_reserves(rawReserves)
        return parsedReserves

    def get_pool_tokens(self, pool_addr):
        # Returns tokens of uni pool
        query = """
        query getReserves($addr: Address!) {
          block {
            number
            pool: account(address: $addr) {
              token0: storage(slot: "0x0000000000000000000000000000000000000000000000000000000000000006")
              token1: storage(slot: "0x0000000000000000000000000000000000000000000000000000000000000007")
            }
          }
        }
        """

        # Creates and send GraphQL query
        variables = {'addr': pool_addr}
        resp = requests.post(self.endpoint, json={'query': query, 'variables': variables})
        json_data = json.loads(resp.text)
        tokens = json_data['data']['block']['pool']

        # Remove zero padding
        tokens['token0'] = '0x' + tokens['token0'][-40:]
        tokens['token1'] = '0x' + tokens['token1'][-40:]
        return tokens

    def get_factory_pair(self, token0, token1):
        # given two token addresses, return the address of the pool (using uniswap factory address)
        # option to only give one address, which will return all pools containing that token addr (there is a seperate contract function that returns this)
        pass

    def get_pool_volume(self, block_range):
        # need to look into how to get this...
        # given a number of blocks, return volume of uni pool from latest block minus block_range to latest block
        # maybe need to look at transfer events per block; maybe need to standardize in one currency (so volume is comparable across diff pools)
        pass
