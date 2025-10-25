"""
Example demonstrating fractionated substitution ciphers.

This example shows how Bifid and Trifid ciphers work with their fractionation
techniques, and how they can use custom alphabets for enhanced security.
"""

import sys
import os

# Add the parent directory to the path so we can import cryptology
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cryptology.classical.substitution.fractionated import bifid_encrypt, bifid_decrypt, trifid_encrypt, trifid_decrypt


def demonstrate_bifid_cipher():
    """Demonstrate the Bifid cipher with English alphabet."""
    print("=== Bifid Cipher Demo ===")
    
    plaintext = "HELLO WORLD"
    key = "MONARCHY"
    
    print(f"Plaintext: {plaintext}")
    print(f"Key: {key}")
    print()
    
    # Encrypt
    encrypted = bifid_encrypt(plaintext, key)
    print(f"Encrypted: {encrypted}")
    
    # Decrypt
    decrypted = bifid_decrypt(encrypted, key)
    print(f"Decrypted: {decrypted}")
    print()


def demonstrate_trifid_cipher():
    """Demonstrate the Trifid cipher with English alphabet."""
    print("=== Trifid Cipher Demo ===")
    
    plaintext = "HELLO WORLD"
    key = "MONARCHY"
    
    print(f"Plaintext: {plaintext}")
    print(f"Key: {key}")
    print()
    
    # Encrypt
    encrypted = trifid_encrypt(plaintext, key)
    print(f"Encrypted: {encrypted}")
    
    # Decrypt
    decrypted = trifid_decrypt(encrypted, key)
    print(f"Decrypted: {decrypted}")
    print()


def demonstrate_bifid_with_custom_alphabet():
    """Demonstrate Bifid cipher with Turkish alphabet."""
    print("=== Bifid Cipher with Turkish Alphabet ===")
    
    plaintext = "MERHABA DÜNYA"
    key = "GİZLİ"
    turkish_alphabet = "ABCÇDEFGĞHIJKLMNOÖPRSŞTUÜVYZ"
    
    print(f"Plaintext: {plaintext}")
    print(f"Key: {key}")
    print(f"Turkish alphabet: {turkish_alphabet}")
    print()
    
    # Encrypt
    encrypted = bifid_encrypt(plaintext, key, turkish_alphabet)
    print(f"Encrypted: {encrypted}")
    
    # Decrypt
    decrypted = bifid_decrypt(encrypted, key, turkish_alphabet)
    print(f"Decrypted: {decrypted}")
    print()


def demonstrate_trifid_with_custom_alphabet():
    """Demonstrate Trifid cipher with Turkish alphabet."""
    print("=== Trifid Cipher with Turkish Alphabet ===")
    
    plaintext = "MERHABA DÜNYA"
    key = "GİZLİ"
    turkish_alphabet = "ABCÇDEFGĞHIJKLMNOÖPRSŞTUÜVYZ"
    
    print(f"Plaintext: {plaintext}")
    print(f"Key: {key}")
    print(f"Turkish alphabet: {turkish_alphabet}")
    print()
    
    # Encrypt
    encrypted = trifid_encrypt(plaintext, key, turkish_alphabet)
    print(f"Encrypted: {encrypted}")
    
    # Decrypt
    decrypted = trifid_decrypt(encrypted, key, turkish_alphabet)
    print(f"Decrypted: {decrypted}")
    print()


def demonstrate_fractionation_technique():
    """Demonstrate how fractionation works in Bifid cipher."""
    print("=== Fractionation Technique Explanation ===")
    
    plaintext = "HELLO"
    key = "MONARCHY"
    
    print(f"Plaintext: {plaintext}")
    print(f"Key: {key}")
    print()
    
    print("Step 1: Create 5x5 Polybius square")
    print("M O N A R")
    print("C H Y B D")
    print("E F G I J")
    print("K L P S T")
    print("U V W X Z")
    print()
    
    print("Step 2: Convert each letter to coordinates")
    print("H -> (1,2), E -> (2,0), L -> (3,1), L -> (3,1), O -> (0,1)")
    print("Rows: [1, 2, 3, 3, 0]")
    print("Cols: [2, 0, 1, 1, 1]")
    print()
    
    print("Step 3: Fractionation - write all rows, then all columns")
    print("Fractionated: [1, 2, 3, 3, 0, 2, 0, 1, 1, 1]")
    print()
    
    print("Step 4: Read pairs of coordinates to get new letters")
    print("(1,2) -> H, (3,0) -> K, (0,1) -> O, (1,1) -> H")
    print()
    
    # Actual encryption
    encrypted = bifid_encrypt(plaintext, key)
    print(f"Actual result: {encrypted}")
    print()


