"""
Example demonstrating the composable cipher system.

This example shows how monoalphabetic ciphers can produce custom alphabets
that are then used by polygraphic ciphers, creating a powerful composable system.
"""

import sys
import os

# Add the parent directory to the path so we can import cryptology
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import monoalphabetic ciphers
from cryptology.classical.substitution.monoalphabetic.caesar import produce_alphabet as caesar_produce
from cryptology.classical.substitution.monoalphabetic.keyword import produce_alphabet as keyword_produce
from cryptology.classical.substitution.monoalphabetic.affine import produce_alphabet as affine_produce
from cryptology.classical.substitution.monoalphabetic.atbash import produce_alphabet as atbash_produce

# Import polygraphic ciphers
from cryptology.classical.substitution.polygraphic.playfair import encrypt as playfair_encrypt, decrypt as playfair_decrypt
from cryptology.classical.substitution.polygraphic.two_square import encrypt as two_square_encrypt, decrypt as two_square_decrypt
from cryptology.classical.substitution.polygraphic.four_square import encrypt as four_square_encrypt, decrypt as four_square_decrypt
from cryptology.classical.substitution.polygraphic.hill import encrypt as hill_encrypt, decrypt as hill_decrypt


def demonstrate_caesar_playfair():
    """Demonstrate Caesar-produced alphabet with Playfair cipher."""
    print("=== Caesar + Playfair ===")
    
    plaintext = "HELLO WORLD"
    key = "MONARCHY"
    
    # Produce Caesar-shifted alphabet
    caesared_alphabet = caesar_produce(shift=5)
    print(f"Caesar-produced alphabet (shift=5): {caesared_alphabet}")
    print(f"Plaintext: {plaintext}")
    print(f"Playfair key: {key}")
    
    # Use Caesar-produced alphabet with Playfair
    encrypted = playfair_encrypt(plaintext, key, caesared_alphabet)
    decrypted = playfair_decrypt(encrypted, key, caesared_alphabet)
    
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
    print()


def demonstrate_keyword_two_square():
    """Demonstrate Keyword-produced alphabet with Two Square cipher."""
    print("=== Keyword + Two Square ===")
    
    plaintext = "ATTACK AT DAWN"
    keyword1 = "SECRET"
    keyword2 = "PLAYFAIR"
    
    # Produce keyword-based alphabets
    keyword_alphabet1 = keyword_produce(keyword1)
    keyword_alphabet2 = keyword_produce(keyword2)
    
    print(f"Keyword-produced alphabet 1: {keyword_alphabet1}")
    print(f"Keyword-produced alphabet 2: {keyword_alphabet2}")
    print(f"Plaintext: {plaintext}")
    
    # Use keyword-produced alphabets with Two Square
    encrypted = two_square_encrypt(plaintext, keyword1, keyword2, keyword_alphabet1, keyword_alphabet2)
    decrypted = two_square_decrypt(encrypted, keyword1, keyword2, keyword_alphabet1, keyword_alphabet2)
    
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
    print()


def demonstrate_affine_four_square():
    """Demonstrate Affine-produced alphabet with Four Square cipher."""
    print("=== Affine + Four Square ===")
    
    plaintext = "THE QUICK BROWN FOX"
    keys = ["MONARCHY", "PLAYFAIR", "CIPHER", "SECRET"]
    
    # Produce affine-transformed alphabets
    affine_alphabets = []
    for i, key in enumerate(keys):
        a, b = 5 + i, 8 + i  # Different affine parameters
        affine_alphabet = affine_produce(a, b)
        affine_alphabets.append(affine_alphabet)
        print(f"Affine-produced alphabet {i+1} (a={a}, b={b}): {affine_alphabet}")
    
    print(f"Plaintext: {plaintext}")
    
    # Use affine-produced alphabets with Four Square
    encrypted = four_square_encrypt(plaintext, *keys, *affine_alphabets)
    decrypted = four_square_decrypt(encrypted, *keys, *affine_alphabets)
    
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
    print()


def demonstrate_atbash_hill():
    """Demonstrate Atbash-produced alphabet with Hill cipher."""
    print("=== Atbash + Hill ===")
    
    plaintext = "HELLO WORLD"
    hill_matrix = [[3, 3], [2, 5]]
    
    # Produce Atbash-reversed alphabet
    atbash_alphabet = atbash_produce()
    print(f"Atbash-produced alphabet: {atbash_alphabet}")
    print(f"Plaintext: {plaintext}")
    print(f"Hill matrix: {hill_matrix}")
    
    # Use Atbash-produced alphabet with Hill
    encrypted = hill_encrypt(plaintext, hill_matrix)
    decrypted = hill_decrypt(encrypted, hill_matrix)
    
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
    print()


