// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";


contract IgoToken is ERC20 {

    address public owner;
    address public publicIgoContract;
    uint256 public MAXAMOUNT;
    event IgoTokenMinted(uint256 _amount, address indexed _to);


    constructor(string memory _name, string memory _symbol, address _publicIgoContract, uint256 _maxAmount) ERC20(_name, _symbol) {
        owner = msg.sender;
        publicIgoContract = _publicIgoContract;
        MAXAMOUNT = _maxAmount;
    }

    modifier ownerOnly {
        require(msg.sender == owner, "owner only");
        _;
    }

    modifier canMint {
        require((msg.sender == owner || msg.sender == publicIgoContract), "no mint privileges");
        _;
    }

    function mint(address _to, uint256 _amount) external canMint returns(bool){
        require(totalSupply() + _amount <= MAXAMOUNT, "Not enough tokens left to mint");
        _mint(_to, _amount);
        emit IgoTokenMinted(_amount, _to);
        return true;
    }

    function transferOwnership(address _to) external ownerOnly returns(bool){
        owner = _to;
        return true;
    }

}
