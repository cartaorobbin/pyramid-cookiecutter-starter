import requests
import six
import struct
import base64

from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicNumbers
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization


def get_public_key(url):
    headers = {"Content-Type": "application/json; charset=utf-8"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    for key in response.json()["keys"]:
        if key["kid"].startswith("s-"):
            return key


def get_public_pen(url):
    headers = {"Content-Type": "application/json; charset=utf-8"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    for key in response.json()["keys"]:
        if key["kid"].startswith("s-"):
            return jwk_to_pem(key)


def intarr2long(arr):
    return int("".join(["%02x" % byte for byte in arr]), 16)


def base64_to_long(data):
    if isinstance(data, six.text_type):
        data = data.encode("ascii")

    # urlsafe_b64decode will happily convert b64encoded data
    _d = base64.urlsafe_b64decode(bytes(data) + b"==")
    return intarr2long(struct.unpack("%sB" % len(_d), _d))


def jwk_to_pem(jwk):
    """Convert a JWK to PEM format."""
    exponent = base64_to_long(jwk["e"])
    modulus = base64_to_long(jwk["n"])
    numbers = RSAPublicNumbers(exponent, modulus)
    public_key = numbers.public_key(backend=default_backend())
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    return pem
