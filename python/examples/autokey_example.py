#!/usr/bin/env python3
"""
Auto-key Cipher Example

This example demonstrates the Auto-key cipher, which automatically extends
the key using the plaintext itself. This makes it more secure than Vigenère
but also more complex.
"""

from cryptology.classical.substitution.polyalphabetic.autokey import (
    encrypt, decrypt, produce_table, generate_random_key, 
    generate_key_for_text, encrypt_with_random_key
)
from cryptology.classical.substitution.monoalphabetic.caesar import produce_alphabet as caesar_produce_alphabet
from cryptology.classical.substitution.monoalphabetic.keyword import produce_alphabet as keyword_produce_alphabet
from cryptology.classical.substitution.monoalphabetic.affine import produce_alphabet as affine_produce_alphabet
from cryptology.classical.substitution.monoalphabetic.atbash import produce_alphabet as atbash_produce_alphabet

def demonstrate_basic_autokey():
    """Demonstrate basic Auto-key encryption/decryption"""
    print("=== Basic Auto-key Encryption/Decryption ===")
    
    plaintext = "HELLO WORLD"
    key = "KEY"
    
    print(f"Plaintext: {plaintext}")
    print(f"Key: {key}")
    
    # Encrypt
    encrypted = encrypt(plaintext, key)
    print(f"Encrypted: {encrypted}")
    
    # Decrypt
    decrypted = decrypt(encrypted, key)
    print(f"Decrypted: {decrypted}")
    print()

def demonstrate_key_extension():
    """Demonstrate Auto-key's key extension mechanism"""
    print("=== Auto-key Key Extension Mechanism ===")
    
    plaintext = "THIS IS A LONG MESSAGE"
    key = "SHORT"
    
    print(f"Plaintext: {plaintext}")
    print(f"Initial Key: {key}")
    print("Note: Key is automatically extended using plaintext")
    
    # Encrypt
    encrypted = encrypt(plaintext, key)
    print(f"Encrypted: {encrypted}")
    
    # Decrypt
    decrypted = decrypt(encrypted, key)
    print(f"Decrypted: {decrypted}")
    print()

def demonstrate_random_key_generation():
    """Demonstrate random key generation"""
    print("=== Auto-key with Random Key Generation ===")
    
    plaintext = "TEST MESSAGE"
    
    print(f"Plaintext: {plaintext}")
    
    # Generate random key
    random_key = generate_random_key(8)
    print(f"Generated Random Key: {random_key}")
    
    # Encrypt with random key
    encrypted = encrypt(plaintext, random_key)
    print(f"Encrypted: {encrypted}")
    
    # Decrypt using generated key
    decrypted = decrypt(encrypted, random_key)
    print(f"Decrypted: {decrypted}")
    print()

def demonstrate_encrypt_with_random_key():
    """Demonstrate encryption with automatic random key generation"""
    print("=== Auto-key Encryption with Random Key ===")
    
    plaintext = "HELLO WORLD"
    
    print(f"Plaintext: {plaintext}")
    
    # Encrypt with random key generation
    encrypted, generated_key = encrypt_with_random_key(plaintext, key_length=5)
    print(f"Generated Key: {generated_key}")
    print(f"Encrypted: {encrypted}")
    
    # Decrypt using generated key
    decrypted = decrypt(encrypted, generated_key)
    print(f"Decrypted: {decrypted}")
    print()

def demonstrate_table_generation():
    """Demonstrate different table generation strategies"""
    print("=== Auto-key Table Generation ===")
    
    # Classical table
    print("1. Classical Auto-key Table:")
    classical_table = produce_table("classical")
    print("   Each row is a Caesar cipher shifted by row index")
    print(f"   First row: {classical_table[0]}")
    print(f"   Second row: {classical_table[1]}")
    print()
    
    # Caesar table
    print("2. Caesar Auto-key Table (shift=3):")
    caesar_table = produce_table("caesar", shift=3)
    print("   Each row uses Caesar cipher with base_shift + row_index")
    print(f"   First row: {caesar_table[0]}")
    print(f"   Second row: {caesar_table[1]}")
    print()
    
    # Affine table
    print("3. Affine Auto-key Table (a=3, b=5):")
    affine_table = produce_table("affine", a=3, b=5)
    print("   Each row uses Affine cipher with modified b")
    print(f"   First row: {affine_table[0]}")
    print(f"   Second row: {affine_table[1]}")
    print()
    
    # Keyword table
    print("4. Keyword Auto-key Table (keyword='SECRET'):")
    keyword_table = produce_table("keyword", keyword="SECRET")
    print("   Each row uses keyword cipher with row character appended")
    print(f"   First row: {keyword_table[0]}")
    print(f"   Second row: {keyword_table[1]}")
    print()
    
    # Atbash table
    print("5. Atbash Auto-key Table:")
    atbash_table = produce_table("atbash")
    print("   Each row uses Atbash cipher with rotation by row index")
    print(f"   First row: {atbash_table[0]}")
    print(f"   Second row: {atbash_table[1]}")
    print()

