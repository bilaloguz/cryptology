"""
Gronsfeld Cipher Example

This example demonstrates the Gronsfeld cipher, which is a numeric variant
of the Vigenère cipher. Instead of using alphabetic keys, Gronsfeld uses
numeric keys where each digit specifies the shift amount.
"""

from cryptology.classical.substitution.polyalphabetic.gronsfeld import (
    encrypt, decrypt, produce_table, generate_random_numeric_key,
    generate_numeric_key_for_text, encrypt_with_random_key
)


def main():
    print("=" * 60)
    print("GRONSFELD CIPHER EXAMPLE")
    print("=" * 60)
    
    # Example 1: Basic encryption/decryption
    print("\n1. Basic Encryption/Decryption")
    print("-" * 40)
    
    plaintext = "HELLO WORLD"
    key = "12312"
    
    print(f"Plaintext: {plaintext}")
    print(f"Key:       {key}")
    
    encrypted = encrypt(plaintext, key)
    decrypted = decrypt(encrypted, key)
    
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
    print(f"Success:   {plaintext == decrypted}")
    
    # Example 2: Key repetition for longer messages
    print("\n2. Key Repetition")
    print("-" * 40)
    
    long_text = "THIS IS A LONG MESSAGE THAT REQUIRES KEY REPETITION"
    short_key = "123"
    
    print(f"Text:      {long_text}")
    print(f"Key:       {short_key}")
    
    encrypted_long = encrypt(long_text, short_key)
    decrypted_long = decrypt(encrypted_long, short_key)
    
    print(f"Encrypted: {encrypted_long}")
    print(f"Decrypted: {decrypted_long}")
    print(f"Success:   {long_text == decrypted_long}")
    
    # Example 3: Case preservation
    print("\n3. Case Preservation")
    print("-" * 40)
    
    mixed_case = "Hello World"
    key = "12312"
    
    print(f"Text:      {mixed_case}")
    print(f"Key:       {key}")
    
    encrypted_mixed = encrypt(mixed_case, key)
    decrypted_mixed = decrypt(encrypted_mixed, key)
    
    print(f"Encrypted: {encrypted_mixed}")
    print(f"Decrypted: {decrypted_mixed}")
    print(f"Success:   {mixed_case == decrypted_mixed}")
    
    # Example 4: Custom table generation
    print("\n4. Custom Table Generation")
    print("-" * 40)
    
    plaintext = "SECRET MESSAGE"
    key = "12345"
    
    # Classical table (default)
    classical_table = produce_table("classical")
    encrypted_classical = encrypt(plaintext, key, classical_table)
    decrypted_classical = decrypt(encrypted_classical, key, classical_table)
    
    print(f"Classical Table:")
    print(f"  Plaintext:  {plaintext}")
    print(f"  Encrypted:  {encrypted_classical}")
    print(f"  Decrypted:  {decrypted_classical}")
    print(f"  Success:    {plaintext == decrypted_classical}")
    
    # Caesar-based table
    caesar_table = produce_table("caesar", shift=5)
    encrypted_caesar = encrypt(plaintext, key, caesar_table)
    decrypted_caesar = decrypt(encrypted_caesar, key, caesar_table)
    
    print(f"\nCaesar Table (shift=5):")
    print(f"  Plaintext:  {plaintext}")
    print(f"  Encrypted:  {encrypted_caesar}")
    print(f"  Decrypted:  {decrypted_caesar}")
    print(f"  Success:    {plaintext == decrypted_caesar}")
    
    # Affine-based table
    affine_table = produce_table("affine", a=5, b=7)
    encrypted_affine = encrypt(plaintext, key, affine_table)
    decrypted_affine = decrypt(encrypted_affine, key, affine_table)
    
    print(f"\nAffine Table (a=5, b=7):")
    print(f"  Plaintext:  {plaintext}")
    print(f"  Encrypted:  {encrypted_affine}")
    print(f"  Decrypted:  {decrypted_affine}")
    print(f"  Success:    {plaintext == decrypted_affine}")
    
    # Keyword-based table
    keyword_table = produce_table("keyword", keyword="SECRET")
    encrypted_keyword = encrypt(plaintext, key, keyword_table)
    decrypted_keyword = decrypt(encrypted_keyword, key, keyword_table)
    
    print(f"\nKeyword Table (keyword=SECRET):")
    print(f"  Plaintext:  {plaintext}")
    print(f"  Encrypted:  {encrypted_keyword}")
    print(f"  Decrypted:  {decrypted_keyword}")
    print(f"  Success:    {plaintext == decrypted_keyword}")
    
    # Atbash-based table
    atbash_table = produce_table("atbash")
    encrypted_atbash = encrypt(plaintext, key, atbash_table)
    decrypted_atbash = decrypt(encrypted_atbash, key, atbash_table)
    
    print(f"\nAtbash Table:")
    print(f"  Plaintext:  {plaintext}")
    print(f"  Encrypted:  {encrypted_atbash}")
    print(f"  Decrypted:  {decrypted_atbash}")
    print(f"  Success:    {plaintext == decrypted_atbash}")
    
    # Example 5: Random key generation
    print("\n5. Random Key Generation")
    print("-" * 40)
    
    plaintext = "RANDOM KEY EXAMPLE"
    
    # Generate random key
    random_key = generate_random_numeric_key(10)
    print(f"Random key (length 10): {random_key}")
    
    encrypted_random = encrypt(plaintext, random_key)
    decrypted_random = decrypt(encrypted_random, random_key)
    
    print(f"Plaintext:  {plaintext}")
    print(f"Encrypted:  {encrypted_random}")
    print(f"Decrypted:  {decrypted_random}")
    print(f"Success:    {plaintext == decrypted_random}")
    
    # Generate key for specific text
    auto_key = generate_numeric_key_for_text(plaintext)
    print(f"\nAuto-generated key: {auto_key}")
    
    encrypted_auto = encrypt(plaintext, auto_key)
    decrypted_auto = decrypt(encrypted_auto, auto_key)
    
    print(f"Plaintext:  {plaintext}")
    print(f"Encrypted:  {encrypted_auto}")
    print(f"Decrypted:  {decrypted_auto}")
    print(f"Success:    {plaintext == decrypted_auto}")
    
    # Example 6: Encrypt with random key (returns both ciphertext and key)
    print("\n6. Encrypt with Random Key")
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
    
    # Example 7: Turkish alphabet support
    print("\n7. Turkish Alphabet Support")
    print("-" * 40)
    
    turkish_alphabet = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ"
    turkish_text = "MERHABA DÜNYA"
    key = "12312"
    
    print(f"Turkish Alphabet: {turkish_alphabet}")
    print(f"Turkish Text:     {turkish_text}")
    print(f"Key:              {key}")
    
    encrypted_turkish = encrypt(turkish_text, key, alphabet=turkish_alphabet)
    decrypted_turkish = decrypt(encrypted_turkish, key, alphabet=turkish_alphabet)
    
    print(f"Encrypted:        {encrypted_turkish}")
    print(f"Decrypted:        {decrypted_turkish}")
    print(f"Success:          {turkish_text == decrypted_turkish}")
    
    # Example 8: Error handling
    print("\n8. Error Handling")
    print("-" * 40)
    
    try:
        encrypt("HELLO", "abc123")  # Invalid key
    except ValueError as e:
        print(f"Invalid key error: {e}")
    
    try:
        encrypt("HELLO", "")  # Empty key
    except ValueError as e:
        print(f"Empty key error: {e}")
    
    try:
        produce_table("invalid")  # Invalid table type
    except ValueError as e:
        print(f"Invalid table type error: {e}")
    
    try:
        produce_table("caesar")  # Missing shift parameter
    except ValueError as e:
        print(f"Missing parameter error: {e}")
    
    print("\n" + "=" * 60)
    print("GRONSFELD CIPHER EXAMPLE COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()
