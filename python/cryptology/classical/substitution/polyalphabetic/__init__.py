"""
Polyalphabetic substitution ciphers module.

This module contains implementations of polyalphabetic substitution ciphers,
which use multiple alphabets to enhance security.

Available ciphers:
- Alberti: First polyalphabetic cipher with rotating disk system
- Vigenère: Classical polyalphabetic cipher with customizable tables
- Beaufort: Self-reciprocal polyalphabetic cipher
- Auto-key: Self-extending key polyalphabetic cipher
- Chaocipher: Dynamic alphabet permutation cipher
- Gronsfeld: Numeric key variant of Vigenère cipher
- Porta: Self-reciprocal polyalphabetic cipher with alphabet pairs
"""

from .alberti import encrypt as alberti_encrypt, decrypt as alberti_decrypt
from .vigenere import (encrypt as vigenere_encrypt, decrypt as vigenere_decrypt, 
                      produce_table as vigenere_produce_table,
                      generate_random_key as vigenere_generate_random_key,
                      generate_key_for_text as vigenere_generate_key_for_text,
                      encrypt_with_random_key as vigenere_encrypt_with_random_key)
from .beaufort import (encrypt as beaufort_encrypt, decrypt as beaufort_decrypt,
                      produce_table as beaufort_produce_table,
                      generate_random_key as beaufort_generate_random_key,
                      generate_key_for_text as beaufort_generate_key_for_text,
                      encrypt_with_random_key as beaufort_encrypt_with_random_key)
from .autokey import (encrypt as autokey_encrypt, decrypt as autokey_decrypt,
                     produce_table as autokey_produce_table,
                     generate_random_key as autokey_generate_random_key,
                     generate_key_for_text as autokey_generate_key_for_text,
                     encrypt_with_random_key as autokey_encrypt_with_random_key)
from .chaocipher import (encrypt as chaocipher_encrypt, decrypt as chaocipher_decrypt,
                        create_custom_alphabets as chaocipher_create_custom_alphabets,
                        create_alphabets_with_mono_ciphers as chaocipher_create_alphabets_with_mono_ciphers,
                        decrypt_with_alphabets as chaocipher_decrypt_with_alphabets)
from .gronsfeld import (encrypt as gronsfeld_encrypt, decrypt as gronsfeld_decrypt,
                       produce_table as gronsfeld_produce_table,
                       generate_random_numeric_key as gronsfeld_generate_random_numeric_key,
                       generate_numeric_key_for_text as gronsfeld_generate_numeric_key_for_text,
                       encrypt_with_random_key as gronsfeld_encrypt_with_random_key)
from .porta import (encrypt as porta_encrypt, decrypt as porta_decrypt,
                   produce_pairs as porta_produce_pairs,
                   generate_random_key as porta_generate_random_key,
                   generate_key_for_text as porta_generate_key_for_text,
                   encrypt_with_random_key as porta_encrypt_with_random_key)

__all__ = [
    'alberti_encrypt',
    'alberti_decrypt',
    'vigenere_encrypt',
    'vigenere_decrypt',
    'vigenere_produce_table',
    'vigenere_generate_random_key',
    'vigenere_generate_key_for_text',
    'vigenere_encrypt_with_random_key',
    'beaufort_encrypt',
    'beaufort_decrypt',
    'beaufort_produce_table',
    'beaufort_generate_random_key',
    'beaufort_generate_key_for_text',
    'beaufort_encrypt_with_random_key',
    'autokey_encrypt',
    'autokey_decrypt',
    'autokey_produce_table',
    'autokey_generate_random_key',
    'autokey_generate_key_for_text',
    'autokey_encrypt_with_random_key',
    'chaocipher_encrypt',
    'chaocipher_decrypt',
    'chaocipher_create_custom_alphabets',
    'chaocipher_create_alphabets_with_mono_ciphers',
    'chaocipher_decrypt_with_alphabets',
    'gronsfeld_encrypt',
    'gronsfeld_decrypt',
    'gronsfeld_produce_table',
    'gronsfeld_generate_random_numeric_key',
    'gronsfeld_generate_numeric_key_for_text',
    'gronsfeld_encrypt_with_random_key',
    'porta_encrypt',
    'porta_decrypt',
    'porta_produce_pairs',
    'porta_generate_random_key',
    'porta_generate_key_for_text',
    'porta_encrypt_with_random_key'
]
