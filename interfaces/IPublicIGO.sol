pragma solidity ^0.4.0;

contract IPublicIGO {

    /**
     * @dev Updates coin accepted for Public IGO payment.
     */
    function setCoin (address _coin) external;

    /**
     * @dev Updates address for Public IGO token
     */
    function setIgoToken (address _igoToken) external;

    /**
     * @dev Transfers ownership of the Public IGO contract
     * Returns true in case ownership transfer is successfull
     */
    function transferOwnership(address _to) external returns(bool);


    /**
     * @dev Allows EOA to perform KYC
     */
//    function performKyc(string memory _email, string memory _country) external;

    /**
     * @dev Allows EOA to invest into public IGO
     */
    function buyTokens(uint256 _paidAmount) external ;




}
