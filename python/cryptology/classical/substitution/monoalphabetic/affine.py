"""
Affine Cipher implementation.

The Affine cipher is a monoalphabetic substitution cipher that uses modular arithmetic.
It is the general form of all linear monoalphabetic substitution ciphers.

Encryption: E(x) = (ax + b) mod m
Decryption: D(y) = a^(-1) * (y - b) mod m

Where:
- a, b are the keys (a must be coprime with m)
- m is the size of the alphabet
- a^(-1) is the modular multiplicative inverse of a
"""

import math

# Default English alphabet (lowercase only)
DEFAULT_ALPHABET = "abcdefghijklmnopqrstuvwxyz"


def _gcd(a: int, b: int) -> int:
    """Calculate greatest common divisor using Euclidean algorithm."""
    while b:
        a, b = b, a % b
    return a


def _mod_inverse(a: int, m: int) -> int:
    """
    Calculate modular multiplicative inverse of a modulo m.
    Uses Extended Euclidean Algorithm.
    """
    if _gcd(a, m) != 1:
        raise ValueError(f"No modular inverse exists: gcd({a}, {m}) != 1")
    
    # Extended Euclidean Algorithm
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    
    return x1 % m0


def encrypt(plaintext: str, a: int, b: int, alphabet: str = DEFAULT_ALPHABET) -> str:
    """
    Encrypt plaintext using Affine cipher.
    
    Args:
        plaintext: The text to encrypt (will be converted to lowercase)
        a: The multiplicative key (must be coprime with alphabet length)
        b: The additive key
        alphabet: The alphabet to use for encryption (default: English lowercase)
    
    Returns:
        The encrypted ciphertext
    
    Raises:
        ValueError: If a is not coprime with the alphabet length
    
    Example:
        >>> encrypt("HELLO", 5, 8)
        'rclla'
    """
    m = len(alphabet)
    
    # Check that a is coprime with m
    if _gcd(a, m) != 1:
        raise ValueError(f"Key 'a' ({a}) must be coprime with alphabet length ({m})")
    
    # Convert input to lowercase
    plaintext = plaintext.lower()
    result = []
    
    for char in plaintext:
        if char in alphabet:
            # Get position in alphabet
            x = alphabet.index(char)
            # Apply affine transformation: E(x) = (ax + b) mod m
            encrypted_pos = (a * x + b) % m
            result.append(alphabet[encrypted_pos])
        else:
            # Keep characters not in alphabet unchanged
            result.append(char)
    
    return ''.join(result)


def decrypt(ciphertext: str, a: int, b: int, alphabet: str = DEFAULT_ALPHABET) -> str:
    """
    Decrypt ciphertext using Affine cipher.
    
    Args:
        ciphertext: The text to decrypt (will be converted to lowercase)
        a: The multiplicative key that was used for encryption
        b: The additive key that was used for encryption
        alphabet: The alphabet that was used for encryption (default: English lowercase)
    
    Returns:
        The decrypted plaintext
    
    Raises:
        ValueError: If a is not coprime with the alphabet length
    
    Example:
        >>> decrypt("rclla", 5, 8)
        'hello'
    """
    m = len(alphabet)
    
    # Check that a is coprime with m
    if _gcd(a, m) != 1:
        raise ValueError(f"Key 'a' ({a}) must be coprime with alphabet length ({m})")
    
    # Calculate modular inverse of a
    a_inv = _mod_inverse(a, m)
    
    # Convert input to lowercase
    ciphertext = ciphertext.lower()
    result = []
    
    for char in ciphertext:
        if char in alphabet:
            # Get position in alphabet
            y = alphabet.index(char)
            # Apply inverse affine transformation: D(y) = a^(-1) * (y - b) mod m
            decrypted_pos = (a_inv * (y - b)) % m
            result.append(alphabet[decrypted_pos])
        else:
            # Keep characters not in alphabet unchanged
            result.append(char)
    
    return ''.join(result)

