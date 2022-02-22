from utils.Decorators import timer
from dotenv import load_dotenv
import requests
import json
import os


class Storage:
    load_dotenv()
    endpoint = os.getenv('WEB3_PROVIDER_GRAPHQL')

    @timer
    def get_storage_slot(self, contract_addr, slot):
        # returns raw storage slot value for provided slot and contract

        query = """
        query getReserves($addr: Address!, $slot: Bytes32!) {
          block {
            number
            contract: account(address: $addr) {
              storage_slot: storage(slot: $slot)
            }
          }
        }
        """

        # Pad slot number
        zeros = 64 - len(str(slot))
        slot = f'0x' + f'{str("0" * zeros)}' + str(slot)

        # Call GraphQL endpoint
        variables = {'addr': contract_addr, 'slot': slot}
        resp = requests.post(self.endpoint, json={'query': query, 'variables': variables})
        json_data = json.loads(resp.text)
        storage = json_data['data']['block']['contract']['storage_slot']
        return storage

    def search_storage_slots(self, contract_addr, search_string, nslots = 10000):
        # loops through early storage slots for a specific search string
        # TODO: find way to loop through all storage slot of a contract efficiently (about 1T [2^256] slots)
        #       ...maybe with parallelization

        query = """
                query getReserves($addr: Address!, $slot: Bytes32!) {
                  block {
                    number
                    contract: account(address: $addr) {
                      storage_slot: storage(slot: $slot)
                    }
                  }
                }
                """

        for i in range(nslots):
            # Pad slot number
            zeros = 64 - len(str(i))
            slot = f'0x' + f'{str("0" * zeros)}' + str(i)

            # Call GraphQL endpoint
            variables = {'addr': contract_addr, 'slot': slot}
            resp = requests.post(self.endpoint, json={'query': query, 'variables': variables})
            json_data = json.loads(resp.text)
            storage = json_data['data']['block']['contract']['storage_slot']

            if search_string in storage:
                print(f'Found "{search_string}" in storage slot: {i}')
