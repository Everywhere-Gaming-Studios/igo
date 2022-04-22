// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";


contract IgoToken is ERC20 {

    address public owner;

    constructor(string memory _name, string memory _symbol) ERC20(_name, _symbol) {
        owner = msg.sender;
    }

    modifier ownerOnly {
        require(msg.sender == owner, "owner only");
        _;
    }

    function mint(address to, uint256 amount) external ownerOnly returns(bool){
        _mint(to, amount);
        return true;
    }

}
