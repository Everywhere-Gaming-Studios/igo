import brownie
from brownie import accounts, IgoToken, PublicIgo, PaymentCoin, config, network
import pytest

from tests_config import price_numerator, price_denominator, \
    payment_coin_symbol, payment_coin_name, account, \
    investor, investor_kyc, igo_token, public_igo, payment_coin, NO_MINT_PRIVILEGES_MESSAGE, \
    NOT_ENOUGH_TOKENS_TO_MINT_MESSAGE, \
    network_is_not_development, LOCAL_BLOCKCHAIN_ENVIRONMENTS


def test_deployment(igo_token):
    assert (igo_token.name() == config['igo_token_params']['name'])
    assert (igo_token.symbol() == config['igo_token_params']['symbol'])


def test_setters(igo_token, account):
    mint_value = 1000

    igo_token.mint(account, mint_value, {"from": account})

    assert (igo_token.balanceOf(account) == mint_value)


@pytest.mark.skipif(network_is_not_development(), reason="Network is not development")
def test_ownership_change(igo_token, account, investor):
    igo_token.transferOwnership(investor, {"from": account})

    mint_value = 1000

    # Confirm deployer no longer able to mint

    with brownie.reverts(NO_MINT_PRIVILEGES_MESSAGE):
        igo_token.mint(account, mint_value, {"from": account, "gasLimit": 207404400})

    # Confirm second owner is able to mint

    igo_token.mint(account, mint_value, {"from": investor})

    assert (igo_token.balanceOf(account) == mint_value)


def test_wallet_transfer(igo_token, account):
    mint_value = 10

    igo_token.mint(account, mint_value, {"from": account})


@pytest.mark.skipif(network_is_not_development(), reason="Network is not development")
def test_surpass_max_amount(igo_token, account):
    mint_value = 10 * 10 ** 6 * 10 ** 18

    igo_token.mint(account, mint_value, {"from": account})

    with brownie.reverts(NOT_ENOUGH_TOKENS_TO_MINT_MESSAGE):
        second_mint_value = 3 * 10 ** 6 * 10 ** 18
        igo_token.mint(account, second_mint_value, {"from": account})
