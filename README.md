# merkle-tree-validation

1. Set up a Ganache instance
2. `createBalances.py` script generates file `src/balances.json` and puts a random withdraw value ( in range 0.1 - 0.01 ETH) for each account in Ganache
3. `createMerkle.py` script generates file `src/merkle_tree.json` which is a list of list containing the hashing values for each level (leaves are hashes too).
4. `truffle migrate` to deploy contract. The needed balance for the contract is sent at deployment.
5. `yarn install` then `yarn start` for the ui with wallet connection and transactions. `src/App.js` contains the proof construction.
