#!/usr/bin/env python3
"""
Example demonstrating Chaocipher integration with monoalphabetic ciphers.

This example shows how to create Chaocipher alphabets using various
monoalphabetic substitution ciphers for enhanced security.
"""

from cryptology.classical.substitution.polyalphabetic.chaocipher import (
    create_alphabets_with_mono_ciphers, encrypt, decrypt
)


def demonstrate_mono_cipher_combinations():
    """Demonstrate various combinations of monoalphabetic ciphers."""
    print("=== Chaocipher with Monoalphabetic Cipher Integration ===\n")
    
    plaintext = "HELLO WORLD"
    print(f"Plaintext: {plaintext}\n")
    
    # Test different combinations
    combinations = [
        {
            "name": "Caesar + Keyword",
            "left_cipher": "caesar", "left_params": {"shift": 5},
            "right_cipher": "keyword", "right_params": {"keyword": "SECRET"}
        },
        {
            "name": "Atbash + Affine",
            "left_cipher": "atbash", "left_params": {},
            "right_cipher": "affine", "right_params": {"a": 5, "b": 7}
        },
        {
            "name": "Keyword + Caesar",
            "left_cipher": "keyword", "left_params": {"keyword": "HELLO"},
            "right_cipher": "caesar", "right_params": {"shift": 13}
        },
        {
            "name": "Affine + Keyword",
            "left_cipher": "affine", "left_params": {"a": 7, "b": 3},
            "right_cipher": "keyword", "right_params": {"keyword": "WORLD"}
        }
    ]
    
    for i, combo in enumerate(combinations, 1):
        print(f"{i}. {combo['name']} Combination")
        print("=" * 50)
        
        # Create alphabets using monoalphabetic ciphers
        left_alphabet, right_alphabet = create_alphabets_with_mono_ciphers(
            left_cipher=combo["left_cipher"], left_params=combo["left_params"],
            right_cipher=combo["right_cipher"], right_params=combo["right_params"]
        )
        
        # Show alphabet details
        print(f"Left alphabet ({combo['left_cipher']}): {''.join(left_alphabet[:10])}...")
        print(f"Right alphabet ({combo['right_cipher']}): {''.join(right_alphabet[:10])}...")
        
        # Encrypt and decrypt
        encrypted = encrypt(plaintext, left_alphabet, right_alphabet)
        decrypted = decrypt(encrypted, left_alphabet, right_alphabet)
        
        print(f"Encrypted: {encrypted}")
        print(f"Decrypted: {decrypted}")
        print(f"Success: {'✓' if plaintext == decrypted else '✗'}")
        print()


def demonstrate_custom_alphabet():
    """Demonstrate using custom base alphabet."""
    print("5. Custom Base Alphabet")
    print("=" * 50)
    
    # Use only letters (no space) for a 26-character alphabet
    custom_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    left_alphabet, right_alphabet = create_alphabets_with_mono_ciphers(
        left_cipher="caesar", left_params={"shift": 3},
        right_cipher="atbash",
        alphabet=custom_alphabet
    )
    
    print(f"Custom alphabet: {custom_alphabet}")
    print(f"Left alphabet (Caesar shift=3): {''.join(left_alphabet)}")
    print(f"Right alphabet (Atbash): {''.join(right_alphabet)}")
    
    plaintext = "HELLO"
    encrypted = encrypt(plaintext, left_alphabet, right_alphabet)
    decrypted = decrypt(encrypted, left_alphabet, right_alphabet)
    
    print(f"Plaintext: {plaintext}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
    print(f"Success: {'✓' if plaintext == decrypted else '✗'}")
    print()


def demonstrate_error_handling():
    """Demonstrate error handling for invalid parameters."""
    print("6. Error Handling")
    print("=" * 50)
    
    # Test invalid cipher name
    try:
        create_alphabets_with_mono_ciphers(
            left_cipher="invalid", left_params={},
            right_cipher="caesar", right_params={"shift": 3}
        )
    except ValueError as e:
        print(f"Invalid cipher name error: {e}")
    
    # Test Affine cipher with non-coprime 'a'
    try:
        create_alphabets_with_mono_ciphers(
            left_cipher="affine", left_params={"a": 3, "b": 5},  # 3 not coprime with 27
            right_cipher="caesar", right_params={"shift": 3}
        )
    except ValueError as e:
        print(f"Affine coprime error: {e}")
    
    print()


if __name__ == "__main__":
    demonstrate_mono_cipher_combinations()
    demonstrate_custom_alphabet()
    demonstrate_error_handling()
    
    print("=== Example completed successfully! ===")
