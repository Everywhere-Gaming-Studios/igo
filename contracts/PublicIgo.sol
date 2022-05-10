pragma solidity ^0.8.0;

import "@openzeppelin/contracts/utils/math/SafeMath.sol";
import "./interfaces/IERC20.sol";
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";



////////////////////////////////// TODO add mint / investment events!

contract PublicIgo {

    struct PublicInvestor {
        string email;
        string country;
    }

    address public owner; // Owner of the contract -> should be the multisig wallet as well
    address public paymentCoinAddress; // Currency used to pay for IGO Tokens
    address public igoTokenAddress;
    uint8 public priceNumerator; // Price numerator used to compute ratio between payment currency and igo token price
    uint8 public priceDenominator; // Price denoinator used to compute ratio between payment currency and igo token price
    mapping(address => PublicInvestor) private _kyc; // Map to store KYC information
    mapping(address => bool) private _kycPerformed; // Map for addresses with performed KYC
    string[] whitelistedCountries; // List of whitelisted countries
    uint256 mintedByPublicIgo = 0;
    uint256 MAXAMOUNT; // Maximum amount of mintable tokens on pre sale 2.5 Millions
    IERC20 internal paymentCoin;
    IERC20 internal igoToken;
    AggregatorV3Interface public priceFeed;

    uint public lastWithdrawValue;

    event KycPerformed(address investorAddress, string email);

    modifier hasKyc {
        require(_kycPerformed[msg.sender], "KYC necessary to invest");
        _;
    }

    modifier ownerOnly {
      require(msg.sender == owner);
      _;
    }

    modifier igoTokenSet {
        require(igoTokenAddress != address(0), "Igo token not set");
        _;
    }

    constructor(uint8 _priceNumerator, uint8 _priceDenominator, address _paymentCoinAddress, uint256 _maxAmount, address AggregatorAddress) {
        owner = msg.sender;
        priceNumerator = _priceNumerator;
        priceDenominator = _priceDenominator;
        paymentCoinAddress = _paymentCoinAddress;
        paymentCoin = IERC20(paymentCoinAddress);
        MAXAMOUNT = _maxAmount;
        priceFeed = AggregatorV3Interface(AggregatorAddress);
    }

    function updateTokenPrice(uint8 _priceNumerator, uint8 _priceDenominator) external ownerOnly returns(bool){
        priceNumerator = _priceNumerator;
        priceDenominator = _priceDenominator;
        return true;
    }

    function setCoinAddress (address _coinAddress) external ownerOnly {
        paymentCoinAddress = _coinAddress;
        paymentCoin = IERC20(paymentCoinAddress);
    }

    function setIgoTokenAddress (address _igoTokenAddress) external ownerOnly {
        igoTokenAddress = _igoTokenAddress;
        igoToken = IERC20(igoTokenAddress);
    }

    function transferOwnership(address _to) external ownerOnly returns(bool) {
        owner = _to;
        return true;
    }

    function performKyc(string calldata _email, string calldata _country) external {
        require(!_kycPerformed[msg.sender], "User already performed KYC");
        _kyc[msg.sender] = PublicInvestor({email: _email, country: _country});
        _kycPerformed[msg.sender] = true;
        emit KycPerformed(msg.sender, _email);
    }

    function buyTokens(uint256 _paidAmount) external hasKyc igoTokenSet {
        _checkAllowance(_paidAmount);
        uint256 _amountToMint = _computeTokenAmount(_paidAmount);
        require(mintedByPublicIgo + _amountToMint <= MAXAMOUNT, "Not enough tokens left to mint");
        paymentCoin.transferFrom(msg.sender, address(this), _paidAmount);
        _mintTokenToUser(msg.sender, _amountToMint);
    }

    function buyTokensWithNativeCurrency() external payable hasKyc {
        uint256 _nativeCurrencyAmount = msg.value;
        // check equivalence in payment_coin_units
        // Oracle price feed call for AVAX price
//        uint _avaxPrice = getLatestPrice();
        uint256 _paidAmountInPaymentCoin = 1 * _nativeCurrencyAmount; // Example with 1$ static price
        uint256 _amountToMint = _computeTokenAmount(_paidAmountInPaymentCoin);
        require(mintedByPublicIgo + _amountToMint <= MAXAMOUNT, "Not enough tokens left to mint");
        _mintTokenToUser(msg.sender, _amountToMint);
    }


    function _checkAllowance(uint256 _paidAmount) private view {
        uint256 allowance = IERC20(paymentCoinAddress).allowance(msg.sender, address(this));
        require(allowance >= _paidAmount, "Check the token allowance");
    }

    function _mintTokenToUser(address _to, uint256 _amount) private {
        igoToken.mint(_to, _amount);
        mintedByPublicIgo += _amount;
    }


    function _computeTokenAmount(uint256 paidAmount) private view returns (uint256) {
        uint256 tokenAmount =  SafeMath.div(paidAmount * priceDenominator,priceNumerator, "Unable to divide integers");
        return tokenAmount;
    }


     function withdrawNativeCurrencyFunds() external ownerOnly returns (uint256) {
        uint256 _funds = address(this).balance;
        require(_funds > 0, "Contract has no native currency funds");
        (bool sent, ) = msg.sender.call{value: _funds}("");
        require(sent, "Failed to send ether");
         lastWithdrawValue = _funds;
         return _funds;
    }

     function getLatestPrice() public view returns (uint) {
        (
            uint80 roundID,
            int price,
            uint startedAt,
            uint timeStamp,
            uint80 answeredInRound
        ) = priceFeed.latestRoundData();
        return uint(price);
    }

}
