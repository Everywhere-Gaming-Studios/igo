// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";


contract IgoToken is ERC20 {

    address public owner;
    address public publicIgoContract;

    constructor(string memory _name, string memory _symbol, address _publicIgoContract) ERC20(_name, _symbol) {
        owner = msg.sender;
        publicIgoContract = _publicIgoContract;
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
        _mint(_to, _amount);
        return true;
    }

    function transferOwnership(address _to) external ownerOnly returns(bool){
        owner = _to;
        return true;
    }

}
