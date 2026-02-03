import requests
import tempfile
import os
import subprocess
import base64

def main():
    response = requests.get('https://hackattic.com/challenges/collision_course/problem?access_token=9099aaae9c650db1')
    print("Response:", response.content)
    include_bytes = response.json()['include'].encode()
    
    files = []
    prefix_path = "prefix.bin"
    with open(prefix_path, "wb") as f:
        f.write(include_bytes)
    subprocess.run(["./fastcoll", prefix_path,],
                   check=True)
    with open("md5_data1", "rb") as f1, open("md5_data2", "rb") as f2:
        files = [
            base64.b64encode(f1.read()).decode(),
            base64.b64encode(f2.read()).decode()
        ]

    result = { 'files' : files }
    response = requests.post('https://hackattic.com/challenges/collision_course/solve?access_token=9099aaae9c650db1&playground=1', json=result)
    print("Response:", response.content)


main()
