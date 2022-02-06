import requests
import json
import os
from web3 import Web3
from typing import List
from dotenv import load_dotenv


class LooksRare:
    def __init__(self):
        load_dotenv()
        self.exchange_contract = '0x59728544B08AB483533076417FbBB2fD0B17CE3a'
        self.contract_abi = '[{"inputs":[{"internalType":"address","name":"_currencyManager","type":"address"},{"internalType":"address","name":"_executionManager","type":"address"},{"internalType":"address","name":"_royaltyFeeManager","type":"address"},{"internalType":"address","name":"_WETH","type":"address"},{"internalType":"address","name":"_protocolFeeRecipient","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"newMinNonce","type":"uint256"}],"name":"CancelAllOrders","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256[]","name":"orderNonces","type":"uint256[]"}],"name":"CancelMultipleOrders","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"currencyManager","type":"address"}],"name":"NewCurrencyManager","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"executionManager","type":"address"}],"name":"NewExecutionManager","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"protocolFeeRecipient","type":"address"}],"name":"NewProtocolFeeRecipient","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"royaltyFeeManager","type":"address"}],"name":"NewRoyaltyFeeManager","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"transferSelectorNFT","type":"address"}],"name":"NewTransferSelectorNFT","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"collection","type":"address"},{"indexed":true,"internalType":"uint256","name":"tokenId","type":"uint256"},{"indexed":true,"internalType":"address","name":"royaltyRecipient","type":"address"},{"indexed":false,"internalType":"address","name":"currency","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"RoyaltyPayment","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bytes32","name":"orderHash","type":"bytes32"},{"indexed":false,"internalType":"uint256","name":"orderNonce","type":"uint256"},{"indexed":true,"internalType":"address","name":"taker","type":"address"},{"indexed":true,"internalType":"address","name":"maker","type":"address"},{"indexed":true,"internalType":"address","name":"strategy","type":"address"},{"indexed":false,"internalType":"address","name":"currency","type":"address"},{"indexed":false,"internalType":"address","name":"collection","type":"address"},{"indexed":false,"internalType":"uint256","name":"tokenId","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"price","type":"uint256"}],"name":"TakerAsk","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bytes32","name":"orderHash","type":"bytes32"},{"indexed":false,"internalType":"uint256","name":"orderNonce","type":"uint256"},{"indexed":true,"internalType":"address","name":"taker","type":"address"},{"indexed":true,"internalType":"address","name":"maker","type":"address"},{"indexed":true,"internalType":"address","name":"strategy","type":"address"},{"indexed":false,"internalType":"address","name":"currency","type":"address"},{"indexed":false,"internalType":"address","name":"collection","type":"address"},{"indexed":false,"internalType":"uint256","name":"tokenId","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"price","type":"uint256"}],"name":"TakerBid","type":"event"},{"inputs":[],"name":"DOMAIN_SEPARATOR","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"WETH","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"minNonce","type":"uint256"}],"name":"cancelAllOrdersForSender","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256[]","name":"orderNonces","type":"uint256[]"}],"name":"cancelMultipleMakerOrders","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"currencyManager","outputs":[{"internalType":"contract ICurrencyManager","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"executionManager","outputs":[{"internalType":"contract IExecutionManager","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint256","name":"orderNonce","type":"uint256"}],"name":"isUserOrderNonceExecutedOrCancelled","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"components":[{"internalType":"bool","name":"isOrderAsk","type":"bool"},{"internalType":"address","name":"taker","type":"address"},{"internalType":"uint256","name":"price","type":"uint256"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"uint256","name":"minPercentageToAsk","type":"uint256"},{"internalType":"bytes","name":"params","type":"bytes"}],"internalType":"struct OrderTypes.TakerOrder","name":"takerBid","type":"tuple"},{"components":[{"internalType":"bool","name":"isOrderAsk","type":"bool"},{"internalType":"address","name":"signer","type":"address"},{"internalType":"address","name":"collection","type":"address"},{"internalType":"uint256","name":"price","type":"uint256"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"address","name":"strategy","type":"address"},{"internalType":"address","name":"currency","type":"address"},{"internalType":"uint256","name":"nonce","type":"uint256"},{"internalType":"uint256","name":"startTime","type":"uint256"},{"internalType":"uint256","name":"endTime","type":"uint256"},{"internalType":"uint256","name":"minPercentageToAsk","type":"uint256"},{"internalType":"bytes","name":"params","type":"bytes"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"internalType":"struct OrderTypes.MakerOrder","name":"makerAsk","type":"tuple"}],"name":"matchAskWithTakerBid","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"components":[{"internalType":"bool","name":"isOrderAsk","type":"bool"},{"internalType":"address","name":"taker","type":"address"},{"internalType":"uint256","name":"price","type":"uint256"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"uint256","name":"minPercentageToAsk","type":"uint256"},{"internalType":"bytes","name":"params","type":"bytes"}],"internalType":"struct OrderTypes.TakerOrder","name":"takerBid","type":"tuple"},{"components":[{"internalType":"bool","name":"isOrderAsk","type":"bool"},{"internalType":"address","name":"signer","type":"address"},{"internalType":"address","name":"collection","type":"address"},{"internalType":"uint256","name":"price","type":"uint256"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"address","name":"strategy","type":"address"},{"internalType":"address","name":"currency","type":"address"},{"internalType":"uint256","name":"nonce","type":"uint256"},{"internalType":"uint256","name":"startTime","type":"uint256"},{"internalType":"uint256","name":"endTime","type":"uint256"},{"internalType":"uint256","name":"minPercentageToAsk","type":"uint256"},{"internalType":"bytes","name":"params","type":"bytes"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"internalType":"struct OrderTypes.MakerOrder","name":"makerAsk","type":"tuple"}],"name":"matchAskWithTakerBidUsingETHAndWETH","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"components":[{"internalType":"bool","name":"isOrderAsk","type":"bool"},{"internalType":"address","name":"taker","type":"address"},{"internalType":"uint256","name":"price","type":"uint256"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"uint256","name":"minPercentageToAsk","type":"uint256"},{"internalType":"bytes","name":"params","type":"bytes"}],"internalType":"struct OrderTypes.TakerOrder","name":"takerAsk","type":"tuple"},{"components":[{"internalType":"bool","name":"isOrderAsk","type":"bool"},{"internalType":"address","name":"signer","type":"address"},{"internalType":"address","name":"collection","type":"address"},{"internalType":"uint256","name":"price","type":"uint256"},{"internalType":"uint256","name":"tokenId","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"address","name":"strategy","type":"address"},{"internalType":"address","name":"currency","type":"address"},{"internalType":"uint256","name":"nonce","type":"uint256"},{"internalType":"uint256","name":"startTime","type":"uint256"},{"internalType":"uint256","name":"endTime","type":"uint256"},{"internalType":"uint256","name":"minPercentageToAsk","type":"uint256"},{"internalType":"bytes","name":"params","type":"bytes"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"internalType":"struct OrderTypes.MakerOrder","name":"makerBid","type":"tuple"}],"name":"matchBidWithTakerAsk","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"protocolFeeRecipient","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"royaltyFeeManager","outputs":[{"internalType":"contract IRoyaltyFeeManager","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"transferSelectorNFT","outputs":[{"internalType":"contract ITransferSelectorNFT","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_currencyManager","type":"address"}],"name":"updateCurrencyManager","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_executionManager","type":"address"}],"name":"updateExecutionManager","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_protocolFeeRecipient","type":"address"}],"name":"updateProtocolFeeRecipient","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_royaltyFeeManager","type":"address"}],"name":"updateRoyaltyFeeManager","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_transferSelectorNFT","type":"address"}],"name":"updateTransferSelectorNFT","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"userMinOrderNonce","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'
        self.w3 = Web3(Web3.HTTPProvider(os.getenv('WEB3_PROVIDER_HTTP')))
        self.lr = self.w3.eth.contract(address=self.exchange_contract, abi=self.contract_abi)

    def get_contract_owner(self):
        owner = self.lr.functions.owner().call()
        return owner

    def get_min_order_nonce(self, user: str):
        minNonce = self.lr.functions.userMinOrderNonce(user).call()
        return minNonce

    def cancel_all_orders(self, minNonce: int):
        tx_hash = self.lr.functions.cancelAllOrderForSender(minNonce).transact()
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_receipt

    def cancel_multiple_maker_orders(self, orderNonces: List[int]):
        tx_hash = self.lr.functions.cancelMultipleMakerOrders(orderNonces).transact()
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_receipt

