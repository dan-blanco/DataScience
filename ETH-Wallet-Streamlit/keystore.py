import os
import time
import json
from web3 import Web3
from decimal import Decimal
from dotenv import load_dotenv
from eth_account import Account

from pathlib import Path
from getpass import getpass

from pathlib import Path
import streamlit as st

def read_account(password):
    with open(keystore_file) as keyfile:
        encrypted_key = keyfile.read()
        private_key = w3.eth.account.decrypt(
            encrypted_key, password)
        account = Account.from_key(private_key)
        return account



def create_raw_tx(account, recipient, amount):
    gasEstimate = w3.eth.estimateGas(
        {"from": account.address, "to": recipient, "value": amount}
    )
    return {
        "from": account.address,
        "to": recipient,
        "value": amount,
        "gasPrice": w3.eth.gasPrice,
        "gas": gasEstimate,
        "nonce": w3.eth.getTransactionCount(account.address),
    }


def send_tx(account, recipient, amount):
    tx = create_raw_tx(account, recipient, amount)
    signed_tx = account.sign_transaction(tx)
    result = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    print(result.hex())
    return result.hex()



load_dotenv()

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

keystore_file = Path("keystore.json")


if not keystore_file.is_file(): # if no wallet is found

    private_key = st.text_input("Enter your private key")

    password = st.text_input("Password to protect private key", type="password")

    if st.button("Save Private Key"):

        account = Account.encrypt(os.getenv("PRIVATE_KEY"), password)

        out_file = open(keystore_file, "w")

        json.dump(account, out_file)

        out_file.close()
else:

    recipient = st.text_input("Enter address to send transaction to")

    amount = st.text_input("How much would you like to send? ")

    password = st.text_input("Symmetric key to your Asymmetric keys", type="password")

    if st.button("View Wallet Info"):
        account = read_account(password)
        st.write("Account Address : " + account.address)
        st.write("Private Key : " + account.privateKey.hex())
        st.write(f"Account Balance : {w3.fromWei(w3.eth.getBalance(account.address),'ether')}")


    if st.button("Send Transaction"):
        account = read_account(password)
        amount = w3.toWei(Decimal(amount), 'ether')
        tx_hash = send_tx(account, recipient, amount)
        st.write("Transaction Hash :")
        st.write(tx_hash)

#print(account.address)
#print(account.privateKey.hex())
#print(w3.eth.getBalance(account.address))
#
#if "y" in input("Would you like to fund your new account? (y/n):"):
#    amount = input("How much ETH? :")
#
#    amount = w3.toWei(Decimal(amount), 'ether')
#
#
#    send_tx(Account.from_key(input("Enter private key:")), account.address, amount)
#    print("Waiting for transaction to send")
#    time.sleep(10)
#    print(w3.eth.getBalance(account.address))
#







