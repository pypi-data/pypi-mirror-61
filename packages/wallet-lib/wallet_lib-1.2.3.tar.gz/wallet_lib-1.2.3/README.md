# Wallet lib
[![PyPI version](https://badge.fury.io/py/wallet-lib.svg)](https://badge.fury.io/py/wallet-lib) ![](https://github.com/Bitcoin-com/wallet_lib/workflows/CI/badge.svg)
## Description
This library contains classes to work with hot wallet for different cryptocurrency.
## API Documentation
### Supported cryptocurrencies
1. BCH
1. BTC
1. DASH
1. ZEC
### Methods
1. `wallet.create_address(label=None)` - creates an address (label is ignored for ZEC)
1. `wallet.get_balance()` - returns the current balance
1. `wallet.get_transaction(tx_id)` - returns transaction info by tx id
1. `wallet.get_transactions(label=None, count=25, offset=0)` - returns list of transactions by label based on count and offset arguments.
1. `wallet.send(address, amount)` - sends some amount to an address.
1. `wallet.get_transactions_since(block_hash)` - gets all transactions since block block_hash, or all transactions if block_hash is None. (No mempool transactions)
1. `wallet.run(command, args...)` - runs a custom command with the arguments specified
1. `wallet.get_zmq_notifier(zmq_address, topics=[TOPIC_BLOCKHASH,...], loop=None, verbose=False)` - API for receiving topics from specified zmq address (ipc, tpc and udp supported).
