"""
Example demonstrating the Alberti cipher.

This example shows how the Alberti cipher works with its rotating disk system,
various rotation strategies, and integration with the composable cipher system.
"""

import sys
import os

# Add the parent directory to the path so we can import cryptology
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cryptology.classical.substitution.polyalphabetic import alberti_encrypt, alberti_decrypt
from cryptology.classical.substitution.monoalphabetic.caesar import produce_alphabet as caesar_produce
from cryptology.classical.substitution.monoalphabetic.keyword import produce_alphabet as keyword_produce


def demonstrate_basic_alberti():
    """Demonstrate basic Alberti cipher with simple rotation strategy."""
    print("=== Basic Alberti Cipher Demo ===")
    
    plaintext = "HELLO WORLD"
    rotation_strategy = "every_3"
    initial_position = 0
    rotation_amount = 1
    
    print(f"Plaintext: {plaintext}")
    print(f"Rotation strategy: {rotation_strategy}")
    print(f"Initial position: {initial_position}")
    print(f"Rotation amount: {rotation_amount}")
    print()
    
    # Encrypt
    encrypted = alberti_encrypt(plaintext, 
                               rotation_strategy=rotation_strategy,
                               initial_position=initial_position,
                               rotation_amount=rotation_amount)
    print(f"Encrypted: {encrypted}")
    
    # Decrypt
    decrypted = alberti_decrypt(encrypted,
                               rotation_strategy=rotation_strategy,
                               initial_position=initial_position,
                               rotation_amount=rotation_amount)
    print(f"Decrypted: {decrypted}")
    print()


def demonstrate_rotation_strategies():
    """Demonstrate different rotation strategies."""
    print("=== Rotation Strategies Demo ===")
    
    plaintext = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
    
    strategies = [
        "every_3",
        "every_5", 
        "on_vowel",
        "on_space",
        "on_consonant",
        "fibonacci"
    ]
    
    print(f"Plaintext: {plaintext}")
    print()
    
    for strategy in strategies:
        try:
            encrypted = alberti_encrypt(plaintext, rotation_strategy=strategy)
            decrypted = alberti_decrypt(encrypted, rotation_strategy=strategy)
            
            print(f"Strategy: {strategy}")
            print(f"Encrypted: {encrypted}")
            print(f"Decrypted: {decrypted}")
            print(f"Success: {'✓' if decrypted == plaintext.replace(' ', '') else '✗'}")
            print()
        except Exception as e:
            print(f"Strategy: {strategy} - Error: {e}")
            print()


def demonstrate_custom_alphabets():
    """Demonstrate Alberti cipher with custom alphabets."""
    print("=== Custom Alphabets Demo ===")
    
    plaintext = "HELLO WORLD"
    outer_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    inner_alphabet = "ZYXWVUTSRQPONMLKJIHGFEDCBA"  # Reversed alphabet
    rotation_strategy = "every_2"
    
    print(f"Plaintext: {plaintext}")
    print(f"Outer alphabet: {outer_alphabet}")
    print(f"Inner alphabet: {inner_alphabet}")
    print(f"Rotation strategy: {rotation_strategy}")
    print()
    
    # Encrypt
    encrypted = alberti_encrypt(plaintext,
                               outer_alphabet=outer_alphabet,
                               inner_alphabet=inner_alphabet,
                               rotation_strategy=rotation_strategy)
    print(f"Encrypted: {encrypted}")
    
    # Decrypt
    decrypted = alberti_decrypt(encrypted,
                               outer_alphabet=outer_alphabet,
                               inner_alphabet=inner_alphabet,
                               rotation_strategy=rotation_strategy)
    print(f"Decrypted: {decrypted}")
    print()


def demonstrate_turkish_alphabet():
    """Demonstrate Alberti cipher with Turkish alphabet."""
    print("=== Turkish Alphabet Demo ===")
    
    plaintext = "MERHABA DÜNYA"
    turkish_alphabet = "ABCÇDEFGĞHIJKLMNOÖPRSŞTUÜVYZ"
    rotation_strategy = "every_4"
    
    print(f"Plaintext: {plaintext}")
    print(f"Turkish alphabet: {turkish_alphabet}")
    print(f"Rotation strategy: {rotation_strategy}")
    print()
    
    # Encrypt
    encrypted = alberti_encrypt(plaintext,
                               outer_alphabet=turkish_alphabet,
                               rotation_strategy=rotation_strategy)
    print(f"Encrypted: {encrypted}")
    
    # Decrypt
    decrypted = alberti_decrypt(encrypted,
                               outer_alphabet=turkish_alphabet,
                               rotation_strategy=rotation_strategy)
    print(f"Decrypted: {decrypted}")
    print()


