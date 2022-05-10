from brownie import FlattenedIgoToken, PublicIgo, IgoToken, PaymentCoin, accounts, network, config
import pytest

price_numerator = 3
price_denominator = 10


payment_coin_name = "Test DAI"
payment_coin_symbol = "TDAI"


LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]

investor_kyc = {'email': "renatomrocha93@gmail.com", 'country': 'Portugal'}

#Modifier messages
TOKEN_NOT_SET_MESSAGE = "Igo token not set"
NO_MINT_PRIVILEGES_MESSAGE = "No mint privileges"
NOT_ENOUGH_TOKENS_TO_MINT_MESSAGE = "Not enough tokens left to mint"
CHECK_ALLOWANCE_MESSAGE = "Check the token allowance"
KYC_NECESSARY_MESSAGE = "KYC necessary to invest"
USER_ALREADY_HAS_KYC_MESSAGE = "User already performed KYC"

AVAX_UNIT = 10*10**18


@pytest.fixture
def account():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    else:
        return accounts.add(config["test_wallets"]["from_key"])

@pytest.fixture
def investor():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[1]
    else:
        return accounts.add(config["test_wallets"]["from_key_2"])

@pytest.fixture
def payment_coin(account):
    return PaymentCoin.deploy(payment_coin_name, payment_coin_symbol, {"from": account})


@pytest.fixture
def public_igo(payment_coin, account):
    return PublicIgo.deploy(price_numerator, price_denominator, payment_coin.address,
                            config['igo_token_params']['max_presale_mint'],
                            config['chainlink_oracle']['avax_testnet_price_feed_address'], {"from": account})


@pytest.fixture
def igo_token(public_igo, account):
    return IgoToken.deploy(config['igo_token_params']['name'], config['igo_token_params']['symbol'], public_igo,
                           config['igo_token_params']['max_amount'],
                           {"from": account})