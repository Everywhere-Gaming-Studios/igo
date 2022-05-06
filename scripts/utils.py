from brownie import FlattenedIgoToken, PublicIgo, IgoToken, PaymentCoin, accounts, network, config
import os

DECIMALS = 8
STARTING_PRICE = 200000000000
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
payment_coin_name = "Test DAI"
payment_coin_symbol = "TDAI"
investor_kyc = {'email': "renatomrocha93@gmail.com", 'country': 'Portugal'}

DEPLOY_ENV = os.getenv('DEPLOY_ENV')


def get_account():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        # Local ganache account
        account = accounts[0]
    else:
        print("Fetching credentials from live network")
        if DEPLOY_ENV == 'MAINNET':
            print("Fetching mainnet wallet")
            account = accounts.add(config["wallets"]["from_key"])
        else:
            print("Fetching testnet wallet")
            account = accounts.add(config["test_wallets"]["from_key"])
    return account



def deploy_payment_coin():
    return PaymentCoin.deploy(payment_coin_name, payment_coin_symbol, {"from": get_account()})


def deploy_public_igo():
    active_network = network.show_active()
    payment_coin = deploy_payment_coin()
    print(f"Deploying on network: {active_network}")
    public_igo = PublicIgo.deploy(config['igo_token_params']['price_numerator'], config['igo_token_params']['price_denominator'], payment_coin.address, config['igo_token_params']['max_presale_mint'], {"from": get_account()})
    return public_igo, payment_coin


def deploy_igo_token_factory():
    public_igo, payment_coin = deploy_public_igo()
    igo_token = IgoToken.deploy(config['igo_token_params']['name'], config['igo_token_params']['symbol'], public_igo.address, config['igo_token_params']['max_amount'], {"from": get_account()})
    public_igo.setIgoToken(igo_token.address)
    print(f"Contract deployed to {igo_token.address}")
    return igo_token, public_igo, payment_coin

