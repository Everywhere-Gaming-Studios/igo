import brownie
from brownie import accounts, IgoToken, PublicIgo, PaymentCoin, config
import pytest
from utils import price_numerator, price_denominator,  payment_coin_symbol, payment_coin_name, account, investor, investor_kyc


@pytest.fixture
def payment_coin():
    return PaymentCoin.deploy(payment_coin_name, payment_coin_symbol, {"from": account})

@pytest.fixture
def public_igo(payment_coin):
    return PublicIgo.deploy(price_numerator, price_denominator, payment_coin.address, config['igo_token_params']['max_presale_mint'], {"from": account})

@pytest.fixture
def igo_token(public_igo):
    return IgoToken.deploy(config['igo_token_params']['name'], config['igo_token_params']['symbol'], public_igo.address, config['igo_token_params']['max_amount'],{"from": account})


def test_deployment(igo_token):
    assert (igo_token.name() == config['igo_token_params']['name'])
    assert (igo_token.symbol() == config['igo_token_params']['symbol'])


def test_setters(igo_token):

    mint_value = 1000

    igo_token.mint(account, mint_value, {"from": account})

    assert (igo_token.balanceOf(account) == mint_value)


def test_ownership_change(igo_token):

    second_owner = accounts[0]

    igo_token.transferOwnership(second_owner, {"from": account})

    mint_value = 1000

    # Confirm deployer no longer able to mint

    with brownie.reverts("no mint privileges"):
        igo_token.mint(account, mint_value, {"from": account})

    # Confirm second owner is able to mint

    igo_token.mint(account, mint_value, {"from": second_owner})

    assert (igo_token.balanceOf(account) == mint_value)


def test_wallet_transfer(igo_token):

    mint_value = 10

    igo_token.mint(account, mint_value, {"from": account})


def test_surpass_max_amount(igo_token):

    mint_value = 10 * 10 ** 6 * 10 ** 18;

    igo_token.mint(account, mint_value, {"from": account})

    with brownie.reverts("Not enough tokens left to mint"):
        second_mint_value = 3 * 10 ** 6 * 10 ** 18
        igo_token.mint(account, second_mint_value, {"from": account})
