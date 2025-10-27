"""
Composite substitution ciphers module.

This module contains implementations of composite substitution ciphers,
which combine multiple cryptographic techniques for enhanced security.

Available ciphers:
- Straddling Checkerboard: Combines substitution and fractionation with numeric key addition
- Nihilist: Combines Polybius square substitution with numeric key addition
"""

from .straddling_checkerboard import (
    straddling_checkerboard_encrypt,
    straddling_checkerboard_decrypt,
    straddling_checkerboard_produce_checkerboard,
    straddling_checkerboard_generate_random_key,
    straddling_checkerboard_generate_key_for_text,
    straddling_checkerboard_encrypt_with_random_key
)

from .nihilist import (
    nihilist_encrypt,
    nihilist_decrypt,
    nihilist_produce_square,
    nihilist_generate_random_key,
    nihilist_generate_key_for_text,
    nihilist_encrypt_with_random_key
)

__all__ = [
    # Straddling Checkerboard
    'straddling_checkerboard_encrypt',
    'straddling_checkerboard_decrypt',
    'straddling_checkerboard_produce_checkerboard',
    'straddling_checkerboard_generate_random_key',
    'straddling_checkerboard_generate_key_for_text',
    'straddling_checkerboard_encrypt_with_random_key',
    
    # Nihilist
    'nihilist_encrypt',
    'nihilist_decrypt',
    'nihilist_produce_square',
    'nihilist_generate_random_key',
    'nihilist_generate_key_for_text',
    'nihilist_encrypt_with_random_key'
]
