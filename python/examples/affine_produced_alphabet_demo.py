"""
Demonstration of using Affine cipher to produce alphabets for polygraphic ciphers.

This shows how we can use Affine(a=3, b=5) to transform the base alphabet,
then use that transformed alphabet with polygraphic ciphers.
"""

import sys
import os

# Add the parent directory to the path so we can import cryptology
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cryptology.classical.substitution.monoalphabetic.affine import produce_alphabet as affine_produce
from cryptology.classical.substitution.monoalphabetic.caesar import produce_alphabet as caesar_produce
from cryptology.classical.substitution.monoalphabetic.keyword import produce_alphabet as keyword_produce
from cryptology.classical.substitution.polygraphic.playfair import encrypt as playfair_encrypt, decrypt as playfair_decrypt
from cryptology.classical.substitution.polygraphic.two_square import encrypt as two_square_encrypt, decrypt as two_square_decrypt


def demonstrate_affine_produced_alphabet():
    """Demonstrate using Affine cipher to produce alphabets."""
    print("=== Affine-Produced Alphabet for Polygraphic Ciphers ===")
    
    base_alphabet = "abcdefghijklmnopqrstuvwxyz"
    a, b = 3, 5  # Affine parameters
    
    print(f"Base alphabet: {base_alphabet}")
    print(f"Affine parameters: a={a}, b={b}")
    print()
    
    # Step 1: Produce Affine-transformed alphabet
    affine_alphabet = affine_produce(a, b, base_alphabet)
    print(f"Affine-produced alphabet: {affine_alphabet}")
    print(f"Size: {len(affine_alphabet)} letters")
    print()
    
    # Step 2: Use with Playfair
    plaintext = "HELLO WORLD"
    key = "MONARCHY"
    
    print(f"Plaintext: {plaintext}")
    print(f"Playfair key: {key}")
    print()
    
    try:
        encrypted = playfair_encrypt(plaintext, key, affine_alphabet)
        decrypted = playfair_decrypt(encrypted, key, affine_alphabet)
        
        print(f"Encrypted: {encrypted}")
        print(f"Decrypted: {decrypted}")
        print()
    except Exception as e:
        print(f"Error: {e}")
        print()
    
    # Step 3: Use with Two Square
    key1 = "SECRET"
    key2 = "PLAYFAIR"
    
    print(f"Two Square keys: {key1}, {key2}")
    
    try:
        encrypted = two_square_encrypt(plaintext, key1, key2, affine_alphabet, affine_alphabet)
        decrypted = two_square_decrypt(encrypted, key1, key2, affine_alphabet, affine_alphabet)
        
        print(f"Encrypted: {encrypted}")
        print(f"Decrypted: {decrypted}")
        print()
    except Exception as e:
        print(f"Error: {e}")
        print()


def demonstrate_different_affine_parameters():
    """Demonstrate different Affine parameters producing different alphabets."""
    print("=== Different Affine Parameters ===")
    
    base_alphabet = "abcdefghijklmnopqrstuvwxyz"
    
    affine_params = [
        (3, 5),   # Original example
        (5, 8),   # Different parameters
        (7, 13),  # Another set
        (11, 17)  # Yet another set
    ]
    
    for a, b in affine_params:
        try:
            affine_alphabet = affine_produce(a, b, base_alphabet)
            print(f"Affine(a={a}, b={b}): {affine_alphabet}")
            print(f"Size: {len(affine_alphabet)} letters")
            print()
        except ValueError as e:
            print(f"Affine(a={a}, b={b}): Error - {e}")
            print()


def demonstrate_mixed_cipher_alphabets():
    """Demonstrate using different monoalphabetic ciphers to produce alphabets."""
    print("=== Mixed Cipher Alphabets ===")
    
    base_alphabet = "abcdefghijklmnopqrstuvwxyz"
    plaintext = "HELLO WORLD"
    key = "MONARCHY"
    
    print(f"Base alphabet: {base_alphabet}")
    print(f"Plaintext: {plaintext}")
    print(f"Key: {key}")
    print()
    
    # Different monoalphabetic ciphers
    cipher_alphabets = {
        "Caesar(shift=5)": caesar_produce(5, base_alphabet),
        "Affine(a=3, b=5)": affine_produce(3, 5, base_alphabet),
        "Affine(a=5, b=8)": affine_produce(5, 8, base_alphabet),
        "Keyword(SECRET)": keyword_produce("SECRET", base_alphabet),
        "Keyword(PLAYFAIR)": keyword_produce("PLAYFAIR", base_alphabet)
    }
    
    for cipher_name, alphabet in cipher_alphabets.items():
        print(f"{cipher_name}:")
        print(f"  Alphabet: {alphabet}")
        print(f"  Size: {len(alphabet)} letters")
        
        try:
            encrypted = playfair_encrypt(plaintext, key, alphabet)
            print(f"  Encrypted: {encrypted}")
        except Exception as e:
            print(f"  Error: {e}")
        print()


