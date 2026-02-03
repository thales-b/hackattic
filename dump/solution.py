import requests
import base64
import gzip
import re

def main():
    response = requests.get('https://hackattic.com/challenges/backup_restore/problem?access_token=9099aaae9c650db1')
    b64_dump = response.json()['dump']
    dump = base64.b64decode(b64_dump)
    decompressed_dump = gzip.decompress(dump).decode('utf-8')
    
    relevant_data = decompressed_dump.split('stdin;\n')[1]
    relevant_data = relevant_data.split('\n\\.')[0]
    
    data_parts = re.split('\t|\n', relevant_data)
    alive_ssns = []
    num_cols = 8
    status_col = 7
    ssn_col = 3
    i = 0
    end = len(data_parts)
    while i < end:
        status = data_parts[i + status_col]
        if status == "alive":
            ssn = data_parts[i + ssn_col]
            alive_ssns.append(ssn)
            print("SSN:", ssn)
        i += 8

    result = {'alive_ssns': alive_ssns }
    response = requests.post('https://hackattic.com/challenges/backup_restore/solve?access_token=9099aaae9c650db1', json=result)
    print("Response:", response.content)
    

main()
