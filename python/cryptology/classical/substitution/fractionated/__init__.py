"""
Fractionated substitution ciphers module.

This module contains implementations of fractionated substitution ciphers,
which use techniques like fractionation to enhance security.

Available ciphers:
- Bifid: Uses a 5x5 Polybius square with fractionation
- Trifid: Uses a 3x3x3 cube with fractionation
"""

from .bifid import encrypt as bifid_encrypt, decrypt as bifid_decrypt
from .trifid import encrypt as trifid_encrypt, decrypt as trifid_decrypt

__all__ = [
    'bifid_encrypt',
    'bifid_decrypt', 
    'trifid_encrypt',
    'trifid_decrypt'
]
