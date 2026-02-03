import requests
import subprocess
import re
import zipfile

def main():
    response = requests.get('https://hackattic.com/challenges/brute_force_zip/problem?access_token=9099aaae9c650db1')
    response = response.json()
    print("Response:", response)
    zip_url = response['zip_url']
    zip_content = requests.get(zip_url).content
    zip_name = "package.zip"
    with open(zip_name, "wb") as f:
            f.write(zip_content)

    zip2john_proc = subprocess.run(["./zip2john", zip_name],
                    capture_output=True, text=True)
    zip_hash = re.search(r"(\$pkzip\$.*?\$)", zip2john_proc.stdout).group(1) 
    print("Zip hash:", zip_hash)
    with open("tmp.hash", "w") as f:
        f.write(zip_hash)
    
    hashcat_proc = subprocess.run(["./hashcat.sh"], 
                                  capture_output=True, text=True)
    pwd = hashcat_proc.stdout.strip()
    print("Password:", pwd, "End")

    subprocess.run(
        ["unzip", "-o", "-P", pwd, "package.zip", "secret.txt"], 
    )
    with open("secret.txt", "r") as f:
        secret = f.read().strip()


    print("Secret:", secret)
    result = { "secret" : secret }
    response = requests.post('https://hackattic.com/challenges/brute_force_zip/solve?access_token=9099aaae9c650db1', json=result)
    print("Response:", response.content)

main()
