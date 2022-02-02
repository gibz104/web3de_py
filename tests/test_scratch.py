import os
from dotenv import load_dotenv
from web3 import Web3

from utils.Transactions import Transactions
from handlers.Opensea import Opensea


# TODO: build out more in Opensea
# TODO: build util for address watcher (sends alerts for activity on provided addresses)
#       - log alert
#       - Discord alert
#       - Twilio sms alert
# TODO: to YAML or to TOML ...? Build config file with smart contracts as addresses and attributes, like names, ABIs, etc. attributes
#       - find ways to automate attributes?  like getting names of smart contracts with only address?


load_dotenv()


## testing sending a transaction using Transactions util
provider = os.getenv('WEB3_PROVIDER_HTTP')
private_key = os.getenv('PRIVATE_KEY')
public_address = Web3.toChecksumAddress(os.getenv('PUBLIC_ADDRESS'))

tx = Transactions(provider, private_key, public_address)
txHash = tx.sendTx(public_address, 0.01)
print(txHash)


# ## testing getting asset price for an Opensea collection
# os = Opensea()
#
# # galactic apes smart contract
# # https://opensea.io/assets/0x12d2d1bed91c24f878f37e66bd829ce7197e4d14/494
# price = os.get_asset_price('0x12d2d1bed91c24f878f37e66bd829ce7197e4d14', '494')
# print(price)

