"""
Example demonstrating polygraphic substitution ciphers.

This example shows how to use the Playfair, Two Square, Four Square, and Hill ciphers.
"""

import sys
import os

# Add the parent directory to the path so we can import cryptology
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cryptology.classical.substitution.polygraphic.playfair import encrypt as playfair_encrypt, decrypt as playfair_decrypt
from cryptology.classical.substitution.polygraphic.two_square import encrypt as two_square_encrypt, decrypt as two_square_decrypt
from cryptology.classical.substitution.polygraphic.four_square import encrypt as four_square_encrypt, decrypt as four_square_decrypt
from cryptology.classical.substitution.polygraphic.hill import encrypt as hill_encrypt, decrypt as hill_decrypt


def demonstrate_playfair():
    """Demonstrate Playfair cipher."""
    print("=== Playfair Cipher ===")
    
    plaintext = "HELLO WORLD"
    key = "MONARCHY"
    
    print(f"Plaintext: {plaintext}")
    print(f"Key: {key}")
    
    encrypted = playfair_encrypt(plaintext, key)
    print(f"Encrypted: {encrypted}")
    
    decrypted = playfair_decrypt(encrypted, key)
    print(f"Decrypted: {decrypted}")
    print()


def demonstrate_two_square():
    """Demonstrate Two Square cipher."""
    print("=== Two Square Cipher ===")
    
    plaintext = "HELLO WORLD"
    key1 = "MONARCHY"
    key2 = "PLAYFAIR"
    
    print(f"Plaintext: {plaintext}")
    print(f"Key 1: {key1}")
    print(f"Key 2: {key2}")
    
    encrypted = two_square_encrypt(plaintext, key1, key2)
    print(f"Encrypted: {encrypted}")
    
    decrypted = two_square_decrypt(encrypted, key1, key2)
    print(f"Decrypted: {decrypted}")
    print()


def demonstrate_four_square():
    """Demonstrate Four Square cipher."""
    print("=== Four Square Cipher ===")
    
    plaintext = "HELLO WORLD"
    key1 = "MONARCHY"
    key2 = "PLAYFAIR"
    key3 = "CIPHER"
    key4 = "SECRET"
    
    print(f"Plaintext: {plaintext}")
    print(f"Key 1: {key1}")
    print(f"Key 2: {key2}")
    print(f"Key 3: {key3}")
    print(f"Key 4: {key4}")
    
    encrypted = four_square_encrypt(plaintext, key1, key2, key3, key4)
    print(f"Encrypted: {encrypted}")
    
    decrypted = four_square_decrypt(encrypted, key1, key2, key3, key4)
    print(f"Decrypted: {decrypted}")
    print()


def demonstrate_hill():
    """Demonstrate Hill cipher."""
    print("=== Hill Cipher ===")
    
    plaintext = "HELLO WORLD"
    key_matrix = [[3, 3], [2, 5]]
    
    print(f"Plaintext: {plaintext}")
    print(f"Key Matrix: {key_matrix}")
    
    encrypted = hill_encrypt(plaintext, key_matrix)
    print(f"Encrypted: {encrypted}")
    
    decrypted = hill_decrypt(encrypted, key_matrix)
    print(f"Decrypted: {decrypted}")
    print()


def demonstrate_hill_3x3():
    """Demonstrate Hill cipher with 3x3 matrix."""
    print("=== Hill Cipher (3x3 Matrix) ===")
    
    plaintext = "HELLO WORLD"
    key_matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 10]]
    
    print(f"Plaintext: {plaintext}")
    print(f"Key Matrix: {key_matrix}")
    
    encrypted = hill_encrypt(plaintext, key_matrix)
    print(f"Encrypted: {encrypted}")
    
    decrypted = hill_decrypt(encrypted, key_matrix)
    print(f"Decrypted: {decrypted}")
    print()


def demonstrate_security_comparison():
    """Demonstrate security differences between ciphers."""
    print("=== Security Comparison ===")
    
    plaintext = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
    
    # Playfair
    playfair_key = "MONARCHY"
    playfair_encrypted = playfair_encrypt(plaintext, playfair_key)
    
    # Two Square
    two_square_key1 = "MONARCHY"
    two_square_key2 = "PLAYFAIR"
    two_square_encrypted = two_square_encrypt(plaintext, two_square_key1, two_square_key2)
    
    # Four Square
    four_square_keys = ("MONARCHY", "PLAYFAIR", "CIPHER", "SECRET")
    four_square_encrypted = four_square_encrypt(plaintext, *four_square_keys)
    
    # Hill
    hill_matrix = [[3, 3], [2, 5]]
    hill_encrypted = hill_encrypt(plaintext, hill_matrix)
    
    print(f"Plaintext: {plaintext}")
    print(f"Playfair:  {playfair_encrypted}")
    print(f"Two Square: {two_square_encrypted}")
    print(f"Four Square: {four_square_encrypted}")
    print(f"Hill:      {hill_encrypted}")
    print()


def demonstrate_error_handling():
    """Demonstrate error handling."""
    print("=== Error Handling ===")
    
    # Test invalid keys
    try:
        playfair_encrypt("HELLO", "")
        print("ERROR: Should have raised ValueError for empty key")
    except ValueError as e:
        print(f"✓ Correctly caught empty key error: {e}")
    
    try:
        playfair_encrypt("HELLO", "123!@#")
        print("ERROR: Should have raised ValueError for non-letter key")
    except ValueError as e:
        print(f"✓ Correctly caught non-letter key error: {e}")
    
    # Test invalid Hill matrix
    try:
        hill_encrypt("HELLO", [[1, 2], [2, 4]])  # Singular matrix
        print("ERROR: Should have raised ValueError for singular matrix")
    except ValueError as e:
        print(f"✓ Correctly caught singular matrix error: {e}")
    
    print()


if __name__ == "__main__":
    print("Polygraphic Substitution Ciphers Demo")
    print("=" * 50)
    print()
    
    demonstrate_playfair()
    demonstrate_two_square()
    demonstrate_four_square()
    demonstrate_hill()
    demonstrate_hill_3x3()
    demonstrate_security_comparison()
    demonstrate_error_handling()
    
    print("Demo completed!")
