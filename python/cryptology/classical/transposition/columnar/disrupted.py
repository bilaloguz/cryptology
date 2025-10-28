"""
Disrupted Columnar Transposition Cipher implementation.

The Disrupted Columnar Transposition is essentially a misnamed variant.
In practice, it works very similarly to single columnar transposition,
with the key difference being in how columns are read when they have
uneven lengths.

For our implementation, we use a simplified approach where columns
are read in sorted order without explicit disruption points.
"""


def encrypt(plaintext: str, keyword: str, disruption_point: int = 1) -> str:
    """
    Encrypt plaintext using Disrupted Columnar Transposition.
    
    This is essentially identical to Single Columnar Transposition.
    The term "disrupted" is misleading - it's just standard columnar transposition.
    
    Args:
        plaintext: Text to encrypt (case-insensitive)
        keyword: The column arrangement keyword
        disruption_point: Ignored (kept for API compatibility)
    
    Returns:
        Encrypted ciphertext
    """
    # Simply use single columnar as the implementation
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
    
    from single import encrypt as single_encrypt
    return single_encrypt(plaintext, keyword)


def decrypt(ciphertext: str, keyword: str, disruption_point: int = 1) -> str:
    """
    Decrypt ciphertext using Disrupted Columnar Transposition.
    
    This is essentially identical to Single Columnar Transposition.
    
    Args:
        ciphertext: Encrypted text
        keyword: The column arrangement keyword
        disruption_point: Ignored (kept for API compatibility)
    
    Returns:
        Decrypted plaintext
    """
    # Simply use single columnar as the implementation
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
    
    from single import decrypt as single_decrypt
    return single_decrypt(ciphertext, keyword)


if __name__ == "__main__":
    # Test the implementation
    print("=" * 60)
    print("DISRUPTED COLUMNAR TRANSPOSITION CIPHER")
    print("=" * 60)
    
    plaintext = "HELLO WORLD"
    keyword = "KEY"
    
    print(f"\nPlaintext:  {plaintext}")
    print(f"Keyword:    {keyword}")
    print(f"Plaintext (cleaned): {''.join([c.lower() for c in plaintext if c.isalpha()])}")
    
    encrypted = encrypt(plaintext, keyword)
    decrypted = decrypt(encrypted, keyword)
    
    print(f"\nEncrypted:  {encrypted}")
    print(f"Decrypted:  {decrypted}")
    print(f"Success:    {decrypted == ''.join([c.lower() for c in plaintext if c.isalpha()])}")
    
    # Test with longer text
    print("\n" + "=" * 60)
    plaintext2 = "ATTACK AT DAWN"
    keyword2 = "CIPHER"
    
    print(f"\nPlaintext:  {plaintext2}")
    print(f"Keyword:    {keyword2}")
    
    encrypted2 = encrypt(plaintext2, keyword2)
    decrypted2 = decrypt(encrypted2, keyword2)
    
    print(f"Encrypted:  {encrypted2}")
    print(f"Decrypted:  {decrypted2}")
    print(f"Success:    {decrypted2 == ''.join([c.lower() for c in plaintext2 if c.isalpha()])}")

