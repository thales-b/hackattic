import requests
import subprocess
import os
import bcrypt


def main():
    response = requests.get('https://hackattic.com/challenges/dockerized_solutions/problem?access_token=9099aaae9c650db1')
    print("Response:", response.content)
    creds = response.json()['credentials']
    password = creds['password']
    user = creds['user']
    ignition_key = response.json()['ignition_key']
    trigger_token = response.json()['trigger_token']

    salt = bcrypt.gensalt(rounds=12, prefix=b"2b")
    hashed_password = bcrypt.hashpw(password.encode(), salt).decode()
    with open("htpasswd", "w") as f:
        f.write(f"{user}:{hashed_password}\n")
    os.chmod("htpasswd", 0o644)
    
    subprocess.run(["./create-registry.sh"])

    host = { 'registry_host' : "shy-hotels-hear.loca.lt" }
    response = requests.post(f'https://hackattic.com/_/push/{trigger_token}', json=host)

    tags = requests.get("http://localhost:5000/v2/hack/tags/list", auth=(user, password)).json()['tags']
    for tag in tags:
        image_name = f"localhost:5000/hack:{tag}"
        subprocess.run(["docker", "login", "localhost:5000", "-u", 
                        user, "-p", password])
        subprocess.run(["docker", "pull", image_name])
        res = subprocess.run(["docker", "run", "--rm", "-e", 
            f"IGNITION_KEY={ignition_key}", image_name],
            capture_output=True, text=True
        )
        secret = res.stdout.strip()
        print("Secret:", secret)
        if "oops" not in secret.lower():
            response = requests.post(f"https://hackattic.com/challenges/dockerized_solutions/solve?access_token=9099aaae9c650db1", json={"secret": secret})
            print("Respose:", response.content)
            break


main()
