// import Web3 from 'web3';
const web3 = require('web3');

const Withdraw = artifacts.require("Withdraw");
const merkleTree = require('../src/merkle_tree.json');
const balances = require('../src/balances.json');



function getTotalBalance(){
  let balance = 0;
  for(const key in balances ){
    balance += balances[key];
  }
  return balance;
}


var balanceInWei = getTotalBalance();

module.exports = function(deployer) {
  deployer.deploy(Withdraw, merkleTree[0][0], {value : balanceInWei});

  // const instance = Withdraw.deployed();
  

};
