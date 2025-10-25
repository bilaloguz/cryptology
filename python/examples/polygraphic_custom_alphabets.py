"""
Example demonstrating polygraphic substitution ciphers with custom alphabets.

This example shows how to use Playfair, Two Square, Four Square, and Hill ciphers
with different alphabets including Turkish, Russian, and "Caesared" alphabets.
"""

import sys
import os

# Add the parent directory to the path so we can import cryptology
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cryptology.classical.substitution.polygraphic.playfair import encrypt as playfair_encrypt, decrypt as playfair_decrypt
from cryptology.classical.substitution.polygraphic.two_square import encrypt as two_square_encrypt, decrypt as two_square_decrypt
from cryptology.classical.substitution.polygraphic.four_square import encrypt as four_square_encrypt, decrypt as four_square_decrypt
from cryptology.classical.substitution.polygraphic.hill import encrypt as hill_encrypt, decrypt as hill_decrypt
from cryptology.classical.substitution.polygraphic.alphabet_utils import (
    create_caesared_alphabet, detect_language, get_letter_combination_rules
)


def demonstrate_turkish_alphabet():
    """Demonstrate polygraphic ciphers with Turkish alphabet."""
    print("=== Turkish Alphabet Support ===")
    
    # Turkish alphabet (29 letters)
    turkish_alphabet = "abcçdefgğhıijklmnoöprsştuüvyz"
    plaintext = "merhaba dünya"
    key = "gizli"
    
    print(f"Turkish Alphabet: {turkish_alphabet}")
    print(f"Plaintext: {plaintext}")
    print(f"Key: {key}")
    print(f"Detected Language: {detect_language(turkish_alphabet)}")
    
    # Show letter combination rules
    rules = get_letter_combination_rules()
    print(f"Combination Rules: {rules['turkish']}")
    print()
    
    # Playfair with Turkish
    try:
        encrypted = playfair_encrypt(plaintext, key, turkish_alphabet)
        decrypted = playfair_decrypt(encrypted, key, turkish_alphabet)
        print(f"Playfair Encrypted: {encrypted}")
        print(f"Playfair Decrypted: {decrypted}")
    except Exception as e:
        print(f"Playfair Error: {e}")
    
    print()


def demonstrate_russian_alphabet():
    """Demonstrate polygraphic ciphers with Russian alphabet."""
    print("=== Russian Alphabet Support ===")
    
    # Russian alphabet (33 letters)
    russian_alphabet = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
    plaintext = "привет мир"
    key = "секрет"
    
    print(f"Russian Alphabet: {russian_alphabet}")
    print(f"Plaintext: {plaintext}")
    print(f"Key: {key}")
    print(f"Detected Language: {detect_language(russian_alphabet)}")
    
    # Show letter combination rules
    rules = get_letter_combination_rules()
    print(f"Combination Rules: {rules['russian']}")
    print()
    
    # Playfair with Russian
    try:
        encrypted = playfair_encrypt(plaintext, key, russian_alphabet)
        decrypted = playfair_decrypt(encrypted, key, russian_alphabet)
        print(f"Playfair Encrypted: {encrypted}")
        print(f"Playfair Decrypted: {decrypted}")
    except Exception as e:
        print(f"Playfair Error: {e}")
    
    print()


def demonstrate_caesared_alphabet():
    """Demonstrate polygraphic ciphers with 'Caesared' alphabet."""
    print("=== Caesared Alphabet Support ===")
    
    # Create a Caesared alphabet (shifted by 3)
    base_alphabet = "abcdefghijklmnopqrstuvwxyz"
    caesared_alphabet = create_caesared_alphabet(base_alphabet, 3)
    
    plaintext = "hello world"
    key = "secret"
    
    print(f"Base Alphabet: {base_alphabet}")
    print(f"Caesared Alphabet (shift=3): {caesared_alphabet}")
    print(f"Plaintext: {plaintext}")
    print(f"Key: {key}")
    print()
    
    # Playfair with Caesared alphabet
    try:
        encrypted = playfair_encrypt(plaintext, key, caesared_alphabet)
        decrypted = playfair_decrypt(encrypted, key, caesared_alphabet)
        print(f"Playfair Encrypted: {encrypted}")
        print(f"Playfair Decrypted: {decrypted}")
    except Exception as e:
        print(f"Playfair Error: {e}")
    
    print()