def demonstrate_multi_layer_encryption():
    """Demonstrate multi-layer encryption using different combinations."""
    print("=== Multi-Layer Encryption ===")
    
    plaintext = "SECRET MESSAGE"
    
    # Layer 1: Caesar + Playfair
    caesared_alphabet = caesar_produce(shift=7)
    layer1_encrypted = playfair_encrypt(plaintext, "KEY1", caesared_alphabet)
    
    # Layer 2: Keyword + Two Square
    keyword_alphabet1 = keyword_produce("SECRET")
    keyword_alphabet2 = keyword_produce("KEY2")
    layer2_encrypted = two_square_encrypt(layer1_encrypted, "KEY1", "KEY2", keyword_alphabet1, keyword_alphabet2)
    
    # Layer 3: Affine + Hill
    affine_alphabet = affine_produce(5, 8)
    hill_matrix = [[3, 3], [2, 5]]
    layer3_encrypted = hill_encrypt(layer2_encrypted, hill_matrix)
    
    print(f"Original: {plaintext}")
    print(f"Layer 1 (Caesar+Playfair): {layer1_encrypted}")
    print(f"Layer 2 (Keyword+Two Square): {layer2_encrypted}")
    print(f"Layer 3 (Affine+Hill): {layer3_encrypted}")
    print()


def demonstrate_custom_language_combinations():
    """Demonstrate combinations with custom languages."""
    print("=== Custom Language Combinations ===")
    
    # Turkish alphabet
    turkish_alphabet = "abcçdefgğhıijklmnoöprsştuüvyz"
    plaintext = "merhaba dünya"
    key = "gizli"
    
    # Produce Caesar-shifted Turkish alphabet
    caesared_turkish = caesar_produce(shift=3, alphabet=turkish_alphabet)
    print(f"Turkish alphabet: {turkish_alphabet}")
    print(f"Caesar-shifted Turkish: {caesared_turkish}")
    print(f"Plaintext: {plaintext}")
    
    # Use with Playfair
    try:
        encrypted = playfair_encrypt(plaintext, key, caesared_turkish)
        decrypted = playfair_decrypt(encrypted, key, caesared_turkish)
        print(f"Encrypted: {encrypted}")
        print(f"Decrypted: {decrypted}")
    except Exception as e:
        print(f"Error: {e}")
    
    print()


def demonstrate_alphabet_analysis():
    """Demonstrate analysis of produced alphabets."""
    print("=== Alphabet Analysis ===")
    
    base_alphabet = "abcdefghijklmnopqrstuvwxyz"
    
    # Different Caesar shifts
    for shift in [1, 3, 5, 13]:
        caesared = caesar_produce(shift, base_alphabet)
        print(f"Caesar shift {shift:2d}: {caesared}")
    
    print()
    
    # Different keywords
    keywords = ["SECRET", "PLAYFAIR", "CIPHER"]
    for keyword in keywords:
        keyword_alphabet = keyword_produce(keyword, base_alphabet)
        print(f"Keyword '{keyword}': {keyword_alphabet}")
    
    print()
    
    # Different affine parameters
    affine_params = [(3, 1), (5, 8), (7, 13)]
    for a, b in affine_params:
        try:
            affine_alphabet = affine_produce(a, b, base_alphabet)
            print(f"Affine (a={a}, b={b}): {affine_alphabet}")
        except ValueError as e:
            print(f"Affine (a={a}, b={b}): Error - {e}")
    
    print()


if __name__ == "__main__":
    print("Composable Cipher System Demo")
    print("=" * 50)
    print()
    
    demonstrate_caesar_playfair()
    demonstrate_keyword_two_square()
    demonstrate_affine_four_square()
    demonstrate_atbash_hill()
    demonstrate_multi_layer_encryption()
    demonstrate_custom_language_combinations()
    demonstrate_alphabet_analysis()
    
    print("Demo completed!")
    print()
    print("Key Benefits of Composable System:")
    print("1. Enhanced Security: Multiple layers of encryption")
    print("2. Flexibility: Mix and match different cipher types")
    print("3. Customization: Use any alphabet with any cipher")
    print("4. Educational: Understand how different ciphers interact")
    print("5. Practical: Real-world applications often use multiple ciphers")
