from utils.Decorators import timer
from dotenv import load_dotenv
from web3 import Web3
import os
import requests
import json


class ERC20Handler:
    load_dotenv()
    endpoint = os.getenv('WEB3_PROVIDER_GRAPHQL')

    def get_decimals(self, contract_addr):
        query = """
        query getDecimals($addr: Address!) {
          block {
            number
            call(data: {
              to: $addr
              data: "0x313ce567"  # Web3.keccak(text='decimals()')[:4]
            }) {
              data
              gasUsed
              status
            }
          }
        }
        """

        variables = {'addr': contract_addr}
        resp = requests.post(self.endpoint, json={'query': query, 'variables': variables})
        json_data = json.loads(resp.text)
        decimals = json_data['data']['block']['call']['data']
        return Web3.toInt(hexstr=decimals)

    def get_symbol(self, contract_addr):
        query = """
        query getDecimals($addr: Address!) {
          block {
            number
            call(data: {
              to: $addr
              data: "0x95d89b41"  # Web3.keccak(text='symbol()')[:4]
            }) {
              data
              gasUsed
              status
            }
          }
        }
        """

        variables = {'addr': contract_addr}
        resp = requests.post(self.endpoint, json={'query': query, 'variables': variables})
        json_data = json.loads(resp.text)
        symbol = json_data['data']['block']['call']['data']
        print(symbol)
        symbol = '0x' + symbol[-64:]
        print(symbol)
        return Web3.toText(hexstr=symbol)

    def get_name(self, contract_addr):
        query = """
        query getDecimals($addr: Address!) {
          block {
            number
            call(data: {
              to: $addr
              data: "0x06fdde03"  # Web3.keccak(text='symbol()')[:4]
            }) {
              data
              gasUsed
              status
            }
          }
        }
        """

        variables = {'addr': contract_addr}
        resp = requests.post(self.endpoint, json={'query': query, 'variables': variables})
        json_data = json.loads(resp.text)
        name = json_data['data']['block']['call']['data']
        name = '0x' + name[-64:]
        return Web3.toText(hexstr=name)
