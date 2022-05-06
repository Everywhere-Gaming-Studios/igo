from brownie import FlattenedIgoToken, PublicIgo, IgoToken, PaymentCoin, accounts, network, config
from scripts.utils import get_account, deploy_igo_token_factory, investor_kyc
import os


DEPLOY_ENV = os.getenv('DEPLOY_ENV')


def testnet_deploy():
    igo_token, public_igo, payment_coin = deploy_igo_token_factory()
    account = get_account()

    # Mint some TDAI to myself
    payment_coin.mint(account, 100 * 10 ** 18, {"from": account})

    # Allow public igo to spend those DAI
    payment_coin.approve(public_igo, 100 * 10 ** 18, {"from": account})

    # Perform KYC
    public_igo.performKyc(investor_kyc['email'], investor_kyc['country'])

    # Buy tokens from igo
    public_igo.buyTokens(100 * 10 ** 18, {"from": account})

    # Change ownership to multisig
    igo_token.transferOwnership(config['igo_token_params']['multisig_test_address'], {"from": account})
    public_igo.transferOwnership(config['igo_token_params']['multisig_test_address'], {"from": account})


def mainnet_deploy():
    account = get_account()

    '''Uncomment when ready for mainnet deployment'''

    print("Not yet ready for mainnet deployment...")

    # public_igo = PublicIgo.deploy(config['igo_token_params']['price_numerator'], config['igo_token_params']['price_denominator'], config['payment_coin_params']['address'],
    #                               config['igo_token_params']['max_presale_mint'], {"from": account})
    #
    # igo_token = IgoToken.deploy(config['igo_token_params']['name'], config['igo_token_params']['symbol'],
    #                             public_igo.address, config['igo_token_params']['max_amount'], {"from": account()})
    #
    # public_igo.setIgoToken(igo_token.address)
    # # Change ownership to multisig
    # igo_token.transferOwnership(config['igo_token_params']['multisig_test_address'], {"from": account})
    # public_igo.transferOwnership(config['igo_token_params']['multisig_mainnet_address'], {"from": account})


def main():

    print(f"Deploying with environment {DEPLOY_ENV}")
    if DEPLOY_ENV == 'MAINNET':
        mainnet_deploy()
    elif DEPLOY_ENV == 'TESTNET':
        testnet_deploy()
    else:
        print("Please select a valid deployment environment \n MAINNET for mainnet deployment \n TESTNET for testnet deployment")






