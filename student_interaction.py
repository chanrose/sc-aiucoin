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

contract = {
    'contract_addr': '',
    'sender': '',
    'private_key': ''
}

def set_default_acc():
    sender = Web3.toChecksumAddress(str(input("Enter Account Address: ")).strip())
    sender_private_key = str(input("Enter Private key: ")).strip()
    contract['sender'], w3.eth.defaultAccount, contract['private_key'] = sender, sender, sender_private_key
    print("Sender and Private key updated\n")

def set_contract_acc():
    contract['contract_addr'] = str(input("Contract Address: ")).strip()
    asc = w3.eth.contract(address=contract['contract_addr'], abi=abi)
    print("Contract address updated\n")

def get_account_address():
    print("Owner Acc:", contract['sender'])

def get_account_balance_auc():
    balance = asc.functions.get_account_balance().call()
    print("AUC:", balance, "units")


def get_account_balance_eth():
    balance = asc.functions.get_account_balance().call()
    balance = asc.functions.convert_aucs_to_weis(balance).call()
    balance = balance / 10**18
    print("ETH:", balance, "units")

def get_account_nonce():
    nonce = w3.eth.getTransactionCount(w3.eth.defaultAccount)
    print("TX count:", nonce)

def deposit_auc():
    nonce = w3.eth.getTransactionCount(w3.eth.defaultAccount)
    auc_unit = int(input("AUC: "))
    auc_to_wei = asc.functions.convert_aucs_to_weis(auc_unit).call()
    txn = asc.functions.deposit_aucs(contract['sender']).buildTransaction({
        'value': auc_to_wei,
        'gas': 100000,
        'gasPrice': w3.toWei('1', 'gwei'),
        'nonce': nonce
    })
    signed_txn = w3.eth.account.signTransaction(txn, private_key=contract['private_key'])
    signed_txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    print(f"Deposit {auc_unit} units successfully")


def send_auc_other_acc():
    nonce = w3.eth.getTransactionCount(w3.eth.defaultAccount)
    recipient_addr = str(input("Recipient Address: ")).strip()
    auc_unit = int(input("AUC: "))
    auc_to_wei = asc.functions.convert_aucs_to_weis(auc_unit).call()
    # Withdraw 
    txn = asc.functions.withdraw_aucs(auc_unit).buildTransaction({
        'gas': 100000,
        'gasPrice': w3.toWei('1', 'gwei'),
        'nonce': nonce
    })
    signed_txn = w3.eth.account.signTransaction(txn, private_key=contract['private_key'])
    signed_txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)

    # Deposit to others
    txn = asc.functions.deposit_aucs(Web3.toChecksumAddress(recipient_addr)).buildTransaction({
        'value': auc_to_wei,
        'gas': 100000,
        'gasPrice': w3.toWei('1', 'gwei'),
        'nonce': nonce + 1
    })
    signed_txn = w3.eth.account.signTransaction(txn, private_key=contract['private_key'])
    signed_txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    print(f"Sent {auc_unit} units to {recipient_addr} successfully")

def display_auc_eth():
    auc_wei = asc.functions.convert_aucs_to_weis(1).call()
    auc_eth = auc_wei / (10 ** 18)
    print(f"1 AUC = {auc_eth} ETH")
 
def display_eth_auc():
    eth_auc = asc.functions.convert_weis_to_aucs(10**18).call()
    print(f"1 ETH = {eth_auc} AUC")

def exit():
    print("Saiyonara!")

print("Starting AUC Dashboard...\n")
menu = {
    0: set_default_acc,
    1: set_contract_acc,
    2: get_account_address,
    3: get_account_balance_auc,
    4: get_account_balance_eth,
    5: get_account_nonce,
    6: send_auc_other_acc,
    7: deposit_auc,
    8: display_auc_eth,
    9: display_eth_auc,
    10: exit
}

def display_menu():
    print("="*10, "Menu", "="*10)
    for key, val in menu.items():
        print(f"{key}: {val.__name__}")
    print("")

def check_contract():
    if contract['contract_addr'] or contract['sender'] or contract['private_key']:
        print("Required information fulfilled!")
    else:
        print("Please enter the following detail first:")
        menu[0]()
        menu[1]()

check_contract()
asc = w3.eth.contract(address=contract['contract_addr'], abi=abi)
w3.eth.defaultAccount = contract['sender']
exit = False

while not exit:
    display_menu()
    your_option = int(str(input("Your Pick: ")).strip())
    if your_option >= 0 and your_option <= 9:
        menu[your_option]()
    else:
        menu[10]()
        exit = True
    print("")
    
