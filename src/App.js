
import './App.css';
import React, {useState} from 'react';
import Web3 from 'web3';
import styled from "styled-components";

const ButtonGroup = styled.div`
  display: flex;
`
var web3 = new Web3(Web3.givenProvider);
const balances = require("./balances.json");
const merkleTree = require("./merkle_tree.json");
const abi = require('./abi/Withdraw.json');
const contractAddress = '0x8C00391cDDcCcd229470Ce0AFD9735037f914379';
let instance = new web3.eth.Contract(abi, contractAddress);


let userAddress;
let balanceInWei;


// connect to wallet account
async function Connect(setAccount, setBalance) {
  if (window.ethereum) {
      try{
        window.ethereum.enable();
        web3 = new Web3(window.ethereum);

        let accounts = await web3.eth.getAccounts();
        console.log(accounts);
        userAddress = accounts[0];
        console.log(userAddress);
        setAccount(userAddress);
        balanceInWei = balances[userAddress];

        const userWithdrawn = await instance.methods.userWithdrawn(userAddress).call();
        if(balanceInWei === undefined || userWithdrawn)
          balanceInWei = 0;
        setBalance(web3.utils.fromWei(balanceInWei.toString(), "ether"));
    }catch(e){
      console.log(e);
    }
  }

}
  

function constructProof(address, value){
  let proof = [];
  let digest = web3.utils.soliditySha3({t: "address", v: address},{t:"uint256",v: value.toString()});
  
  let idx = merkleTree[merkleTree.length - 1].indexOf(digest);
  let lvl = merkleTree.length - 1;

  if(idx < 0){
    idx = merkleTree[merkleTree.length - 2].indexOf(digest);
    lvl = merkleTree.length - 2;
  }

  if(idx < 0)
    return proof;

  let neighbor_idx;
  
  while(lvl > 0){
    if(idx % 2 === 1)
      neighbor_idx = idx - 1; // neighbor is on the left
    else
      neighbor_idx = idx + 1; // neighbor is on the right

    
    proof.push(merkleTree[lvl][neighbor_idx]);
    idx = Math.floor(idx/2);
    lvl--;
  }
  
  return proof;
}

async function Withdraw(setBalance){

  let proof = constructProof(userAddress, balanceInWei);
  // console.log(proof);

  // let root = await instance.methods.merkleRoot().call();
  // console.log(root);
  

  try{
    let result = await instance.methods.withdraw(proof, userAddress, balanceInWei.toString()).send({from: userAddress});    
    console.log(result);
    setBalance(0);
  }catch(e){
    alert("You cannot withdraw!");
  }

}



function App() {

  
  let [account, setAccount] = useState("0x");
  let [balance, setBalance] = useState(0);

  return (
    <div className="App">
      <header className="App-header">
        
        <div>Your address {account} </div>
        <div>You can withdraw {balance} ETH</div>

        <ButtonGroup>
          <button onClick={() => {Withdraw(setBalance)}}> Withdraw </button>
          <button onClick={() => {Connect(setAccount, setBalance)}}> Connect Wallet </button>
        </ButtonGroup>

      </header>
    </div>
  );
}

export default App;
