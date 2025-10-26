"""
Example demonstrating Vigenère cipher with random key generation.

This example shows how to use the Vigenère cipher with randomly generated keys,
including proper key communication for secure transmission.
"""

import sys
import os

# Add the parent directory to the path so we can import cryptology
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cryptology.classical.substitution.polyalphabetic import (
    vigenere_encrypt, vigenere_decrypt, vigenere_produce_table,
    vigenere_generate_random_key, vigenere_generate_key_for_text,
    vigenere_encrypt_with_random_key
)


def demonstrate_random_key_generation():
    """Demonstrate random key generation features."""
    print("=== Random Key Generation Demo ===")
    
    # Generate random keys of different lengths
    print("1. Generate random keys of different lengths:")
    key_5 = vigenere_generate_random_key(5)
    key_10 = vigenere_generate_random_key(10)
    key_15 = vigenere_generate_random_key(15)
    
    print(f"5-character key:  {key_5}")
    print(f"10-character key: {key_10}")
    print(f"15-character key: {key_15}")
    print()
    
    # Generate key for specific text
    print("2. Generate key for specific text:")
    plaintext = "HELLO WORLD"
    auto_key = vigenere_generate_key_for_text(plaintext)
    print(f"Plaintext: {plaintext}")
    print(f"Auto-generated key: {auto_key}")
    print(f"Key length: {len(auto_key)}")
    print()


def demonstrate_encryption_with_random_key():
    """Demonstrate encryption with random key generation."""
    print("=== Encryption with Random Key Demo ===")
    
    plaintext = "SECRET MESSAGE"
    
    print(f"Plaintext: {plaintext}")
    print()
    
    # Method 1: Generate key separately, then encrypt
    print("Method 1: Generate key separately")
    random_key = vigenere_generate_key_for_text(plaintext)
    encrypted = vigenere_encrypt(plaintext, random_key)
    
    print(f"Generated key: {random_key}")
    print(f"Encrypted: {encrypted}")
    print()
    
    # Method 2: Encrypt with auto-generated key
    print("Method 2: Encrypt with auto-generated key")
    encrypted2, generated_key = vigenere_encrypt_with_random_key(plaintext)
    
    print(f"Generated key: {generated_key}")
    print(f"Encrypted: {encrypted2}")
    print()
    
    # Verify decryption works
    print("Verification - Decryption:")
    decrypted = vigenere_decrypt(encrypted, random_key)
    decrypted2 = vigenere_decrypt(encrypted2, generated_key)
    
    print(f"Decrypted (Method 1): {decrypted}")
    print(f"Decrypted (Method 2): {decrypted2}")
    print(f"Both methods work: {decrypted == decrypted2 == plaintext}")
    print()


def demonstrate_key_communication():
    """Demonstrate proper key communication for secure transmission."""
    print("=== Key Communication Demo ===")
    
    plaintext = "IMPORTANT SECRET DATA"
    
    print("Scenario: Alice wants to send encrypted message to Bob")
    print(f"Message: {plaintext}")
    print()
    
    # Alice encrypts with random key
    print("Step 1: Alice encrypts the message")
    encrypted, secret_key = vigenere_encrypt_with_random_key(plaintext)
    
    print(f"Encrypted message: {encrypted}")
    print(f"Secret key: {secret_key}")
    print()
    
    # Alice communicates the key to Bob (securely)
    print("Step 2: Alice securely transmits the key to Bob")
    print("(This should be done through a secure channel)")
    print(f"Key to transmit: {secret_key}")
    print()
    
    # Bob decrypts using the received key
    print("Step 3: Bob decrypts using the received key")
    decrypted = vigenere_decrypt(encrypted, secret_key)
    
    print(f"Decrypted message: {decrypted}")
    print(f"Message integrity: {decrypted == plaintext}")
    print()


def demonstrate_different_table_types_with_random_keys():
    """Demonstrate random keys with different table types."""
    print("=== Random Keys with Different Table Types ===")
    
    plaintext = "CRYPTOGRAPHIC SECURITY"
    
    print(f"Plaintext: {plaintext}")
    print()
    
    # Generate different tables
    classical_table = vigenere_produce_table("classical")
    caesar_table = vigenere_produce_table("caesar", shift=7)
    affine_table = vigenere_produce_table("affine", a=3, b=5)
    atbash_table = vigenere_produce_table("atbash")
    
    tables = [
        ("Classical", classical_table),
        ("Caesar (shift=7)", caesar_table),
        ("Affine (a=3, b=5)", affine_table),
        ("Atbash", atbash_table)
    ]
    
    for name, table in tables:
        print(f"{name} table:")
        
        # Generate random key
        random_key = vigenere_generate_key_for_text(plaintext)
        
        # Encrypt
        encrypted = vigenere_encrypt(plaintext, random_key, table=table)
        
        # Decrypt
        decrypted = vigenere_decrypt(encrypted, random_key, table=table)
        
        print(f"  Random key: {random_key}")
        print(f"  Encrypted:  {encrypted}")
        print(f"  Decrypted:  {decrypted}")
        print(f"  Success:    {decrypted == plaintext}")
        print()


