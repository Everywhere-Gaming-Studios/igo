from scripts.utils import get_account
from brownie import accounts

price_numerator = 3
price_denominator = 10


payment_coin_name = "Test DAI"
payment_coin_symbol = "TDAI"

account = get_account()
investor = accounts[0]

investor_kyc = {'email': "renatomrocha93@gmail.com", 'country': 'Portugal'}

#Modifier messages
token_not_set_message = "Igo token not set"