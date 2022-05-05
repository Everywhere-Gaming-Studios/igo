pragma solidity ^0.8.0;

import "@openzeppelin/contracts/utils/math/SafeMath.sol";
import "./interfaces/IERC20.sol";




contract PublicIgo {

    struct PublicInvestor {
        string email;
        string country;
    }

    address public owner; // Owner of the contract -> should be the multisig wallet as well
    address public coin; // Currency used to pay for IGO Tokens
    address public igoToken;
    uint8 private priceNumerator; // Price numerator used to compute ratio between payment currency and igo token price
    uint8 private priceDenominator; // Price denoinator used to compute ratio between payment currency and igo token price
    mapping(address => PublicInvestor) private _kyc; // Map to store KYC information
    mapping(address => bool) private _kycPerformed; // Map for addresses with performed KYC
    string[] whitelistedCountries; // List of whitelisted countries
    uint256 mintedByPublicIgo = 0;
    uint256 MAXAMOUNT = 25 * 10**5 * 10**18; // Maximum amount of mintable tokens on pre sale 2.5 Millions

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
        require(igoToken != address(0), "Igo token not set");
        _;
    }

    constructor(uint8 _priceNumerator, uint8 _priceDenominator, address _paymentCoin) {
        owner = msg.sender;
        priceNumerator = _priceNumerator;
        priceDenominator = _priceDenominator;
        coin = _paymentCoin;
    }

    function setCoin (address _coin) external ownerOnly {
        coin = _coin;
    }

    function setIgoToken (address _igoToken) external ownerOnly {
        igoToken = _igoToken;
    }

    function transferOwnership(address _to) external ownerOnly returns(bool) {
        owner = _to;
        return true;
    }

    function performKyc(string memory _email, string memory _country) external {
        require(!_kycPerformed[msg.sender], "User already performed KYC");
        _kyc[msg.sender] = PublicInvestor({email: _email, country: _country});
        _kycPerformed[msg.sender] = true;
        emit KycPerformed(msg.sender, _email);
    }

    function buyTokens(uint256 _paidAmount) external hasKyc igoTokenSet {
        uint256 boughtAmount = _computeTokenAmount(_paidAmount);
        uint256 allowance = IERC20(coin).allowance(msg.sender, address(this));
        require(allowance >= _paidAmount, "Check the token allowance");
        uint256 _amountToMint = _computeTokenAmount(_paidAmount);
        require(mintedByPublicIgo + _amountToMint <= MAXAMOUNT, "Not enough tokens left to mint");
        IERC20(coin).transferFrom(msg.sender, address(this), _paidAmount);
        _mintTokenToUser(msg.sender, _amountToMint);
    }

    function _mintTokenToUser(address _to, uint256 _amount) private {
        IERC20(igoToken).mint(_to, _amount);
        mintedByPublicIgo += _amount;
    }


    function _computeTokenAmount(uint256 paidAmount) private returns (uint256) {
        uint256 tokenAmount =  SafeMath.div(paidAmount * priceDenominator,priceNumerator, "Unable to divide integers");
        return tokenAmount;
    }

}