def demonstrate_turkish_alphabet_with_random_keys():
    """Demonstrate random keys with Turkish alphabet."""
    print("=== Random Keys with Turkish Alphabet ===")
    
    turkish_alphabet = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ"
    plaintext = "MERHABA DÜNYA"
    
    print(f"Plaintext: {plaintext}")
    print(f"Turkish alphabet: {turkish_alphabet}")
    print(f"Alphabet length: {len(turkish_alphabet)}")
    print()
    
    # Generate random key for Turkish
    turkish_key = vigenere_generate_random_key(10, turkish_alphabet)
    print(f"Generated Turkish key: {turkish_key}")
    
    # Generate table for Turkish
    turkish_table = vigenere_produce_table("classical", alphabet=turkish_alphabet)
    print(f"Table size: {len(turkish_table)}x{len(turkish_table[0])}")
    
    # Encrypt and decrypt
    encrypted = vigenere_encrypt(plaintext, turkish_key, table=turkish_table, alphabet=turkish_alphabet)
    decrypted = vigenere_decrypt(encrypted, turkish_key, table=turkish_table, alphabet=turkish_alphabet)
    
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
    print(f"Success: {decrypted == plaintext}")
    print()


def demonstrate_security_benefits():
    """Demonstrate security benefits of random keys."""
    print("=== Security Benefits of Random Keys ===")
    
    plaintext = "ATTACK AT DAWN"
    
    print(f"Plaintext: {plaintext}")
    print()
    
    print("Comparison of key types:")
    print()
    
    # Weak user key
    weak_key = "KEY"
    encrypted_weak = vigenere_encrypt(plaintext, weak_key)
    print(f"Weak key '{weak_key}':")
    print(f"  Encrypted: {encrypted_weak}")
    print(f"  Security:  LOW (predictable pattern)")
    print()
    
    # Random key
    random_key = vigenere_generate_key_for_text(plaintext)
    encrypted_random = vigenere_encrypt(plaintext, random_key)
    print(f"Random key '{random_key}':")
    print(f"  Encrypted: {encrypted_random}")
    print(f"  Security:  HIGH (unpredictable)")
    print()
    
    print("Security advantages of random keys:")
    print("1. Unpredictable - no patterns to exploit")
    print("2. Cryptographically secure - uses proper random generation")
    print("3. Appropriate length - matches message length")
    print("4. No repetition - each key is unique")
    print("5. Resistant to frequency analysis")
    print()


def demonstrate_key_management_best_practices():
    """Demonstrate key management best practices."""
    print("=== Key Management Best Practices ===")
    
    plaintext = "CONFIDENTIAL INFORMATION"
    
    print(f"Message: {plaintext}")
    print()
    
    # Generate secure key
    secure_key = vigenere_generate_random_key(20)  # Long key for security
    encrypted, _ = vigenere_encrypt_with_random_key(plaintext, key_length=20)
    
    print("✅ Best Practices:")
    print(f"1. Generated secure key: {secure_key}")
    print(f"2. Key length: {len(secure_key)} characters")
    print(f"3. Encrypted message: {encrypted}")
    print()
    
    print("📋 Key Management Checklist:")
    print("□ Generate key using cryptographically secure random")
    print("□ Use appropriate key length (longer = more secure)")
    print("□ Store key securely (not with encrypted message)")
    print("□ Transmit key through secure channel")
    print("□ Destroy key after use (if one-time use)")
    print("□ Never reuse keys for different messages")
    print("□ Keep key secret from unauthorized parties")
    print()


if __name__ == "__main__":
    print("Vigenère Cipher with Random Key Generation Demo")
    print("=" * 50)
    print()
    
    demonstrate_random_key_generation()
    demonstrate_encryption_with_random_key()
    demonstrate_key_communication()
    demonstrate_different_table_types_with_random_keys()
    demonstrate_turkish_alphabet_with_random_keys()
    demonstrate_security_benefits()
    demonstrate_key_management_best_practices()
    
    print("Demo completed!")
    print()
    print("Key Features:")
    print("1. Cryptographically secure random key generation")
    print("2. Automatic key length matching")
    print("3. Integration with all table types")
    print("4. Support for multiple alphabets")
    print("5. Proper key communication guidance")
    print("6. Enhanced security over user-chosen keys")
    print("7. Best practices for key management")
