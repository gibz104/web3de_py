from web3 import Web3

# TODO: better gas price / base fee estimation


class Transactions:
    def __init__(self, provider, private_key, public_address):
        self.web3_provider = provider
        self.private_key = private_key
        self.public_address = public_address
        # self.w3 = Web3(Web3.WebsocketProvider(self.web3_provider))
        self.w3 = Web3(Web3.HTTPProvider(self.web3_provider))

    def sendTx_legacy(self, to, amount, data=''):
        nonce = self.w3.eth.get_transaction_count(self.public_address)
        amount = Web3.toWei(amount, 'ether')
        transaction = {
            'to': to,
            'value': amount,
            'gas': self.w3.eth.estimate_gas({'to': to, 'value': amount, 'data': data}),
            'gasPrice': self.w3.eth.gas_price,
            'nonce': nonce,
            'data': data
        }
        signedTx = self.w3.eth.account.sign_transaction(transaction, self.private_key)
        txHash = self.w3.eth.send_raw_transaction(signedTx.rawTransaction)
        return Web3.toHex(txHash)

    def sendTx(self, to, amount, data=''):
        nonce = self.w3.eth.get_transaction_count(self.public_address)
        amount = Web3.toWei(amount, 'ether')
        transaction = {
            'to': to,
            'value': amount,
            'gas': self.w3.eth.estimate_gas({'to': to, 'value': amount, 'data': data}),
            'maxFeePerGas': self.w3.eth.gas_price,
            'maxPriorityFeePerGas': self.w3.eth.gas_price,
            'nonce': nonce,
            'data': data,
            'chainId': 31337
        }
        signedTx = self.w3.eth.account.sign_transaction(transaction, self.private_key)
        txHash = self.w3.eth.send_raw_transaction(signedTx.rawTransaction)
        return Web3.toHex(txHash)
