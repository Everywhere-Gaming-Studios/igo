import brownie
from brownie import accounts, PublicIgo, IgoToken, PaymentCoin, config, Wei, network
from scripts.utils import get_account
import math
import pytest
from tests_config import price_numerator, price_denominator, \
    payment_coin_symbol, payment_coin_name, \
    investor_kyc, investor, account, AVAX_UNIT, public_igo, igo_token, payment_coin

paid_amount_in_native_currency = Wei('0.002 ether')


def test_igo_token_purchase_with_native_currency(public_igo, igo_token, account, investor):
    print(f"Paid amount in crypto is {paid_amount_in_native_currency}")

    public_igo.setIgoTokenAddress(igo_token.address, {"from": account})

    public_igo.performKyc(investor_kyc['email'], investor_kyc['country'], {"from": investor})

    initial_coin_balance = investor.balance()

    print(f"Investor starts with {initial_coin_balance} AVAX")

    tx = public_igo.buyTokensWithNativeCurrency({"from": investor, "amount": paid_amount_in_native_currency})

    print(f"Finished purchase and now have {igo_token.balanceOf(investor.address, {'from': investor})} IGO Tokens")
    # Check for AVAX final balance
    assert (investor.balance() == initial_coin_balance - paid_amount_in_native_currency)


def test_withdraw_funds(public_igo, igo_token, account, investor):
    public_igo.setIgoTokenAddress(igo_token.address, {"from": account})

    public_igo.performKyc(investor_kyc['email'], investor_kyc['country'], {"from": investor})

    initial_balance = account.balance()

    tx = public_igo.buyTokensWithNativeCurrency({"from": investor, "amount": paid_amount_in_native_currency})

    withdraw_tx = public_igo.withdrawNativeCurrencyFunds({"from": account})

    final_balance = initial_balance + paid_amount_in_native_currency

    print(f"Final balance should be {final_balance} and is {account.balance()}")

    print(f"Difference is {final_balance - account.balance()} (final_balance - account.balance())")

    print(f"Gas paid is {tx.gas_used}")

    assert (account.balance() == final_balance)


def test_get_avax_price(public_igo):
    if network.show_active() == 'development':
        print("Unable to run test...")
        return
    print("Will try to get price from oracle")
    print(f"Using price feed at address {public_igo.priceFeed()}")
    tx = public_igo.getLatestPrice()
    print(tx)

# Test onlyowner on withdraw

# Test no funds

# Test max amount minted