def demonstrate_different_square_sizes():
    """Demonstrate different square sizes for different alphabets."""
    print("=== Different Square Sizes ===")
    
    from cryptology.classical.substitution.polygraphic.alphabet_utils import get_square_size
    
    alphabets = {
        "English": "abcdefghijklmnopqrstuvwxyz",
        "Turkish": "abcçdefgğhıijklmnoöprsştuüvyz",
        "Russian": "абвгдежзийклмнопрстуфхцчшщъыьэюя",
        "Digits": "0123456789",
        "Hex": "0123456789abcdef"
    }
    
    for name, alphabet in alphabets.items():
        square_size = get_square_size(len(alphabet))
        print(f"{name}: {len(alphabet)} letters → {square_size}×{square_size} square")
    
    print()


def demonstrate_hill_with_custom_alphabet():
    """Demonstrate Hill cipher with custom alphabet."""
    print("=== Hill Cipher with Custom Alphabet ===")
    
    # Hill cipher works with any alphabet size
    plaintext = "hello world"
    key_matrix = [[3, 3], [2, 5]]
    
    print(f"Plaintext: {plaintext}")
    print(f"Key Matrix: {key_matrix}")
    
    try:
        encrypted = hill_encrypt(plaintext, key_matrix)
        decrypted = hill_decrypt(encrypted, key_matrix)
        print(f"Hill Encrypted: {encrypted}")
        print(f"Hill Decrypted: {decrypted}")
    except Exception as e:
        print(f"Hill Error: {e}")
    
    print()


def demonstrate_alphabet_combination_rules():
    """Demonstrate how different languages handle letter combinations."""
    print("=== Alphabet Combination Rules ===")
    
    from cryptology.classical.substitution.polygraphic.alphabet_utils import combine_similar_letters
    
    test_cases = [
        ("Turkish", "abcçdefgğhıijklmnoöprsştuüvyz"),
        ("Russian", "абвгдежзийклмнопрстуфхцчшщъыьэюя"),
        ("German", "abcdefghijklmnopqrstuvwxyzäöüß"),
        ("English", "abcdefghijklmnopqrstuvwxyz")
    ]
    
    for language, alphabet in test_cases:
        print(f"{language}:")
        print(f"  Original: {alphabet}")
        combined = combine_similar_letters(alphabet)
        print(f"  Combined: {combined}")
        print(f"  Length: {len(combined)}")
        print()


def demonstrate_error_handling():
    """Demonstrate error handling with custom alphabets."""
    print("=== Error Handling ===")
    
    # Test with very short alphabet
    short_alphabet = "abc"
    plaintext = "hello"
    key = "test"
    
    print(f"Short Alphabet: {short_alphabet}")
    print(f"Plaintext: {plaintext}")
    
    try:
        encrypted = playfair_encrypt(plaintext, key, short_alphabet)
        print(f"Encrypted: {encrypted}")
    except Exception as e:
        print(f"Error: {e}")
    
    print()


if __name__ == "__main__":
    print("Polygraphic Substitution Ciphers with Custom Alphabets Demo")
    print("=" * 60)
    print()
    
    demonstrate_turkish_alphabet()
    demonstrate_russian_alphabet()
    demonstrate_caesared_alphabet()
    demonstrate_different_square_sizes()
    demonstrate_hill_with_custom_alphabet()
    demonstrate_alphabet_combination_rules()
    demonstrate_error_handling()
    
    print("Demo completed!")
