import brownie
from brownie import accounts, PublicIgo, IgoToken, PaymentCoin, config, network
from scripts.utils import get_account
import math
import pytest
from tests_config import price_numerator, price_denominator, \
    payment_coin_symbol, payment_coin_name, account, \
    investor, investor_kyc, TOKEN_NOT_SET_MESSAGE, public_igo, payment_coin, igo_token, CHECK_ALLOWANCE_MESSAGE, \
    KYC_NECESSARY_MESSAGE, USER_ALREADY_HAS_KYC_MESSAGE, NOT_ENOUGH_TOKENS_TO_MINT_MESSAGE, network_is_not_development, LOCAL_BLOCKCHAIN_ENVIRONMENTS


@pytest.mark.skipif(network_is_not_development(), reason="Network is not development")
def test_investment_with_no_token_set(public_igo, payment_coin, investor, account):
    paid_amount = 10

    public_igo.performKyc(investor_kyc['email'], investor_kyc['country'], {"from": investor})

    # Mint some test dai to the user
    payment_coin.mint(investor, paid_amount, {"from": account})

    # Allow public igo contract to transfer those coins to itself
    payment_coin.approve(public_igo.address, paid_amount, {"from": investor})

    with brownie.reverts(TOKEN_NOT_SET_MESSAGE):
        public_igo.buyTokens(paid_amount, {"from": investor})


def test_investment_after_kyc(public_igo, igo_token, payment_coin, investor, account):
    paid_amount = 10

    public_igo.setIgoTokenAddress(igo_token.address, {"from": account})

    public_igo.performKyc(investor_kyc['email'], investor_kyc['country'], {"from": investor})

    # Mint some test dai to the user
    payment_coin.mint(investor, paid_amount, {"from": account})

    initial_coin_balance = payment_coin.balanceOf(investor.address, {"from": investor})

    # Allow public igo contract to transfer those coins to itself
    payment_coin.approve(public_igo.address, paid_amount, {"from": investor})

    public_igo.buyTokens(paid_amount, {"from": investor})

    target_amount = math.trunc(paid_amount * 10 ** 12 * price_denominator / price_numerator)

    assert (target_amount == igo_token.balanceOf(investor))
    assert (payment_coin.balanceOf(investor.address, {"from": investor}) == initial_coin_balance - paid_amount)


@pytest.mark.skipif(network_is_not_development(), reason="Network is not development")
def test_investment_without_allowance(public_igo, igo_token, payment_coin, investor, account):
    paid_amount = 10

    public_igo.setIgoTokenAddress(igo_token.address, {"from": account})

    public_igo.performKyc(investor_kyc['email'], investor_kyc['country'], {"from": investor})

    # Mint some test dai to the user
    payment_coin.mint(investor, paid_amount, {"from": account})

    with brownie.reverts(CHECK_ALLOWANCE_MESSAGE):
        public_igo.buyTokens(paid_amount, {"from": investor})

@pytest.mark.skipif(network_is_not_development(), reason="Network is not development")
def test_investment_without_kyc(public_igo, investor):
    paid_amount = 10

    with brownie.reverts(KYC_NECESSARY_MESSAGE):
        public_igo.buyTokens(paid_amount, {"from": investor})


@pytest.mark.skipif(network_is_not_development(), reason="Network is not development")
def test_duplicated_kyc(public_igo, investor, account):
    public_igo.performKyc(investor_kyc['email'], investor_kyc['country'], {"from": investor})

    with brownie.reverts(USER_ALREADY_HAS_KYC_MESSAGE):
        public_igo.performKyc(investor_kyc['email'], investor_kyc['country'], {"from": investor})


def test_mint_max_amount(payment_coin, investor, account):
    paid_amount = config['igo_token_params']['max_presale_mint_in_usdc']

    public_igo = PublicIgo.deploy(1, 1, payment_coin.address, config['igo_token_params']['max_presale_mint'],
                                  config['chainlink_oracle']['avax_testnet_price_feed_address'],
                                  {"from": account})

    igo_token = IgoToken.deploy(config['igo_token_params']['name'], config['igo_token_params']['symbol'], public_igo,
                                config['igo_token_params']['max_amount'],
                                {"from": account})

    public_igo.setIgoTokenAddress(igo_token.address, {"from": account})

    public_igo.performKyc(investor_kyc['email'], investor_kyc['country'], {"from": investor})

    # Mint some test dai to the user
    payment_coin.mint(investor, paid_amount, {"from": account})

    initial_coin_balance = payment_coin.balanceOf(investor.address, {"from": investor})

    # Allow public igo contract to transfer those coins to itself
    payment_coin.approve(public_igo.address, paid_amount, {"from": investor})

    print(f"Will buy with {paid_amount/ 10 ** 6}")

    public_igo.buyTokens(paid_amount, {"from": investor})

    target_amount = paid_amount * 10 **12

    assert (target_amount == igo_token.balanceOf(investor))
    assert (payment_coin.balanceOf(investor.address, {"from": investor}) == initial_coin_balance - paid_amount)


