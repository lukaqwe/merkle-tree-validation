// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract Withdraw {
    
    mapping(address => bool) public userWithdrawn;
    bytes32 public merkleRoot;

    constructor(bytes32 root) payable{ 
        merkleRoot = root;
    }

    function computeSha(bytes32 left, bytes32 right ) internal pure returns(bytes32){
        bytes32 digest;
        
        if(left < right)
            digest = keccak256(abi.encodePacked(left, right));
        else
            digest = keccak256(abi.encodePacked(right, left));
        
        return digest;
    }

    function withdraw(bytes32[] calldata proof, address payable receiver, uint256 amount) public { // amount is the sum in wei to be paid
        // verify if already withdrawn
        require(userWithdrawn[receiver] == false, "User already has withdrawn");
        
        // verify root
        bytes32 digest = keccak256(abi.encodePacked(receiver, amount));
        for(uint i = 0; i < proof.length; i++){
            digest = computeSha(digest, proof[i]);
        }
        require(digest == merkleRoot);

        // send
        bool sent = receiver.send(amount);
        require(sent, "Failed to send Ether");

        // set withrawn to true
        userWithdrawn[receiver] = true;
    }

    receive() external payable{ // receive ether if no balance to make withdrawals

    }
}
