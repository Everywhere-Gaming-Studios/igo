from brownie import FlattenedIgoToken, IgoToken, accounts, network, config
from scripts.utils import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from web3 import Web3



def deploy_igo_token_factory():
    account = get_account()

    igo_token = IgoToken.deploy(config['igo_token_params']['name'], config['igo_token_params']['symbol'], {"from": account})

    print(f"Contract deployed to {igo_token.address}")
    return igo_token


def main():
    igo_token = deploy_igo_token_factory()
    account = get_account()
    # Change ownership to multisig
    igo_token.transferOwnership(config['igo_token_params']['multisig_test_address'], {"from": account})

