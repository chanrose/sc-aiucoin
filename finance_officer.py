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

# Contract Address
contract = {
    'contract_addr': '',
    'sender': '',
    'private_key': ''
}

def set_owner_default_acc():
    sender = str(input("Enter Account Address: ")).strip()
    sender_private_key = str(input("Enter Private key: ")).strip()
    contract['sender'], w3.eth.defaultAccount, contract['private_key'] = sender, sender, sender_private_key
    print("Sender and Private key updated\n")

def set_contract_acc():
    contract['contract_addr'] = str(input("Contract Address: ")).strip()
    asc = w3.eth.contract(address=contract['contract_addr'], abi=abi)
    print("Contract address updated\n")

def get_owner_account_address():
    print("Owner:", contract['sender'])


def register_student_account():
    nonce = w3.eth.getTransactionCount(w3.eth.defaultAccount)
    id = int(str(input("Student ID: ")).strip())
    acc_addr = str(input("Account Address: ")).strip()
    txn = asc.functions.register_account(id, acc_addr).buildTransaction({
        'gas': 100000,
        'gasPrice': w3.toWei('1', 'gwei'),
        'nonce': nonce
    })
    signed_txn = w3.eth.account.signTransaction(txn, private_key=contract['private_key'])
    signed_txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    w3.eth.waitForTransactionReceipt(signed_txn_hash)
    print(f"{id} has been created")

def get_contract_balance_in_auc():
    balance_wei = asc.functions.get_total_weis().call()
    balance_in_auc = asc.functions.convert_weis_to_aucs(balance_wei).call()
    print("AUC:", balance_in_auc, "units")

def get_contract_balance_in_eth():
    balance_wei = asc.functions.get_total_weis().call()
    print(f"ETH: {balance_wei * 10**18} units")

def send_auc_student_acc():
    nonce = w3.eth.getTransactionCount(w3.eth.defaultAccount)
    recipient_addr = str(input("Account Address: ")).strip()
    auc_unit = int(input("AUC: "))
    auc_to_wei = asc.functions.convert_aucs_to_weis(auc_unit).call()
    txn = asc.functions.deposit_aucs(recipient_addr).buildTransaction({
        'value': auc_to_wei,
        'gas': 100000,
        'gasPrice': w3.toWei('1', 'gwei'),
        'nonce': nonce
    })
    signed_txn = w3.eth.account.signTransaction(txn, private_key=contract['private_key'])
    signed_txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    print(f"Sent {auc_unit} units to {recipient_addr} successfully")

def deduct_auc_student_acc():
    nonce = w3.eth.getTransactionCount(w3.eth.defaultAccount)
    recipient_addr = str(input("Account Address: ")).strip()
    auc_unit = int(input("AUC: "))
    txn = asc.functions.deduct_aucs(recipient_addr, auc_unit).buildTransaction({
        'gas': 100000,
        'gasPrice': w3.toWei('1', 'gwei'),
        'nonce': nonce
    })

    signed_txn = w3.eth.account.signTransaction(txn, private_key=sender_private_key)
    signed_txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    w3.eth.waitForTransactionReceipt(signed_txn_hash)
    print(f"Deduct {auc_unit} units from {recipient_addr}")

def get_student_id_from_acc():
    nonce = w3.eth.getTransactionCount(w3.eth.defaultAccount)
    recipient_addr = str(input("Account Address: ")).strip()
    id = asc.functions.get_account_student_id(recipient_addr).call()
    print("Student ID:", id)

def get_student_balance_from_acc_auc():
    nonce = w3.eth.getTransactionCount(w3.eth.defaultAccount)
    recipient_addr = str(input("Account Address: ")).strip()
    balance = asc.functions.get_student_account_balance(recipient_addr).call()
    print("AUC Balance:", balance, "units")

def get_student_balance_from_acc_eth():
    nonce = w3.eth.getTransactionCount(w3.eth.defaultAccount)
    recipient_addr = str(input("Account Address: ")).strip()
    balance = asc.functions.get_student_account_balance(recipient_addr).call()
    balance = asc.functions.convert_aucs_to_weis(balance).call()
    balance = balance * 10**18
    print("ETH Balance:", balance, "units")

def get_list_of_acc():
    print(asc.functions.get_accounts_list().call())

def change_conversion_rate_wei_auc():
    nonce = w3.eth.getTransactionCount(w3.eth.defaultAccount)
    wei_auc_rate = int(input("New Wei AUC Rate: "))
    txn = asc.functions.change_conversion_rate_wei_auc(wei_auc_rate).buildTransaction({
        'gas': 100000,
        'gasPrice': w3.toWei('1', 'gwei'),
        'nonce': nonce
    })

    signed_txn = w3.eth.account.signTransaction(txn, private_key=contract['private_key'])
    signed_txn_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    w3.eth.waitForTransactionReceipt(signed_txn_hash)

def display_auc_eth():
    auc_wei = asc.functions.convert_aucs_to_weis(1).call()
    auc_eth = auc_wei / (10 ** 18)
    print(f"1 AUC = {auc_eth} ETH")
 
def display_eth_auc():
    eth_auc = asc.functions.convert_weis_to_aucs(10**18).call()
    print(f"1 ETH = {eth_auc} AUC")

def exit():
    print("Saiyonara!")

print("Starting AUC Management...\n")
menu = {
    0: set_owner_default_acc,
    1: set_contract_acc,
    2: get_owner_account_address,
    3: register_student_account,
    4: get_contract_balance_in_auc,
    5: get_contract_balance_in_eth,
    6: send_auc_student_acc,
    7: deduct_auc_student_acc,
    8: get_student_id_from_acc,
    9: get_student_balance_from_acc_auc,
    10: get_student_balance_from_acc_eth,
    11: get_list_of_acc,
    12: change_conversion_rate_wei_auc,
    13: display_auc_eth,
    14: display_eth_auc,
    15: exit
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
    if your_option >= 0 and your_option <= 14:
        menu[your_option]()
    else:
        menu[15]()
        exit = True
    print('')
    

