"""
Enhanced Porta Cipher Example with Custom Pairing Support

This example demonstrates the enhanced Porta cipher with:
- Custom alphabet pair generation
- Turkish alphabet support
- User-defined custom pairs
- Multiple pairing strategies
"""

from cryptology.classical.substitution.polyalphabetic.porta import (
    encrypt, decrypt, produce_pairs, generate_random_key, generate_key_for_text, encrypt_with_random_key
)


def main():
    print("=" * 70)
    print("ENHANCED PORTA CIPHER EXAMPLE - CUSTOM PAIRING SUPPORT")
    print("=" * 70)
    
    # Example 1: Default pairs
    print("\n1. Default Alphabet Pairs")
    print("-" * 50)
    
    default_pairs = produce_pairs("default")
    print(f"Default pairs (first 5): {default_pairs[:5]}")
    print(f"Total pairs: {len(default_pairs)}")
    
    plaintext = "HELLO"
    key = "KEY"
    encrypted = encrypt(plaintext, key, pairs=default_pairs)
    decrypted = decrypt(encrypted, key, pairs=default_pairs)
    
    print(f"Plaintext: {plaintext}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
    print(f"Success: {plaintext == decrypted}")
    
    # Example 2: Turkish alphabet pairs
    print("\n2. Turkish Alphabet Pairs")
    print("-" * 50)
    
    turkish_alphabet = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ"
    turkish_pairs = produce_pairs("turkish", turkish_alphabet)
    
    print(f"Turkish alphabet: {turkish_alphabet}")
    print(f"Turkish pairs: {turkish_pairs}")
    print(f"Total Turkish pairs: {len(turkish_pairs)}")
    
    turkish_text = "MERHABA"
    key = "A"
    encrypted_turkish = encrypt(turkish_text, key, turkish_alphabet, turkish_pairs)
    decrypted_turkish = decrypt(encrypted_turkish, key, turkish_alphabet, turkish_pairs)
    
    print(f"Turkish text: {turkish_text}")
    print(f"Encrypted: {encrypted_turkish}")
    print(f"Decrypted: {decrypted_turkish}")
    print(f"Success: {turkish_text == decrypted_turkish}")
    
    # Example 3: Custom user-defined pairs
    print("\n3. Custom User-Defined Pairs")
    print("-" * 50)
    
    custom_pairs = [("A", "Z"), ("B", "Y"), ("C", "X"), ("D", "W"), ("E", "V")]
    validated_pairs = produce_pairs("custom", custom_pairs=custom_pairs)
    
    print(f"Custom pairs: {validated_pairs}")
    
    plaintext = "ABCDE"
    key = "ABCDE"
    encrypted_custom = encrypt(plaintext, key, pairs=validated_pairs)
    decrypted_custom = decrypt(encrypted_custom, key, pairs=validated_pairs)
    
    print(f"Plaintext: {plaintext}")
    print(f"Encrypted: {encrypted_custom}")
    print(f"Decrypted: {decrypted_custom}")
    print(f"Success: {plaintext == decrypted_custom}")
    
    # Example 4: Balanced pairs
    print("\n4. Balanced Alphabet Pairs")
    print("-" * 50)
    
    alphabet = "ABCDEFGHIJKL"  # 12 letters
    balanced_pairs = produce_pairs("balanced", alphabet)
    
    print(f"Alphabet: {alphabet}")
    print(f"Balanced pairs: {balanced_pairs}")
    
    plaintext = "ABC"
    key = "ABC"
    encrypted_balanced = encrypt(plaintext, key, alphabet, balanced_pairs)
    decrypted_balanced = decrypt(encrypted_balanced, key, alphabet, balanced_pairs)
    
    print(f"Plaintext: {plaintext}")
    print(f"Encrypted: {encrypted_balanced}")
    print(f"Decrypted: {decrypted_balanced}")
    print(f"Success: {plaintext == decrypted_balanced}")
    
    # Example 5: Pair validation and error handling
    print("\n5. Pair Validation and Error Handling")
    print("-" * 50)
    
    # Test invalid custom pairs
    try:
        produce_pairs("custom")  # Missing custom_pairs
    except ValueError as e:
        print(f"Missing custom_pairs error: {e}")
    
    try:
        produce_pairs("custom", custom_pairs=[])  # Empty pairs
    except ValueError as e:
        print(f"Empty pairs error: {e}")
    
    try:
        produce_pairs("custom", custom_pairs=[("A", "Z"), ("A", "Y")])  # Duplicate letter
    except ValueError as e:
        print(f"Duplicate letter error: {e}")
    
    try:
        produce_pairs("invalid")  # Invalid pair type
    except ValueError as e:
        print(f"Invalid pair type error: {e}")
    
    # Example 6: Self-reciprocal property with custom pairs
    print("\n6. Self-Reciprocal Property with Custom Pairs")
    print("-" * 50)
    
    custom_pairs = [("A", "Z"), ("B", "Y"), ("C", "X")]
    plaintext = "ABC"
    key = "ABC"
    
    encrypted = encrypt(plaintext, key, pairs=custom_pairs)
    print(f"Plaintext: {plaintext}")
    print(f"Encrypted: {encrypted}")
    
    # Demonstrate self-reciprocal property
    encrypted_again = encrypt(encrypted, key, pairs=custom_pairs)
    print(f"Encrypt encrypted text: {encrypted_again}")
    print(f"Self-reciprocal: {encrypted_again == plaintext}")
    
    # Example 7: Different alphabet sizes
    print("\n7. Different Alphabet Sizes")
    print("-" * 50)
    
    test_cases = [
        ("ABCDEFGHIJKL", "balanced"),  # 12 letters
        ("ABCDEFGHIJKLMNOPQRSTUVWXYZ", "default"),  # 26 letters
        ("ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ", "turkish")  # 29 letters
    ]
    
    for alphabet, pair_type in test_cases:
        pairs = produce_pairs(pair_type, alphabet)
        print(f"Alphabet ({len(alphabet)} letters): {alphabet[:10]}...")
        print(f"Pair type: {pair_type}, Pairs: {len(pairs)}")
        
        # Test encryption
        plaintext = alphabet[:3]
        key = "ABC"
        encrypted = encrypt(plaintext, key, alphabet, pairs)
        decrypted = decrypt(encrypted, key, alphabet, pairs)
        print(f"Test: {plaintext} -> {encrypted} -> {decrypted} (Success: {plaintext == decrypted})")
        print()
    
    # Example 8: Random key generation with custom pairs
    print("\n8. Random Key Generation with Custom Pairs")
    print("-" * 50)
    
    custom_pairs = [("A", "Z"), ("B", "Y"), ("C", "X"), ("D", "W"), ("E", "V")]
    plaintext = "ABCDE"
    
    # Generate random key
    random_key = generate_random_key(5)
    print(f"Random key: {random_key}")
    
    encrypted_random = encrypt(plaintext, random_key, pairs=custom_pairs)
    decrypted_random = decrypt(encrypted_random, random_key, pairs=custom_pairs)
    
    print(f"Plaintext: {plaintext}")
    print(f"Encrypted: {encrypted_random}")
    print(f"Decrypted: {decrypted_random}")
    print(f"Success: {plaintext == decrypted_random}")
    
    # Example 9: Encrypt with random key and custom pairs
    print("\n9. Encrypt with Random Key and Custom Pairs")
    print("-" * 50)
    
    plaintext = "SECRET MESSAGE"
    encrypted_text, generated_key = encrypt_with_random_key(plaintext)
    
    print(f"Plaintext: {plaintext}")
    print(f"Generated Key: {generated_key}")
    print(f"Encrypted: {encrypted_text}")
    
    # Decrypt using the generated key
    decrypted_text = decrypt(encrypted_text, generated_key)
    print(f"Decrypted: {decrypted_text}")
    print(f"Success: {plaintext == decrypted_text}")
    
    print("\n" + "=" * 70)
    print("ENHANCED PORTA CIPHER EXAMPLE COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()
