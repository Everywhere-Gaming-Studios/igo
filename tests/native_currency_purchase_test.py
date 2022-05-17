import brownie
from brownie import accounts, PublicIgo, IgoToken, PaymentCoin, config, Wei, network
from scripts.utils import get_account
import math
import pytest
from tests_config import price_numerator, price_denominator, \
    payment_coin_symbol, payment_coin_name, \
    investor_kyc, investor, account, AVAX_UNIT, public_igo, igo_token, payment_coin, \
    NO_MINT_PRIVILEGES_MESSAGE, NO_NATIVE_CURRENCY_FUNDS, network_is_not_development, ONLY_OWNER_MESSAGE, LOCAL_BLOCKCHAIN_ENVIRONMENTS

paid_amount_in_native_currency = Wei('0.002 ether')


def test_igo_token_purchase_with_native_currency(public_igo, igo_token, account, investor):
    public_igo.setIgoTokenAddress(igo_token.address, {"from": account})

    public_igo.performKyc(investor_kyc['email'], investor_kyc['country'], {"from": investor})

    avax_price = public_igo.getLatestPrice() / 10 ** 8

    tx = public_igo.buyTokensWithNativeCurrency({"from": investor, "amount": paid_amount_in_native_currency})

    tokens_purchased = tx.events['TokenPurchase'][-1]['amountMinted']

    ground_truth_price = paid_amount_in_native_currency * avax_price * price_denominator / price_numerator

    precision_error = abs(ground_truth_price - tokens_purchased)

    print(
        f"User bought {tokens_purchased / 10 ** 18} IGO tokens for {paid_amount_in_native_currency / 10 ** 18} AVAX at a "
        f"price of {avax_price} AVAX/USD for a total of {paid_amount_in_native_currency / 10 ** 18 * avax_price}$")

    print(f"Error is: {precision_error}")

    assert (precision_error < 100)


def test_withdraw_funds(public_igo, igo_token, account, investor):
    public_igo.setIgoTokenAddress(igo_token.address, {"from": account})

    public_igo.performKyc(investor_kyc['email'], investor_kyc['country'], {"from": investor})

    initial_balance = account.balance()

    public_igo.buyTokensWithNativeCurrency({"from": investor, "amount": paid_amount_in_native_currency})

    public_igo.withdrawNativeCurrencyFunds({"from": account})

    final_balance = initial_balance + paid_amount_in_native_currency
    if network_is_not_development():
        assert (account.balance() > initial_balance)
    else:
        assert (account.balance() == final_balance)

def test_get_avax_price(public_igo):
    tx = public_igo.getLatestPrice()
    print(tx)


# Test onlyowner on withdraw
@pytest.mark.skipif(network_is_not_development(), reason="Network is not development")
def test_only_owner_withdraw(public_igo, igo_token, account, investor):
    public_igo.setIgoTokenAddress(igo_token.address, {"from": account})

    public_igo.performKyc(investor_kyc['email'], investor_kyc['country'], {"from": investor})

    public_igo.buyTokensWithNativeCurrency({"from": investor, "amount": paid_amount_in_native_currency})
    with brownie.reverts(ONLY_OWNER_MESSAGE):
        public_igo.withdrawNativeCurrencyFunds({"from": investor})


# Test no funds
@pytest.mark.skipif(network_is_not_development(), reason="Network is not development")
def test_withdraw_without_funds(public_igo, igo_token, account, investor):
    public_igo.setIgoTokenAddress(igo_token.address, {"from": account})

    public_igo.performKyc(investor_kyc['email'], investor_kyc['country'], {"from": investor})

    with brownie.reverts(NO_NATIVE_CURRENCY_FUNDS):
        public_igo.withdrawNativeCurrencyFunds({"from": account})


@pytest.mark.skipif(network_is_not_development(), reason="Network is not development")
def test_max_amount_minted(public_igo, igo_token, account, investor):

    igo_token.mint(investor.address, 125*10**5*10**18 ,{"from": account})

    public_igo.setIgoTokenAddress(igo_token.address, {"from": account})

    public_igo.performKyc(investor_kyc['email'], investor_kyc['country'], {"from": investor})

    with brownie.reverts('Not enough tokens left to mint'):
        public_igo.buyTokensWithNativeCurrency({"from": investor, "amount": paid_amount_in_native_currency})


