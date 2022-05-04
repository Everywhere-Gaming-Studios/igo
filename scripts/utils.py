from brownie import network, accounts, config
from web3 import Web3

DECIMALS = 8
STARTING_PRICE = 200000000000
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
payment_coin_name = "Test DAI"
payment_coin_symbol = "TDAI"
investor_kyc = {'email': "renatomrocha93@gmail.com", 'country': 'Portugal'}


def get_account():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        # Local ganache account
        account = accounts[0]
    else:
        # Getting from env file
        account = accounts.add(config["wallets"]["from_key"])
    return account


# def get_payment_coin():
#     if network.show_active() == 'avax_test':
#         return