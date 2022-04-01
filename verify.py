
from json import load, dump
from math import floor, log2, ceil
from web3 import Web3
from hexbytes import HexBytes

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545')) 

# THIS SCRIPT IS JUST A SKETCH. THE ACTUAL PROOF IS COMPUTED IN JS


totalUsers = 14
balances = {}

isComplete = False
if log2(totalUsers) == ceil(log2(totalUsers)):
    isComplete = True

maxLvl = ceil(log2(totalUsers))


def getIndex(List, Element):
    if Element in List:
        return List.index(Element)
    return -1

def provideProof(address): # address is string
    
    address_digest = w3.solidityKeccak(['address', 'uint256'], [address , balances[address]])
    
    lvl = 0
    idx = 0
	
    if isComplete:
        lvl = maxLvl
        idx = getIndex(merkleTree[lvl], address_digest)
    else:
        lvl = maxLvl
        idx = getIndex(merkleTree[lvl], address_digest)
        if idx == -1:
            lvl = maxLvl - 1
            idx = getIndex(merkleTree[lvl], address_digest)

    if idx == -1:
        return None

    proof = []
    neighbor_idx = 0
    
    while(lvl != 0):
        
        if idx % 2 == 1:
            neighbor_idx = idx - 1 # neighbor is on the left
        else:
            neighbor_idx = idx + 1 # neighbor is on the right

        idx = floor(idx/2)
        proof.append(merkleTree[lvl][neighbor_idx])
        
        lvl -= 1

    return proof

address = '0x2196654541E63b03dc97d52658E6ae53e7d52063'
balance = balances[address] 


proof = provideProof(address)
print("Proof = ", [x.hex() for x in  proof])
print()


root = merkleTree[0][0]

def verifyProof(proof, address, balance): # idx is index of the address in the sorted array

    digest = w3.solidityKeccak(['address', 'uint256'], [address, balance])
    
    print("Sha of the user", digest.hex())

    for neighbor in proof:
        digest = computeSha(digest, neighbor)
        # print(digest)
        
    return digest == root

print(verifyProof(proof, address, balance))

def callContract(_abi, _address):
    contract = w3.eth.contract(address = _address, abi = _abi)
    
    tx = {"from": "0x3DE40852aB49355Cb15e750D001214D3292B0557"}
    txHash = contract.functions.withdraw(proof, address, balance).transact(tx).hex()
    tx_receipt = w3.eth.wait_for_transaction_receipt(txHash)
    print(tx_receipt)

callContract([
	{
		"inputs": [],
		"stateMutability": "payable",
		"type": "constructor"
	},
	{
		"inputs": [
			{
				"internalType": "bytes32",
				"name": "left",
				"type": "bytes32"
			},
			{
				"internalType": "bytes32",
				"name": "right",
				"type": "bytes32"
			}
		],
		"name": "computeSha",
		"outputs": [
			{
				"internalType": "bytes32",
				"name": "",
				"type": "bytes32"
			}
		],
		"stateMutability": "pure",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "merkleRoot",
		"outputs": [
			{
				"internalType": "bytes32",
				"name": "",
				"type": "bytes32"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "bytes32[]",
				"name": "proof",
				"type": "bytes32[]"
			},
			{
				"internalType": "address payable",
				"name": "receiver",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			}
		],
		"name": "withdraw",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	}
], "0x5f2684eEaA03180F8219b57db0ba85Dcf760979d")
