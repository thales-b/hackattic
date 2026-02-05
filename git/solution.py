import requests
import subprocess
import os


def main():
    response = requests.get('https://hackattic.com/challenges/hosting_git/problem?access_token=9099aaae9c650db1').json()
    print("Response:", response)
    ssh_key = response['ssh_key'] 
    username = response['username']
    repo_path = response['repo_path']
    push_token = response['push_token']

    subprocess.run(f"useradd -m -s /usr/bin/git-shell {username}", shell=True)
    ssh_dir = f"/home/{username}/.ssh"
    os.makedirs(ssh_dir, mode=0o700, exist_ok=True)
    subprocess.run(f'echo "{ssh_key}\n" >> {ssh_dir}/authorized_keys', shell=True)
    subprocess.run(f"chmod 600 {ssh_dir}/authorized_keys", shell=True)
    subprocess.run(f"chown -R {username}:{username} /home/{username}", shell=True)

    repo = f"/home/{username}/{repo_path}"
    subprocess.run(f"mkdir -p {os.path.dirname(repo)}", shell=True)
    subprocess.run(f"git init --bare {repo}", shell=True)
    subprocess.run(f"chown -R {username}:{username} {repo}", shell=True)

    host = { 'repo_host' : 'ip' }
    response = requests.post(f"https://hackattic.com/_/git/{push_token}", json=host)
    print("Response:", response.content)
    
    solution = subprocess.getoutput(f"git --git-dir={repo} show HEAD:solution.txt").strip()
    secret = { 'secret' : solution }
    print("Solution:", solution)
    response = requests.post('https://hackattic.com/challenges/hosting_git/solve?access_token=9099aaae9c650db1', json=secret)
    print("Response:", response.content)

main()
