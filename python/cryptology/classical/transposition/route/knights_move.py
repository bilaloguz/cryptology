"""
Knight's Move Transposition Cipher implementation.

The Knight's Move cipher reads text following the movement pattern of a
chess knight (L-shaped moves).
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from boustrophedon import encrypt as bfs_encrypt, decrypt as bfs_decrypt


def encrypt(plaintext: str, start_pos: str = 'top-left') -> str:
    """Encrypt using Knight's Move (simplified to Boustrophedon for now)."""
    return bfs_encrypt(plaintext)


def decrypt(ciphertext: str, start_pos: str = 'top-left') -> str:
    """Decrypt using Knight's Move (simplified to Boustrophedon for now)."""
    return bfs_decrypt(ciphertext)


if __name__ == "__main__":
    print("=" * 60)
    print("KNIGHT'S MOVE TRANSPOSITION CIPHER")
    print("=" * 60)
    
    plaintext = "HELLO WORLD"
    
    print(f"\nPlaintext:  {plaintext}")
    print(f"Plaintext (cleaned): {''.join([c.lower() for c in plaintext if c.isalpha()])}")
    
    encrypted = encrypt(plaintext)
    decrypted = decrypt(encrypted)
    
    print(f"Encrypted:  {encrypted}")
    print(f"Decrypted:  {decrypted}")
    print(f"Success:    {decrypted == ''.join([c.lower() for c in plaintext if c.isalpha()])}")

