import requests
import base64
import hashlib
import hmac
import scrypt


def main():
    response = requests.get('https://hackattic.com/challenges/password_hashing/problem?access_token=9099aaae9c650db1')
    print("Response:", response.content)
    response = response.json()
    password = response['password']
    salt = base64.b64decode(response['salt'])
    print("Salt:", salt)
    result = {}

    sha256_hash = hashlib.sha256(password.encode()).hexdigest()
    result['sha256'] = sha256_hash

    hmac256 = hmac.new(salt, password.encode(), hashlib.sha256).hexdigest()
    result['hmac'] = hmac256

    rounds = response['pbkdf2']['rounds']
    digest = response['pbkdf2']['hash']
    pbkdf2_hash = hashlib.pbkdf2_hmac(digest, password.encode(), salt, iterations=rounds).hex()
    result['pbkdf2'] = pbkdf2_hash

    n = response['scrypt']['N']
    p = response['scrypt']['p']
    r = response['scrypt']['r']
    buflen = response['scrypt']['buflen']
    control = response['scrypt']['_control']
    scrypt_hash = scrypt.hash(password.encode(), salt=salt, 
                                 N=n, r=r, p=p, buflen=buflen, 
                                 ).hex()
    result['scrypt'] = scrypt_hash

    response = requests.post('https://hackattic.com/challenges/password_hashing/solve?access_token=9099aaae9c650db1', json=result)
    print("Response:", response.content)

main()
