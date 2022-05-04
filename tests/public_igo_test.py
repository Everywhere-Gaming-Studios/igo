import brownie
from brownie import accounts, PublicIgo, IgoToken, PaymentCoin, config
from scripts.utils import get_account
import math
import pytest
from utils import price_numerator, price_denominator, \
    payment_coin_symbol, payment_coin_name, account,\
    investor, investor_kyc, token_not_set_message


@pytest.fixture
def payment_coin():
    return PaymentCoin.deploy(payment_coin_name, payment_coin_symbol, {"from": account})


@pytest.fixture
def public_igo(payment_coin):
    return PublicIgo.deploy(price_numerator, price_denominator, payment_coin.address, {"from": account})


@pytest.fixture
def igo_token(public_igo):
    return IgoToken.deploy(config['igo_token_params']['name'], config['igo_token_params']['symbol'], public_igo, {"from": account})


def test_investment_with_no_token_set(public_igo, payment_coin):
    paid_amount = 10

    public_igo.performKyc(investor_kyc['email'], investor_kyc['country'], {"from": investor})

    # Mint some test dai to the user
    payment_coin.mint(investor, paid_amount, {"from": account})

    print(f"User now has {payment_coin.balanceOf(investor.address)} TDAI")

    # Allow public igo contract to transfer those coins to itself
    payment_coin.approve(public_igo.address, paid_amount)

    with brownie.reverts(token_not_set_message):
        public_igo.buyTokens(paid_amount, {"from": investor})



def test_investment_after_kyc(public_igo, igo_token, payment_coin):

    paid_amount = 10

    public_igo.setIgoToken(igo_token.address, {"from": account})

    public_igo.performKyc(investor_kyc['email'], investor_kyc['country'], {"from": investor})


    # Mint some test dai to the user
    payment_coin.mint(investor, paid_amount, {"from": account})

    initial_coin_balance = payment_coin.balanceOf(investor.address, {"from": investor})

    print(f"User now has {payment_coin.balanceOf(investor.address)} TDAI")

    # Allow public igo contract to transfer those coins to itself
    payment_coin.approve(public_igo.address, paid_amount)


    public_igo.buyTokens(paid_amount, {"from": investor})

    target_amount = math.trunc(paid_amount * price_denominator / price_numerator)

    assert(target_amount == igo_token.balanceOf(investor))
    assert(payment_coin.balanceOf(investor.address, {"from": investor}) == initial_coin_balance - paid_amount)


def test_investment_without_kyc(public_igo):

    paid_amount = 10

    with brownie.reverts("KYC necessary to invest"):
        public_igo.buyTokens(paid_amount, {"from": investor})


def test_duplicated_kyc(public_igo):

    public_igo.performKyc(investor_kyc['email'], investor_kyc['country'], {"from": investor})

    with brownie.reverts("User already performed KYC"):
        public_igo.performKyc(investor_kyc['email'], investor_kyc['country'], {"from": investor})



