pragma solidity ^0.4.0;

contract OracleMock {


    function latestRoundData () public view returns (uint80, int, uint,uint,uint80) {
        uint80 roundID;
        int price = 390865276;
        uint startedAt;
        uint timeStamp;
        uint80 answeredInRound;
        return (roundID, price, startedAt,  timeStamp, answeredInRound);
    }


}
