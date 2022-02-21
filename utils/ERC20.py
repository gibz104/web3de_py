from utils.Decorators import timer
from dotenv import load_dotenv
from web3 import Web3
import os
import requests
import json


class ERC20Handler:
    load_dotenv()
    endpoint = os.getenv('WEB3_PROVIDER_GRAPHQL')

    @timer
    def get_decimals(self, contract_addr):
        query = """
        query getDecimals($addr: Address!) {
          block {
            number
            call(data: {
              to: $addr
              data: "0x313ce567"  # Web3.keccak(text='decimals()')
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
        reserves = json_data['data']['block']['call']['data']
        return Web3.toInt(hexstr=reserves)
