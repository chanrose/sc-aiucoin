# Deploying smart contract with web3
from web3 import Web3, HTTPProvider
from vyper import compile_codes

# Select which file you want to compile
source = open("AIUCoins.vy", 'r')
contract_source_code = source.read()
source.close()

smart_contract = {}
smart_contract['aiucoin'] = contract_source_code

# What we need
format = ['abi', 'bytecode']
compiled_code = compile_codes(smart_contract, format, 'dict')

abi, bytecode = compiled_code['aiucoin']['abi'], compiled_code['aiucoin']['bytecode']

w3 = Web3(HTTPProvider('http://localhost:7545'))

AiucoinSC = w3.eth.contract(abi=abi, bytecode=bytecode)

# Select the Pub Address or Account Address that you want to initiate the contract
tx_hash = AiucoinSC.constructor().transact({
    'from': '0x3f356774Bf88b134De7cf66a30654007B4d2d9D3'
})

tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
print(tx_receipt)
