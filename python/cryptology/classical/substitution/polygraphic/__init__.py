"""
Polygraphic substitution ciphers module.

This module contains implementations of polygraphic substitution ciphers
that operate on groups of letters (digrams, trigrams, etc.) rather than
single letters.

Available ciphers:
- Playfair: Uses a 5x5 key square for digram encryption
- Two Square: Uses two 5x5 key squares for digram encryption  
- Four Square: Uses four 5x5 key squares for digram encryption
- Hill: Uses matrix multiplication for n-gram encryption
"""

from .playfair import encrypt as playfair_encrypt, decrypt as playfair_decrypt
from .two_square import encrypt as two_square_encrypt, decrypt as two_square_decrypt
from .four_square import encrypt as four_square_encrypt, decrypt as four_square_decrypt
from .hill import encrypt as hill_encrypt, decrypt as hill_decrypt

__all__ = [
    'playfair_encrypt', 'playfair_decrypt',
    'two_square_encrypt', 'two_square_decrypt', 
    'four_square_encrypt', 'four_square_decrypt',
    'hill_encrypt', 'hill_decrypt'
]
