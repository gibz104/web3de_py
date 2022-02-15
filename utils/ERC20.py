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
    def get_decimals_gql(self):
        query = """
        {
          block {
            number
            call(data: {
              to: "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599"
              data: "0x313ce567"  # Web3.keccak(text='decimals()')
            }) {
              data
              gasUsed
              status
            }
          }
        }
        """

        resp = requests.post(self.endpoint, json={'query': query})
        json_data = json.loads(resp.text)
        print(json_data)
        reserves = json_data['data']['block']['call']['data']
        return Web3.toInt(hexstr=reserves)


erc20 = ERC20Handler()
print(erc20.get_decimals_gql())

