import requests
import base64
import struct 

def main():
    response = requests.get('https://hackattic.com/challenges/help_me_unpack/problem?access_token=9099aaae9c650db1')
    if response.status_code != 200:
        print("Request failed")
        return 1

    json_res = response.json()
    b64_str = json_res['bytes']
    print("Base 64 string received:", b64_str)
    my_bytes = base64.b64decode(b64_str)
    print("Bytes:", my_bytes)
    
    solution = {}
    my_int = int.from_bytes(my_bytes[:4], byteorder='little', signed=True)
    solution['int'] = my_int
    print("Int:", my_int)
    uint = int.from_bytes(my_bytes[4:8], byteorder='little', signed=False)
    solution['uint'] = uint
    print("Uint:", uint)
    short = int.from_bytes(my_bytes[8:10], byteorder='little', signed=True) 
    solution['short'] = short
    print("Short:", short)
    my_float = struct.unpack('<f',my_bytes[12:16])[0]
    solution['float'] = my_float
    print("Float:", my_float)
    double = struct.unpack('<d', my_bytes[16:24])[0]
    solution['double'] = double
    print("Double:", double)
    big_endian_double = struct.unpack('>d', my_bytes[24:32])[0]
    solution['big_endian_double'] = big_endian_double
    print("Big-endian double:", big_endian_double)

    response = requests.post('https://hackattic.com/challenges/help_me_unpack/solve?access_token=9099aaae9c650db1', json=solution)
    print("Response:", response.content)

main()
