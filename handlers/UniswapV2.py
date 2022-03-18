from utils.Decorators import timer
from handlers.Etherscan import contract_get_abi
from dotenv import load_dotenv
from web3 import Web3
import requests
import json
import os


class UniswapV2:

    def __init__(self):
        load_dotenv()
        self.endpoint = os.getenv('WEB3_PROVIDER_GRAPHQL')

        self.factory_addr = '0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f'
        self.contract_abi = contract_get_abi(self.factory_addr)
        self.contract_abi = '[{"inputs":[{"internalType":"address","name":"_feeToSetter","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"token0","type":"address"},{"indexed":true,"internalType":"address","name":"token1","type":"address"},{"indexed":false,"internalType":"address","name":"pair","type":"address"},{"indexed":false,"internalType":"uint256","name":"","type":"uint256"}],"name":"PairCreated","type":"event"},{"constant":true,"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"allPairs","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"allPairsLength","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"}],"name":"createPair","outputs":[{"internalType":"address","name":"pair","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"feeTo","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"feeToSetter","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"getPair","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_feeTo","type":"address"}],"name":"setFeeTo","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_feeToSetter","type":"address"}],"name":"setFeeToSetter","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]'
        self.w3 = Web3(Web3.HTTPProvider(os.getenv('WEB3_PROVIDER_HTTP')))
        self.uni_factory = self.w3.eth.contract(address=self.factory_addr, abi=self.contract_abi)

    def get_reserves(self, pool_addr, block=None):
        if block is not None:
            block = str(block)

        def get_raw_reserves():

            # Returns pool reserves as of latest block
            query = """
            query getReserves($addr: Address!, $block: Long) {
              block (number: $block) {
                number
                pool: account(address: $addr) {
                  reserve: storage(slot: "0x0000000000000000000000000000000000000000000000000000000000000008")
                }
              }
            }
            """
            variables = {'addr': str(pool_addr), 'block': block}
            resp = requests.post(self.endpoint, json={'query': query, 'variables': variables})
            json_data = json.loads(resp.text)
            block_number = json_data['data']['block']['number']
            reserves = json_data['data']['block']['pool']['reserve']
            result = {block_number: reserves}
            return result

        def parse_reserves(reserves: dict):
            if reserves is None:
                return None

            block = float(list(reserves.keys())[0])
            reserves = list(reserves.values())[0].replace('0x', '')

            timestampRaw = reserves[0:8]
            reserve0Raw = reserves[8:36]
            reserve1Raw = reserves[36:64]

            timestamp = Web3.toInt(hexstr=timestampRaw)
            reserve0 = Web3.toInt(hexstr=reserve0Raw)
            reserve1 = Web3.toInt(hexstr=reserve1Raw)

            return {
                'block': block,
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
        token0 = Web3.toChecksumAddress(token0)
        token1 = Web3.toChecksumAddress(token1)
        pool = self.uni_factory.functions.getPair(token0, token1).call()
        return pool

    def get_all_factory_pairs(self):
        nPairs = self.uni_factory.functions.allPairsLength().call()
        pairs = []
        for pair_idx in range(nPairs):
            pool = self.uni_factory.functions.allPairs(pair_idx).call()
            pairs.append(pool)
        return pairs
