"""
Double Columnar Transposition Cipher implementation.

The Double Columnar Transposition applies columnar transposition twice,
providing stronger security than single columnar transposition.

It can use:
1. Same keyword twice
2. Two different keywords

Process:
1. Apply first columnar transposition with keyword1
2. Apply second columnar transposition with keyword2 to the result

Args:
    text: Plaintext or ciphertext
    keyword1: First column arrangement keyword
    keyword2: Second column arrangement keyword
    encrypt: True for encryption, False for decryption
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from single import encrypt as single_encrypt, decrypt as single_decrypt


def encrypt(plaintext: str, keyword1: str, keyword2: str = None) -> str:
    """
    Encrypt plaintext using Double Columnar Transposition.
    
    Args:
        plaintext: Text to encrypt (case-insensitive)
        keyword1: First column arrangement keyword (required)
        keyword2: Second column arrangement keyword (defaults to keyword1)
    
    Returns:
        Encrypted ciphertext
    
    Example:
        >>> encrypt("HELLO WORLD", "KEY", "CIPHER")
        'output after two passes'
    """
    if not plaintext or not keyword1:
        return ""
    
    # If no second keyword, use the first one
    if keyword2 is None:
        keyword2 = keyword1
    
    # Apply first transposition
    first_pass = single_encrypt(plaintext, keyword1)
    
    # Apply second transposition
    result = single_encrypt(first_pass, keyword2)
    
    return result


def decrypt(ciphertext: str, keyword1: str, keyword2: str = None) -> str:
    """
    Decrypt ciphertext using Double Columnar Transposition.
    
    Args:
        ciphertext: Encrypted text
        keyword1: First column arrangement keyword (required)
        keyword2: Second column arrangement keyword (defaults to keyword1)
    
    Returns:
        Decrypted plaintext
    
    Example:
        >>> decrypt("encrypted text", "KEY", "CIPHER")
        'helloworld'
    """
    if not ciphertext or not keyword1:
        return ""
    
    # If no second keyword, use the first one
    if keyword2 is None:
        keyword2 = keyword1
    
    # Decrypt in reverse order (second transposition first)
    first_pass = single_decrypt(ciphertext, keyword2)
    
    # Decrypt first transposition
    result = single_decrypt(first_pass, keyword1)
    
    return result


if __name__ == "__main__":
    # Test the implementation
    print("=" * 60)
    print("DOUBLE COLUMNAR TRANSPOSITION CIPHER")
    print("=" * 60)
    
    plaintext = "HELLO WORLD"
    keyword1 = "KEY"
    keyword2 = "CIPHER"
    
    print(f"\nPlaintext:  {plaintext}")
    print(f"Keyword1:   {keyword1}")
    print(f"Keyword2:   {keyword2}")
    print(f"Plaintext (cleaned): {''.join([c.lower() for c in plaintext if c.isalpha()])}")
    
    encrypted = encrypt(plaintext, keyword1, keyword2)
    decrypted = decrypt(encrypted, keyword1, keyword2)
    
    print(f"\nEncrypted:  {encrypted}")
    print(f"Decrypted:  {decrypted}")
    print(f"Success:    {decrypted == ''.join([c.lower() for c in plaintext if c.isalpha()])}")
    
    # Test with same keyword twice
    print("\n" + "=" * 60)
    plaintext2 = "ATTACK AT DAWN"
    keyword = "SECRET"
    
    print(f"\nPlaintext:  {plaintext2}")
    print(f"Keyword:   {keyword} (used twice)")
    
    encrypted2 = encrypt(plaintext2, keyword)
    decrypted2 = decrypt(encrypted2, keyword)
    
    print(f"Encrypted:  {encrypted2}")
    print(f"Decrypted:  {decrypted2}")
    print(f"Success:    {decrypted2 == ''.join([c.lower() for c in plaintext2 if c.isalpha()])}")
    
    # Test with different keywords
    print("\n" + "=" * 60)
    plaintext3 = "CRYPTOGRAPHY IS FUN"
    keyword1_3 = "COLUMN"
    keyword2_3 = "TRANS"
    
    print(f"\nPlaintext:  {plaintext3}")
    print(f"Keyword1:   {keyword1_3}")
    print(f"Keyword2:   {keyword2_3}")
    
    encrypted3 = encrypt(plaintext3, keyword1_3, keyword2_3)
    decrypted3 = decrypt(encrypted3, keyword1_3, keyword2_3)
    
    print(f"Encrypted:  {encrypted3}")
    print(f"Decrypted:  {decrypted3}")
    print(f"Success:    {decrypted3 == ''.join([c.lower() for c in plaintext3 if c.isalpha()])}")