def demonstrate_affine_with_custom_languages():
    """Demonstrate Affine-produced alphabets with custom languages."""
    print("=== Affine with Custom Languages ===")
    
    # Turkish alphabet
    turkish_alphabet = "abcçdefgğhıijklmnoöprsştuüvyz"
    print(f"Turkish alphabet: {turkish_alphabet}")
    print(f"Size: {len(turkish_alphabet)} letters")
    print()
    
    # Apply Affine transformation to Turkish
    try:
        affine_turkish = affine_produce(3, 5, turkish_alphabet)
        print(f"Affine-transformed Turkish: {affine_turkish}")
        print(f"Size: {len(affine_turkish)} letters")
        print()
        
        # Use with Playfair
        plaintext = "merhaba dünya"
        key = "gizli"
        
        print(f"Plaintext: {plaintext}")
        print(f"Key: {key}")
        
        encrypted = playfair_encrypt(plaintext, key, affine_turkish)
        decrypted = playfair_decrypt(encrypted, key, affine_turkish)
        
        print(f"Encrypted: {encrypted}")
        print(f"Decrypted: {decrypted}")
        print()
        
    except Exception as e:
        print(f"Error: {e}")
        print()


def demonstrate_alphabet_analysis():
    """Analyze how different Affine parameters affect the alphabet."""
    print("=== Affine Alphabet Analysis ===")
    
    base_alphabet = "abcdefghijklmnopqrstuvwxyz"
    
    print(f"Base alphabet: {base_alphabet}")
    print()
    
    # Test different Affine parameters
    test_params = [
        (1, 0),   # Identity (no change)
        (1, 3),   # Caesar shift of 3
        (3, 5),   # Affine transformation
        (5, 8),   # Different Affine
        (7, 13)   # Another Affine
    ]
    
    for a, b in test_params:
        try:
            affine_alphabet = affine_produce(a, b, base_alphabet)
            print(f"Affine(a={a}, b={b}): {affine_alphabet}")
            
            # Check if it's a permutation
            if sorted(affine_alphabet) == sorted(base_alphabet):
                print("  ✓ Valid permutation")
            else:
                print("  ✗ Not a valid permutation")
            print()
            
        except ValueError as e:
            print(f"Affine(a={a}, b={b}): Error - {e}")
            print()


def demonstrate_security_benefits():
    """Demonstrate security benefits of using Affine-produced alphabets."""
    print("=== Security Benefits ===")
    
    base_alphabet = "abcdefghijklmnopqrstuvwxyz"
    plaintext = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
    key = "MONARCHY"
    
    print(f"Plaintext: {plaintext}")
    print(f"Key: {key}")
    print()
    
    # Compare different approaches
    approaches = {
        "Standard Playfair": (base_alphabet, "Standard English alphabet"),
        "Caesar-Produced": (caesar_produce(5, base_alphabet), "Caesar-shifted alphabet"),
        "Affine-Produced": (affine_produce(3, 5, base_alphabet), "Affine-transformed alphabet"),
        "Keyword-Produced": (keyword_produce("SECRET", base_alphabet), "Keyword-based alphabet")
    }
    
    for approach_name, (alphabet, description) in approaches.items():
        print(f"{approach_name}:")
        print(f"  Description: {description}")
        print(f"  Alphabet: {alphabet}")
        
        try:
            encrypted = playfair_encrypt(plaintext, key, alphabet)
            print(f"  Encrypted: {encrypted}")
            print(f"  Length: {len(encrypted)} characters")
        except Exception as e:
            print(f"  Error: {e}")
        print()
    
    print("Security Benefits:")
    print("1. Additional layer of encryption")
    print("2. Custom alphabet makes frequency analysis harder")
    print("3. Composable with any monoalphabetic cipher")
    print("4. Maintains polygraphic cipher security")
    print("5. Flexible key space expansion")


if __name__ == "__main__":
    print("Affine-Produced Alphabet Demo")
    print("=" * 40)
    print()
    
    demonstrate_affine_produced_alphabet()
    demonstrate_different_affine_parameters()
    demonstrate_mixed_cipher_alphabets()
    demonstrate_affine_with_custom_languages()
    demonstrate_alphabet_analysis()
    demonstrate_security_benefits()
    
    print("Demo completed!")
    print()
    print("Key Insight: Any monoalphabetic cipher can produce an alphabet")
    print("that can then be used with polygraphic ciphers for enhanced security!")
