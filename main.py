import random
import time
import requests
import ecdsa
import base58
from Crypto.Hash import keccak
# import threading

def keccak256(data):
    hasher = keccak.new(digest_bits=256)
    hasher.update(data)
    return hasher.digest()


def get_signing_key(raw_priv):
    return ecdsa.SigningKey.from_string(raw_priv, curve=ecdsa.SECP256k1)


def verifying_key_to_addr(key):
    pub_key = key.to_string()
    primitive_adder = b"\x41" + keccak256(pub_key)[-20:]
    Addr = base58.b58encode_check(primitive_adder)
    return Addr


# Замени 'api_key' на твой токен с сайта https://trongrid.io/
api_key = ''

# api_key2 = ''
# api_key3 = ''

def get_balance(address,api_key):
    url = f'https://api.trongrid.io/v1/accounts/{address}'
    key = str(api_key)
    headers = {
        'TRON-PRO-API-KEY': key
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        balance = data['data'][0]['balance'] if data['data'] else 0
        return balance
    else:
        print(f"Error fetching balance for address {address}: {response.status_code} {response.text}")
        return 0
input("  Больше сливов на tg канале @manual_link \n  Нажмите Enter...")
def check_wallet_balance(api_key):
    while True:
        raw = bytes(random.sample(range(0, 256), 32))
        key = get_signing_key(raw)

        private_key = raw.hex()
        address = verifying_key_to_addr(key.get_verifying_key()).decode()

        balance = get_balance(address, api_key)

        print(f'Private Key: {private_key}')
        print(f'Address: {address}')
        print(f'Balance: {balance} TRX')

        if balance > 0:
            print(f'Wallet with balance found! Private Key: {private_key}, Address: {address}, Balance: {balance} TRX')
            with open('wallets.txt', 'a') as f:
                f.write(f'PrivateKey: {private_key}\n')
                f.write(f'Address: {address}\n')
                f.write(f'Balance: {balance} TRX\n')
                f.write('-' * 30 + '\n')

        time.sleep(0.01)

# api_keys = [api_key1,api_key2,api_key3]

# for key in api_keys:
#     thread = threading.Thread(target=check_wallet_balance,args=[key])
#     thread.start()

check_wallet_balance(api_key)

