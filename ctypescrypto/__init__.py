"""
    Interface to some libcrypto functions

"""


import sys

from django.conf import settings


def config(filename=None):
    """
        Loads OpenSSL Config file. If none are specified, loads default
        (compiled in) one
    """
    libcrypto.OPENSSL_config(filename)

__all__ = ['config']


from cryptography.hazmat.backends.openssl.backend import backend


libcrypto = backend._lib
ffi = backend._ffi

FILETYPE_PEM = libcrypto.SSL_FILETYPE_PEM
FILETYPE_ASN1 = libcrypto.SSL_FILETYPE_ASN1

if settings.OPENSSL_CONFIG:
    print settings.OPENSSL_CONFIG
    # config(str(settings.OPENSSL_CONFIG))
    config('/etc/ssl/openssl.cnf')
