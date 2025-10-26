"""
Porta Cipher Example

This example demonstrates the Porta cipher, which is a self-reciprocal polyalphabetic
substitution cipher that uses alphabet pairs. Each letter in the keyword determines
which alphabet pair to use for encryption.
"""

from cryptology.classical.substitution.polyalphabetic.porta import (
    encrypt, decrypt, generate_random_key, generate_key_for_text, encrypt_with_random_key
)


def main():
    print("=" * 60)
    print("PORTA CIPHER EXAMPLE")
    print("=" * 60)
    
    # Example 1: Basic encryption/decryption
    print("\n1. Basic Encryption/Decryption")
    print("-" * 40)
    
    plaintext = "HELLO WORLD"
    key = "KEY"
    
    print(f"Plaintext: {plaintext}")
    print(f"Key:       {key}")
    
    encrypted = encrypt(plaintext, key)
    decrypted = decrypt(encrypted, key)
    
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
    print(f"Success:   {plaintext == decrypted}")
    
    # Example 2: Self-reciprocal property demonstration
    print("\n2. Self-Reciprocal Property")
    print("-" * 40)
    
    plaintext = "SECRET MESSAGE"
    key = "PORTACIPHER"
    
    print(f"Plaintext: {plaintext}")
    print(f"Key:       {key}")
    
    encrypted = encrypt(plaintext, key)
    print(f"Encrypted: {encrypted}")
    
    # Demonstrate self-reciprocal property
    encrypted_again = encrypt(encrypted, key)
    print(f"Encrypt encrypted text: {encrypted_again}")
    print(f"Self-reciprocal: {encrypted_again == plaintext}")
    
    # Example 3: Alphabet pairs demonstration
    print("\n3. Alphabet Pairs Demonstration")
    print("-" * 40)
    
    print("Porta cipher uses 13 alphabet pairs:")
    pairs = [
        ("A", "N"), ("B", "O"), ("C", "P"), ("D", "Q"), ("E", "R"),
        ("F", "S"), ("G", "T"), ("H", "U"), ("I", "V"), ("J", "W"),
        ("K", "X"), ("L", "Y"), ("M", "Z")
    ]
    
    for i, (a, b) in enumerate(pairs):
        print(f"Pair {i+1:2d}: {a} ↔ {b}")
    
    print("\nTesting individual pairs:")
    test_pairs = [("A", "N"), ("C", "P"), ("E", "R"), ("G", "T")]
    
    for a, b in test_pairs:
        # Test with key 'A' (uses first pair)
        encrypted_a = encrypt(a, "A")
        encrypted_b = encrypt(b, "A")
        print(f"Key 'A': {a} -> {encrypted_a}, {b} -> {encrypted_b}")
        
        # Test with key 'B' (same pair, different mapping)
        encrypted_a_b = encrypt(a, "B")
        encrypted_b_b = encrypt(b, "B")
        print(f"Key 'B': {a} -> {encrypted_a_b}, {b} -> {encrypted_b_b}")
    
    # Example 4: Key repetition for longer messages
    print("\n4. Key Repetition")
    print("-" * 40)
    
    long_text = "THIS IS A LONG MESSAGE THAT REQUIRES KEY REPETITION"
    short_key = "AB"
    
    print(f"Text:      {long_text}")
    print(f"Key:       {short_key}")
    
    encrypted_long = encrypt(long_text, short_key)
    decrypted_long = decrypt(encrypted_long, short_key)
    
    print(f"Encrypted: {encrypted_long}")
    print(f"Decrypted: {decrypted_long}")
    print(f"Success:   {long_text == decrypted_long}")
    
    # Example 5: Case preservation
    print("\n5. Case Preservation")
    print("-" * 40)
    
    mixed_case = "Hello World"
    key = "KEY"
    
    print(f"Text:      {mixed_case}")
    print(f"Key:       {key}")
    
    encrypted_mixed = encrypt(mixed_case, key)
    decrypted_mixed = decrypt(encrypted_mixed, key)
    
    print(f"Encrypted: {encrypted_mixed}")
    print(f"Decrypted: {decrypted_mixed}")
    print(f"Success:   {mixed_case == decrypted_mixed}")
    
    # Example 6: Random key generation
    print("\n6. Random Key Generation")
    print("-" * 40)
    
    plaintext = "RANDOM KEY EXAMPLE"
    
    # Generate random key
    random_key = generate_random_key(10)
    print(f"Random key (length 10): {random_key}")
    
    encrypted_random = encrypt(plaintext, random_key)
    decrypted_random = decrypt(encrypted_random, random_key)
    
    print(f"Plaintext:  {plaintext}")
    print(f"Encrypted:  {encrypted_random}")
    print(f"Decrypted:  {decrypted_random}")
    print(f"Success:    {plaintext == decrypted_random}")
    
    # Generate key for specific text
    auto_key = generate_key_for_text(plaintext)
    print(f"\nAuto-generated key: {auto_key}")
    
    encrypted_auto = encrypt(plaintext, auto_key)
    decrypted_auto = decrypt(encrypted_auto, auto_key)
    
    print(f"Plaintext:  {plaintext}")
    print(f"Encrypted:  {encrypted_auto}")
    print(f"Decrypted:  {decrypted_auto}")
    print(f"Success:    {plaintext == decrypted_auto}")
    
    # Example 7: Encrypt with random key (returns both ciphertext and key)
    print("\n7. Encrypt with Random Key")
    print("-" * 40)
    
    plaintext = "CONFIDENTIAL MESSAGE"
    encrypted_text, generated_key = encrypt_with_random_key(plaintext)
    
    print(f"Plaintext:     {plaintext}")
    print(f"Generated Key: {generated_key}")
    print(f"Encrypted:     {encrypted_text}")
    
    # Decrypt using the generated key
    decrypted_text = decrypt(encrypted_text, generated_key)
    print(f"Decrypted:     {decrypted_text}")
    print(f"Success:       {plaintext == decrypted_text}")
    
    # Example 8: Turkish alphabet support
    print("\n8. Turkish Alphabet Support")
    print("-" * 40)
    
    turkish_alphabet = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ"
    turkish_text = "MERHABA DÜNYA"
    key = "KEY"
    
    print(f"Turkish Alphabet: {turkish_alphabet}")
    print(f"Turkish Text:     {turkish_text}")
    print(f"Key:              {key}")
    
    encrypted_turkish = encrypt(turkish_text, key, alphabet=turkish_alphabet)
    decrypted_turkish = decrypt(encrypted_turkish, key, alphabet=turkish_alphabet)
    
    print(f"Encrypted:        {encrypted_turkish}")
    print(f"Decrypted:        {decrypted_turkish}")
    print(f"Success:          {turkish_text == decrypted_turkish}")
    
    # Example 9: Error handling
    print("\n9. Error Handling")
    print("-" * 40)
    
    try:
        encrypt("HELLO", "123")  # Invalid key
    except ValueError as e:
        print(f"Invalid key error: {e}")
    
    try:
        encrypt("HELLO", "")  # Empty key
    except ValueError as e:
        print(f"Empty key error: {e}")
    
    try:
        encrypt("HELLO", "AB1C")  # Mixed alphanumeric key
    except ValueError as e:
        print(f"Mixed alphanumeric key error: {e}")
    
    # Example 10: Comparison with other ciphers
    print("\n10. Porta vs Other Ciphers")
    print("-" * 40)
    
    plaintext = "COMPARISON TEST"
    key = "KEY"
    
    print(f"Plaintext: {plaintext}")
    print(f"Key:       {key}")
    
    # Porta encryption
    porta_encrypted = encrypt(plaintext, key)
    print(f"Porta encrypted: {porta_encrypted}")
    
    # Demonstrate self-reciprocal property
    porta_decrypted = decrypt(porta_encrypted, key)
    print(f"Porta decrypted: {porta_decrypted}")
    print(f"Self-reciprocal: {porta_decrypted == plaintext}")
    
    print("\n" + "=" * 60)
    print("PORTA CIPHER EXAMPLE COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()
