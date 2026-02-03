import requests
from hashlib import sha256
import sys
import json

def main():
    response = requests.get('https://hackattic.com/challenges/mini_miner/problem?access_token=9099aaae9c650db1')
    response = response.json()
    print("Response:", response)
    difficulty = response['difficulty']
    print("Difficulty:", difficulty)

    nonce = None
    for i in range (sys.maxsize):
        response['block']['nonce'] = i
        block = json.dumps(response['block'], separators=(',',':'), sort_keys=True).encode('utf-8')
        hashed = sha256(block).digest()
        if int.from_bytes(hashed, 'big') >> (256 - difficulty) == 0:
            print("Correct nonce value:", i)
            nonce = i
            break

    result = { 'nonce' : nonce }
    response = requests.post('https://hackattic.com/challenges/mini_miner/solve?access_token=9099aaae9c650db1', json=result)
    print("Response:", response.content)


main()