@pytest.mark.skipif(network_is_not_development(), reason="Network is not development")
def test_surpassing_max_amount(payment_coin, investor, account):
    paid_amount = config['igo_token_params']['max_presale_mint_in_usdc']

    public_igo = PublicIgo.deploy(1, 1, payment_coin.address, config['igo_token_params']['max_presale_mint'],
                                  config['chainlink_oracle']['avax_testnet_price_feed_address'],
                                  {"from": account})

    igo_token = IgoToken.deploy(config['igo_token_params']['name'], config['igo_token_params']['symbol'], public_igo,
                                config['igo_token_params']['max_amount'],
                                {"from": account})

    public_igo.setIgoTokenAddress(igo_token.address, {"from": account})

    public_igo.performKyc(investor_kyc['email'], investor_kyc['country'], {"from": investor})

    # Mint some test dai to the user
    payment_coin.mint(investor, paid_amount + 100, {"from": account})

    initial_coin_balance = payment_coin.balanceOf(investor.address, {"from": investor})

    # Allow public igo contract to transfer those coins to itself
    payment_coin.approve(public_igo.address, paid_amount + 100, {"from": investor})

    public_igo.buyTokens(paid_amount, {"from": investor})

    with brownie.reverts(NOT_ENOUGH_TOKENS_TO_MINT_MESSAGE):
        public_igo.buyTokens(1, {"from": investor})


def test_token_price_change(igo_token, public_igo, payment_coin, investor, account):
    paid_amount = 10 * 10 **6

    public_igo.setIgoTokenAddress(igo_token.address, {"from": account})

    public_igo.performKyc(investor_kyc['email'], investor_kyc['country'], {"from": investor})

    # Mint some test dai to the user
    payment_coin.mint(investor, paid_amount * 2, {"from": account})

    initial_coin_balance = payment_coin.balanceOf(investor.address, {"from": investor})

    assert (initial_coin_balance == paid_amount * 2)

    # Allow public igo contract to transfer those coins to itself
    payment_coin.approve(public_igo.address, paid_amount * 2, {"from": investor})

    public_igo.buyTokens(paid_amount, {"from": investor})

    target_amount = math.trunc(paid_amount *10**12 * price_denominator / price_numerator)

    updated_numerator = 5

    public_igo.updateTokenPrice(updated_numerator, price_denominator, {"from": account})

    paid_amount_2 = 10 * 10 ** 6

    public_igo.buyTokens(paid_amount_2, {"from": investor})

    target_amount_2 = math.trunc(paid_amount_2 *10**12 * price_denominator / updated_numerator)

    precision_error = abs(target_amount + target_amount_2 - igo_token.balanceOf(investor))

    print(f"Precision error: {precision_error}")

    assert (precision_error < 2000)

    assert (payment_coin.balanceOf(investor.address) == initial_coin_balance - paid_amount - paid_amount_2)



def test_coin_withdraw(igo_token, public_igo, payment_coin, investor, account):

    paid_amount = 10* 10**6


    public_igo.setIgoTokenAddress(igo_token.address, {"from": account})

    public_igo.performKyc(investor_kyc['email'], investor_kyc['country'], {"from": investor})

    # Mint some test dai to the user
    payment_coin.mint(investor, paid_amount * 2, {"from": account})

    initial_coin_balance = payment_coin.balanceOf(investor.address, {"from": investor})

    # Allow public igo contract to transfer those coins to itself
    payment_coin.approve(public_igo.address, paid_amount * 2, {"from": investor})

    public_igo.buyTokens(paid_amount, {"from": investor})

    assert(payment_coin.balanceOf(account.address) == 0)

    public_igo.withdrawCoin({"from": account})

    assert(payment_coin.balanceOf(account.address) == paid_amount)



@pytest.mark.skipif(network_is_not_development(), reason="Network is not development")
def test_withdraw_without_permission(igo_token, public_igo, payment_coin, investor, account): 
    
    paid_amount = 10* 10**18

    public_igo.setIgoTokenAddress(igo_token.address, {"from": account})

    public_igo.performKyc(investor_kyc['email'], investor_kyc['country'], {"from": investor})

    # Mint some test dai to the user
    payment_coin.mint(investor, paid_amount * 2, {"from": account})

    initial_coin_balance = payment_coin.balanceOf(investor.address, {"from": investor})

    with brownie.reverts('Only the owner is allowed to perform this operation'):
        public_igo.withdrawCoin({"from": investor})
