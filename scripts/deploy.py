from brownie import IgoToken, accounts, network, config
from scripts.utils import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from web3 import Web3



def deploy_igo_token_factory():
    account = get_account()

    igo_token_factory = IgoToken.deploy(config['igo_token_params']['name'],config['igo_token_params']['symbol'], {"from": account}, publish_source=config["networks"][network.show_active()]["verify"])
    print(f"Contract deployed to {igo_token_factory.address}")
    return igo_token_factory


def main():
    igo_token_factory = deploy_igo_token_factory()