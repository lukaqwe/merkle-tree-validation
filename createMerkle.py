from json import load, dump
from math import floor, log2, ceil
from web3 import Web3
from hexbytes import HexBytes

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545')) 


balances = {}




with open("src/balances.json", "r") as file:
    balances = load(file)

totalUsers = len(balances)
maxLvl = ceil(log2(totalUsers))



isComplete = False
if log2(totalUsers) == ceil(log2(totalUsers)):
    isComplete = True

def computeSha(left, right): # both are HexBytes
    if left < right:
        return  w3.keccak(left + right)
    else:
        return  w3.keccak(right + left)


# Constructing the last level of the merkle Tree
def constructLeaves(balances):
    if isComplete: # if it is a complete tree
        
        return {maxLvl : [w3.solidityKeccak(['address', 'uint256'], [x[0] , x[1]]) for x in balances.items()] }
    

    leafNodes = {maxLvl : [], maxLvl-1 : []} 

    lastLvlLeavesNum = 2*(totalUsers - 2**(maxLvl - 1 ))
    # secondLvlLeavesNum = totalUsers - lastLvlLeavesNum
    

    leafNodes[maxLvl] = [w3.solidityKeccak(['address', 'uint256'], [x[0] , x[1]]) for x in list(balances.items())[:lastLvlLeavesNum]] 
    leafNodes[maxLvl-1] = [w3.solidityKeccak(['address', 'uint256'], [x[0] , x[1]]) for x in list(balances.items())[lastLvlLeavesNum:]] 

            
    return leafNodes

def computeRootFromLeaves(merkleTree):

    # Make higher levels by computing hash of two values in a bottom-up manner

    if isComplete:
        for lvl in range(maxLvl, 0, -1):
            upperLvl = lvl - 1
            merkleTree[upperLvl] = []

            it = iter(merkleTree[lvl])

            for left in it:
                right = next(it)
                merkleTree[upperLvl].append(computeSha(left, right))
    else:
        # compute the first level
        it = iter(merkleTree[maxLvl])
        upperLvl = maxLvl - 1

        lastLvlLeavesNum = 2*(totalUsers - 2**(maxLvl - 1 ))
        secondLvlLeavesNum = totalUsers - lastLvlLeavesNum
        
        for left in it:
            right = next(it)
            merkleTree[upperLvl].append(computeSha(left, right)) # add at the beginning
        merkleTree[upperLvl] = merkleTree[upperLvl][secondLvlLeavesNum:] + merkleTree[upperLvl][:secondLvlLeavesNum]

        # compute the rest
        for lvl in range(maxLvl-1, 0, -1):
            upperLvl = lvl - 1
            merkleTree[upperLvl] = []

            it = iter(merkleTree[lvl])

            for left in it:
                right = next(it)
                merkleTree[upperLvl].append(computeSha(left, right))
    return merkleTree



merkleTree = constructLeaves(balances) # {level : [hash(1), hash(2), ..., hash(2**level - 1) ]} 

# print(merkleTree)

merkleTree = computeRootFromLeaves(merkleTree)

merkleTreeHex = []

print("Merkle tree : ")
for i in range(maxLvl + 1):
    print(len(merkleTree[i]))
    print([x.hex() for x in merkleTree[i]])
    merkleTreeHex.append([x.hex() for x in merkleTree[i]])
    print()

with open("src/merkle_tree.json", 'w') as file:
    dump(merkleTreeHex, file)
