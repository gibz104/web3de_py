from ratelimit import limits, sleep_and_retry
from web3 import Web3
import requests
import json


class Etherscan:
    """ Wrapper to free Etherscan api; includes rate limiter checks"""
    RATE_LIMIT = 1
    RATE_LIMIT_PERIOD_SECONDS = 6

    @sleep_and_retry
    @limits(calls=RATE_LIMIT, period=RATE_LIMIT_PERIOD_SECONDS)
    def contract_get_abi(self, addr):
        endpoint = f'https://api.etherscan.io/api?module=contract&action=getabi&address={addr}'

        resp = requests.get(endpoint).json()
        abi = json.loads(resp['result'])
        return str(abi)

    @sleep_and_retry
    @limits(calls=RATE_LIMIT, period=RATE_LIMIT_PERIOD_SECONDS)
    def contract_get_source_code(self, addr):
        endpoint = f'https://api.etherscan.io/api?module=contract&action=getsourcecode&address={addr}'

        resp = requests.get(endpoint).json()
        code = resp['result'][0]['SourceCode']
        return str(code)

    @sleep_and_retry
    @limits(calls=RATE_LIMIT, period=RATE_LIMIT_PERIOD_SECONDS)
    def account_get_ether_balance(self, addr):
        endpoint = f'https://api.etherscan.io/api?module=account&action=balance&address={addr}&tag=latest'

        resp = requests.get(endpoint).json()
        print(resp)
        balance = json.loads(resp['result'])
        balance = Web3.fromWei(balance, 'Ether')
        return balance

    @sleep_and_retry
    @limits(calls=RATE_LIMIT, period=RATE_LIMIT_PERIOD_SECONDS)
    def account_get_normal_transactions(self, addr):
        # Returns MAX 10k transactions
        endpoint = f'https://api.etherscan.io/api?module=account&action=txlist&address={addr}&startblock=0&endblock=99999999&sort=desc'

        resp = requests.get(endpoint).json()
        normal_tx = resp['result']
        return normal_tx

    @sleep_and_retry
    @limits(calls=RATE_LIMIT, period=RATE_LIMIT_PERIOD_SECONDS)
    def account_get_internal_transactions(self, addr):
        # Returns MAX 10k transactions
        endpoint = f'https://api.etherscan.io/api?module=account&action=txlistinternal&address={addr}&startblock=0&endblock=99999999&sort=desc'

        resp = requests.get(endpoint).json()
        internal_tx = resp['result']
        return internal_tx

    @sleep_and_retry
    @limits(calls=RATE_LIMIT, period=RATE_LIMIT_PERIOD_SECONDS)
    def account_get_ERC20_transfers(self, addr):
        endpoint = f'https://api.etherscan.io/api?module=account&action=tokentx&address={addr}&startblock=0&endblock=99999999&sort=desc'

        resp = requests.get(endpoint).json()
        token_transfers = resp['result']
        return token_transfers

    @sleep_and_retry
    @limits(calls=RATE_LIMIT, period=RATE_LIMIT_PERIOD_SECONDS)
    def account_get_ERC721_transfers(self, addr):
        endpoint = f'https://api.etherscan.io/api?module=account&action=tokennfttx&address={addr}&startblock=0&endblock=99999999&sort=desc'

        resp = requests.get(endpoint).json()
        token_transfers = resp['result']
        return token_transfers

    @sleep_and_retry
    @limits(calls=RATE_LIMIT, period=RATE_LIMIT_PERIOD_SECONDS)
    def transactions_get_internal_transactions(self, tx):
        endpoint = f'https://api.etherscan.io/api?module=account&action=txlistinternal&txhash={tx}'

        resp = requests.get(endpoint).json()
        internal_tx = resp['result']
        return internal_tx

    @sleep_and_retry
    @limits(calls=RATE_LIMIT, period=RATE_LIMIT_PERIOD_SECONDS)
    def gas_estimate(self):
        endpoint = f'https://api.etherscan.io/api?module=gastracker&action=gasoracle'

        resp = requests.get(endpoint).json()
        gas = resp['result']
        return gas