def demonstrate_composable_system():
    """Demonstrate Alberti cipher with monoalphabetic-produced alphabets."""
    print("=== Composable System Demo ===")
    
    plaintext = "COMPOSABLE CIPHER SYSTEM"
    
    print(f"Plaintext: {plaintext}")
    print()
    
    # Layer 1: Caesar-produced alphabet
    caesar_alphabet = caesar_produce(shift=5)
    print(f"Caesar-produced alphabet: {caesar_alphabet}")
    
    # Layer 2: Keyword-produced alphabet
    keyword_alphabet = keyword_produce("SECRET", caesar_alphabet)
    print(f"Keyword-produced alphabet: {keyword_alphabet}")
    print()
    
    # Use Caesar alphabet as inner alphabet
    encrypted_caesar = alberti_encrypt(plaintext,
                                      inner_alphabet=caesar_alphabet,
                                      rotation_strategy="every_3")
    print(f"Alberti with Caesar alphabet: {encrypted_caesar}")
    
    # Use keyword alphabet as inner alphabet
    encrypted_keyword = alberti_encrypt(plaintext,
                                      inner_alphabet=keyword_alphabet,
                                      rotation_strategy="fibonacci")
    print(f"Alberti with keyword alphabet: {encrypted_keyword}")
    print()
    
    print("Multi-layer encryption provides:")
    print("1. Caesar shift adds basic substitution")
    print("2. Keyword rearrangement adds complexity")
    print("3. Alberti rotation adds polyalphabetic security")
    print("4. Multiple rotation strategies add unpredictability")
    print()


def demonstrate_complex_patterns():
    """Demonstrate Alberti cipher with complex rotation patterns."""
    print("=== Complex Rotation Patterns Demo ===")
    
    plaintext = "HELLO WORLD"
    
    # User-defined pattern
    custom_pattern = [2, 3, 1, 4]  # Rotate after 2, 3, 1, 4 letters (repeating)
    
    print(f"Plaintext: {plaintext}")
    print(f"Custom pattern: {custom_pattern}")
    print()
    
    try:
        encrypted = alberti_encrypt(plaintext, rotation_strategy=custom_pattern)
        decrypted = alberti_decrypt(encrypted, rotation_strategy=custom_pattern)
        
        print(f"Encrypted: {encrypted}")
        print(f"Decrypted: {decrypted}")
        print(f"Success: {'✓' if decrypted == plaintext.replace(' ', '') else '✗'}")
    except Exception as e:
        print(f"Error: {e}")
    print()


def demonstrate_historical_context():
    """Demonstrate the historical significance of Alberti cipher."""
    print("=== Historical Context ===")
    
    plaintext = "HISTORICAL CIPHER"
    
    print("The Alberti cipher was invented by Leon Battista Alberti in 1467.")
    print("It was the FIRST polyalphabetic cipher in history!")
    print("This revolutionized cryptography by introducing the concept of")
    print("using multiple alphabets for encryption.")
    print()
    
    print(f"Plaintext: {plaintext}")
    
    # Simulate historical usage with simple rotation
    encrypted = alberti_encrypt(plaintext,
                               rotation_strategy="every_5",
                               initial_position=3,
                               rotation_amount=2)
    
    print(f"Encrypted (historical style): {encrypted}")
    print()
    
    print("Key innovations of Alberti cipher:")
    print("1. First polyalphabetic substitution")
    print("2. Rotating disk mechanism")
    print("3. Multiple alphabet concept")
    print("4. Foundation for all later polyalphabetic ciphers")
    print("5. Revolutionary security improvement over monoalphabetic ciphers")
    print()


def demonstrate_security_analysis():
    """Demonstrate security benefits of Alberti cipher."""
    print("=== Security Analysis ===")
    
    plaintext = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
    
    print(f"Plaintext: {plaintext}")
    print()
    
    # Different rotation strategies
    strategies = ["every_3", "every_5", "on_vowel", "fibonacci"]
    
    print("Security benefits of different rotation strategies:")
    print()
    
    for strategy in strategies:
        encrypted = alberti_encrypt(plaintext, rotation_strategy=strategy)
        
        print(f"Strategy: {strategy}")
        print(f"Encrypted: {encrypted}")
        
        # Analyze letter frequency
        freq = {}
        for char in encrypted:
            freq[char] = freq.get(char, 0) + 1
        
        # Show most frequent letters
        sorted_freq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
        top_letters = [f"{char}:{count}" for char, count in sorted_freq[:5]]
        
        print(f"Top letters: {', '.join(top_letters)}")
        print()
    
    print("Security advantages:")
    print("1. Multiple alphabets break frequency analysis")
    print("2. Rotation strategies add unpredictability")
    print("3. Custom alphabets provide additional security")
    print("4. Composable with other cipher systems")
    print("5. Resistant to simple substitution attacks")
    print()


if __name__ == "__main__":
    print("Alberti Cipher Demo")
    print("==================")
    print()
    
    demonstrate_basic_alberti()
    demonstrate_rotation_strategies()
    demonstrate_custom_alphabets()
    demonstrate_turkish_alphabet()
    demonstrate_composable_system()
    demonstrate_complex_patterns()
    demonstrate_historical_context()
    demonstrate_security_analysis()
    
    print("Demo completed!")
    print()
    print("Key Features:")
    print("1. First polyalphabetic cipher in history")
    print("2. Rotating disk mechanism with multiple strategies")
    print("3. Custom alphabet support for any language")
    print("4. Composable with monoalphabetic ciphers")
    print("5. Complex rotation patterns for enhanced security")
    print("6. Deterministic scrambled alphabet generation")
    print("7. Integration with existing cipher systems")
