from web3 import Web3
from random import randint, uniform
from collections import OrderedDict
from json import dump

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))


accounts = {}
contractBalance = 0

for address in w3.eth.accounts:

    balance = w3.toWei(randint(10, 100), "milli")
    print(address, " - ", w3.fromWei(balance, "ether"), " ETH")
    sha = w3.sha3(text = address + str(balance))

    accounts[address] = balance
    contractBalance += balance

# Sort the dictionary based on the key

# accounts = OrderedDict(sorted(accounts.items(), key =  lambda kv: kv[0]))

with open("src/balances.json", "w") as file:
    dump(accounts, file)

print("needed Balance is ", w3.fromWei(contractBalance, "ether"), "ether = ", contractBalance, " wei")
