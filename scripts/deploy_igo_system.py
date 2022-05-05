from brownie import FlattenedIgoToken, PublicIgo, IgoToken, PaymentCoin, accounts, network, config
from scripts.utils import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS, payment_coin_symbol, payment_coin_name, investor_kyc
from web3 import Web3

account = get_account()


def deploy_payment_coin():
    return PaymentCoin.deploy(payment_coin_name, payment_coin_symbol, {"from": account})


def deploy_public_igo():
    active_network = network.show_active()
    payment_coin = deploy_payment_coin()
    print(f"Deploying on network: {active_network}")
    public_igo = PublicIgo.deploy(config['igo_token_params']['price_numerator'], config['igo_token_params']['price_denominator'], payment_coin.address, {"from": account})
    return public_igo, payment_coin


def deploy_igo_token_factory():
    public_igo, payment_coin = deploy_public_igo()
    igo_token = IgoToken.deploy(config['igo_token_params']['name'], config['igo_token_params']['symbol'], public_igo.address , {"from": account})
    public_igo.setIgoToken(igo_token.address)
    print(f"Contract deployed to {igo_token.address}")
    return igo_token, public_igo, payment_coin


def main():
    igo_token, public_igo, payment_coin = deploy_igo_token_factory()
    account = get_account()

    # Mint some TDAI to myself
    payment_coin.mint(account, 10 * 10**18, {"from": account})

    # Allow public igo to spend those DAI
    payment_coin.approve(public_igo, 10 * 10**18, {"from": account})

    # Perform KYC
    public_igo.performKyc(investor_kyc['email'], investor_kyc['country'])

    # Buy tokens from igo
    public_igo.buyTokens(10 * 10 ** 18, {"from": account})

    # Change ownership to multisig
    igo_token.transferOwnership(config['igo_token_params']['multisig_test_address'], {"from": account})
    public_igo.transferOwnership(config['igo_token_params']['multisig_test_address'], {"from": account})





