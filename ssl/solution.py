import requests
from cryptography import x509
from cryptography.x509.oid import NameOID
import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import datetime
import pycountry


def main():
    response = requests.get('https://hackattic.com/challenges/tales_of_ssl/problem?access_token=9099aaae9c650db1')
    print("Response:", response.content)
    res_json = response.json()
    b64_private_key = res_json['private_key']
    private_key = base64.b64decode(b64_private_key)
    private_key = serialization.load_der_private_key(private_key, password=None)
    if not isinstance(private_key, rsa.RSAPrivateKey):
        return
    required_data = res_json['required_data']
    domain = required_data['domain']
    serial_number = int(required_data['serial_number'], 0)
    country = required_data['country']
    
    country = country.replace("Islands", "").replace("Island", "").strip()
    country_iso = pycountry.countries.search_fuzzy(country)[0].alpha_2
    name = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, country_iso),
        x509.NameAttribute(NameOID.COMMON_NAME, domain),
    ])
    cert = (
        x509.CertificateBuilder()
        .subject_name(name)
        .issuer_name(name)
        .public_key(private_key.public_key())
        .serial_number(serial_number)
        .not_valid_before(datetime.datetime.now(datetime.timezone.utc))
        .not_valid_after(datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=5)) 
        .sign(private_key, hashes.SHA256()))

    cert_der = cert.public_bytes(serialization.Encoding.DER)
    certificate = { 'certificate' : base64.b64encode(cert_der).decode() }
    response = requests.post('https://hackattic.com/challenges/tales_of_ssl/solve?access_token=9099aaae9c650db1', json=certificate)
    print("Response:", response.content)


main()
