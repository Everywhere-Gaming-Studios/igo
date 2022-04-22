from brownie import accounts, IgoToken, config


def test_deployment():
    # Arrange
    deployer = accounts[0]

    # Create coin
    igoToken = IgoToken.deploy(config['igo_token_params']['name'],config['igo_token_params']['symbol'],{"from": deployer})

    assert (igoToken.name() == config['igo_token_params']['name'])
    assert (igoToken.symbol() == config['igo_token_params']['symbol'])

def test_setters():
    # Arrange
    deployer, random_user = accounts[0], accounts[1]

    igoToken = IgoToken.deploy(config['igo_token_params']['name'],config['igo_token_params']['symbol'],{"from": deployer})

    mint_value = 1000

    igoToken.mint(deployer, mint_value,{"from": deployer})

    assert (igoToken.balanceOf(deployer) == mint_value)