def demonstrate_trifid_fractionation():
    """Demonstrate how fractionation works in Trifid cipher."""
    print("=== Trifid Fractionation Technique ===")
    
    plaintext = "HELLO"
    key = "MONARCHY"
    
    print(f"Plaintext: {plaintext}")
    print(f"Key: {key}")
    print()
    
    print("Step 1: Create 3x3x3 Trifid cube")
    print("Layer 0:    Layer 1:    Layer 2:")
    print("M O N       P Q R       X Y Z")
    print("A B C       D E F       G H I")
    print("J K L       S T U       V W X")
    print()
    
    print("Step 2: Convert each letter to 3D coordinates")
    print("H -> (0,1,1), E -> (1,1,1), L -> (0,2,2), L -> (0,2,2), O -> (0,0,1)")
    print("Layers: [0, 1, 0, 0, 0]")
    print("Rows:   [1, 1, 2, 2, 0]")
    print("Cols:   [1, 1, 2, 2, 1]")
    print()
    
    print("Step 3: Fractionation - write all layers, then all rows, then all columns")
    print("Fractionated: [0, 1, 0, 0, 0, 1, 1, 2, 2, 0, 1, 1, 2, 2, 1]")
    print()
    
    print("Step 4: Read triplets of coordinates to get new letters")
    print("(0,1,1) -> B, (0,0,1) -> O, (1,2,2) -> U")
    print()
    
    # Actual encryption
    encrypted = trifid_encrypt(plaintext, key)
    print(f"Actual result: {encrypted}")
    print()


def demonstrate_security_benefits():
    """Demonstrate security benefits of fractionated ciphers."""
    print("=== Security Benefits of Fractionated Ciphers ===")
    
    plaintext = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
    key = "SECRET"
    
    print(f"Plaintext: {plaintext}")
    print(f"Key: {key}")
    print()
    
    # Bifid encryption
    bifid_encrypted = bifid_encrypt(plaintext, key)
    print(f"Bifid encrypted: {bifid_encrypted}")
    
    # Trifid encryption
    trifid_encrypted = trifid_encrypt(plaintext, key)
    print(f"Trifid encrypted: {trifid_encrypted}")
    print()
    
    print("Security Benefits:")
    print("1. Fractionation breaks letter frequency patterns")
    print("2. Each letter affects multiple positions in ciphertext")
    print("3. Trifid provides 3D fractionation (even more secure)")
    print("4. Custom alphabets add another layer of security")
    print("5. Resistant to frequency analysis attacks")
    print()


def demonstrate_composable_system():
    """Demonstrate fractionated ciphers with monoalphabetic-produced alphabets."""
    print("=== Composable System: Monoalphabetic + Fractionated ===")
    
    from cryptology.classical.substitution.monoalphabetic.caesar import produce_alphabet as caesar_produce
    from cryptology.classical.substitution.monoalphabetic.keyword import produce_alphabet as keyword_produce
    
    plaintext = "COMPOSABLE CIPHER SYSTEM"
    key = "FRACTIONATED"
    
    print(f"Plaintext: {plaintext}")
    print(f"Fractionated key: {key}")
    print()
    
    # Layer 1: Caesar-produced alphabet
    caesar_alphabet = caesar_produce(shift=5)
    print(f"Caesar-produced alphabet: {caesar_alphabet}")
    
    # Layer 2: Use Caesar alphabet with Bifid
    bifid_encrypted = bifid_encrypt(plaintext, key, caesar_alphabet)
    print(f"Bifid with Caesar alphabet: {bifid_encrypted}")
    
    # Layer 3: Keyword-produced alphabet
    keyword_alphabet = keyword_produce("SECRET", caesar_alphabet)
    print(f"Keyword-produced alphabet: {keyword_alphabet}")
    
    # Layer 4: Use keyword alphabet with Trifid
    trifid_encrypted = trifid_encrypt(plaintext, key, keyword_alphabet)
    print(f"Trifid with keyword alphabet: {trifid_encrypted}")
    print()
    
    print("Multi-layer encryption provides:")
    print("1. Caesar shift adds basic substitution")
    print("2. Keyword rearrangement adds complexity")
    print("3. Bifid fractionation breaks patterns")
    print("4. Trifid 3D fractionation adds maximum security")
    print()


if __name__ == "__main__":
    print("Fractionated Substitution Ciphers Demo")
    print("=" * 50)
    print()
    
    demonstrate_bifid_cipher()
    demonstrate_trifid_cipher()
    demonstrate_bifid_with_custom_alphabet()
    demonstrate_trifid_with_custom_alphabet()
    demonstrate_fractionation_technique()
    demonstrate_trifid_fractionation()
    demonstrate_security_benefits()
    demonstrate_composable_system()
    
    print("Demo completed!")
    print()
    print("Key Features:")
    print("1. Bifid: 2D fractionation with 5x5 square")
    print("2. Trifid: 3D fractionation with 3x3x3 cube")
    print("3. Custom alphabet support for any language")
    print("4. Composable with monoalphabetic ciphers")
    print("5. Enhanced security through fractionation")
