from dotenv import load_dotenv
import requests
import json
import os


class UniswapV2:
    load_dotenv()
    endpoint = os.getenv('WEB3_PROVIDER_GRAPHQL')

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


uni = UniswapV2()
data = uni.get_reserves()
print(data)