def demonstrate_turkish_alphabet():
    """Demonstrate Turkish alphabet support"""
    print("=== Auto-key with Turkish Alphabet ===")
    
    turkish_alphabet = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ"
    plaintext = "MERHABA DÜNYA"
    key = "ANAHTAR"
    
    print(f"Turkish Alphabet: {turkish_alphabet}")
    print(f"Plaintext: {plaintext}")
    print(f"Key: {key}")
    
    # Encrypt with Turkish alphabet
    encrypted = encrypt(plaintext, key, alphabet=turkish_alphabet)
    print(f"Encrypted: {encrypted}")
    
    # Decrypt
    decrypted = decrypt(encrypted, key, alphabet=turkish_alphabet)
    print(f"Decrypted: {decrypted}")
    print()

def demonstrate_composable_system():
    """Demonstrate composable system with Auto-key"""
    print("=== Composable System with Auto-key ===")
    
    plaintext = "TEST MESSAGE"
    key = "TEST"
    
    print(f"Plaintext: {plaintext}")
    print(f"Key: {key}")
    
    # Generate Caesar alphabet
    caesar_alphabet = caesar_produce_alphabet(3)
    print(f"Caesar Alphabet (shift=3): {caesar_alphabet}")
    
    # Encrypt with Caesar alphabet
    encrypted = encrypt(plaintext, key, alphabet=caesar_alphabet)
    print(f"Encrypted with Caesar alphabet: {encrypted}")
    
    # Decrypt
    decrypted = decrypt(encrypted, key, alphabet=caesar_alphabet)
    print(f"Decrypted with Caesar alphabet: {decrypted}")
    print()

def demonstrate_key_length_vs_text_length():
    """Demonstrate key length vs text length"""
    print("=== Key Length vs Text Length ===")
    
    plaintext = "HELLO WORLD"
    
    print(f"Plaintext: {plaintext}")
    print(f"Plaintext length: {len(plaintext)} characters")
    
    # Generate key matching text length
    key_for_text = generate_key_for_text(plaintext)
    print(f"Generated key for text: {key_for_text}")
    print(f"Key length: {len(key_for_text)} characters")
    
    # Encrypt
    encrypted = encrypt(plaintext, key_for_text)
    print(f"Encrypted: {encrypted}")
    
    # Decrypt
    decrypted = decrypt(encrypted, key_for_text)
    print(f"Decrypted: {decrypted}")
    print()

def demonstrate_security_comparison():
    """Demonstrate security comparison with different table types"""
    print("=== Security Comparison ===")
    
    plaintext = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
    key = "SECRET"
    
    print(f"Plaintext: {plaintext}")
    print(f"Key: {key}")
    print()
    
    # Test different table types
    table_types = [
        ("classical", "Classical Auto-key (vulnerable to frequency analysis)"),
        ("caesar", "Caesar Auto-key (still vulnerable)"),
        ("affine", "Affine Auto-key (more complex, harder to break)")
    ]
    
    for table_type, description in table_types:
        print(f"{description}:")
        
        if table_type == "classical":
            encrypted = encrypt(plaintext, key)
        elif table_type == "caesar":
            encrypted = encrypt(plaintext, key, table=produce_table("caesar", shift=13))
        elif table_type == "affine":
            encrypted = encrypt(plaintext, key, table=produce_table("affine", a=5, b=11))
        
        print(f"  Encrypted: {encrypted}")
        print()

def main():
    """Main function to run all demonstrations"""
    print("=== Auto-key Cipher Example ===")
    print("The Auto-key cipher automatically extends the key using the plaintext itself.")
    print("This makes it more secure than Vigenère but also more complex.")
    print()
    
    demonstrate_basic_autokey()
    demonstrate_key_extension()
    demonstrate_random_key_generation()
    demonstrate_encrypt_with_random_key()
    demonstrate_table_generation()
    demonstrate_turkish_alphabet()
    demonstrate_composable_system()
    demonstrate_key_length_vs_text_length()
    demonstrate_security_comparison()
    
    print("=== Auto-key Example Complete ===")

if __name__ == "__main__":
    main()
