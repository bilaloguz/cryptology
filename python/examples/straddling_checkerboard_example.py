"""
Straddling Checkerboard Cipher Examples

Demonstrates the composite substitution cipher that combines
substitution, fractionation, and numeric key addition.
"""

from cryptology.classical.substitution.composite.straddling_checkerboard import (
    straddling_checkerboard_encrypt,
    straddling_checkerboard_decrypt,
    straddling_checkerboard_produce_checkerboard,
    straddling_checkerboard_generate_random_key,
    straddling_checkerboard_generate_key_for_text,
    straddling_checkerboard_encrypt_with_random_key,
    straddling_checkerboard_encrypt_turkish,
    straddling_checkerboard_decrypt_turkish,
    TURKISH_ALPHABET
)


def main():
    print("=== Straddling Checkerboard Cipher Examples ===\n")
    
    # Basic usage
    print("1. Basic Encryption/Decryption")
    print("-" * 40)
    plaintext = "HELLO WORLD"
    key = "12345"
    
    encrypted = straddling_checkerboard_encrypt(plaintext, key)
    decrypted = straddling_checkerboard_decrypt(encrypted, key)
    
    print(f"Plaintext:  {plaintext}")
    print(f"Key:        {key}")
    print(f"Encrypted:  {encrypted}")
    print(f"Decrypted:  {decrypted}")
    print(f"Success:    {plaintext.replace(' ', '') == decrypted}")
    print()
    
    # Different key types
    print("2. Key Types")
    print("-" * 40)
    
    # Numeric key
    numeric_key = "12345"
    encrypted_numeric = straddling_checkerboard_encrypt(plaintext, numeric_key, key_type="numeric")
    decrypted_numeric = straddling_checkerboard_decrypt(encrypted_numeric, numeric_key, key_type="numeric")
    print(f"Numeric Key:")
    print(f"  Plaintext:  {plaintext}")
    print(f"  Encrypted:  {encrypted_numeric}")
    print(f"  Decrypted:  {decrypted_numeric}")
    print()
    
    # Alphabetic key
    alphabetic_key = "KEY"
    encrypted_alphabetic = straddling_checkerboard_encrypt(plaintext, alphabetic_key, key_type="alphabetic")
    decrypted_alphabetic = straddling_checkerboard_decrypt(encrypted_alphabetic, alphabetic_key, key_type="alphabetic")
    print(f"Alphabetic Key:")
    print(f"  Plaintext:  {plaintext}")
    print(f"  Encrypted:  {encrypted_alphabetic}")
    print(f"  Decrypted:  {decrypted_alphabetic}")
    print()
    
    # Different checkerboard types
    print("3. Checkerboard Types")
    print("-" * 40)
    
    # Standard checkerboard
    standard_checkerboard = straddling_checkerboard_produce_checkerboard("standard")
    encrypted_standard = straddling_checkerboard_encrypt(plaintext, key, standard_checkerboard)
    decrypted_standard = straddling_checkerboard_decrypt(encrypted_standard, key, standard_checkerboard)
    print(f"Standard Checkerboard:")
    print(f"  Plaintext:  {plaintext}")
    print(f"  Encrypted:  {encrypted_standard}")
    print(f"  Decrypted:  {decrypted_standard}")
    print()
    
    # Keyword-based checkerboard
    keyword = "SECRET"
    keyword_checkerboard = straddling_checkerboard_produce_checkerboard("keyword", keyword)
    encrypted_keyword = straddling_checkerboard_encrypt(plaintext, key, keyword_checkerboard)
    decrypted_keyword = straddling_checkerboard_decrypt(encrypted_keyword, key, keyword_checkerboard)
    print(f"Keyword Checkerboard (keyword: {keyword}):")
    print(f"  Plaintext:  {plaintext}")
    print(f"  Encrypted:  {encrypted_keyword}")
    print(f"  Decrypted:  {decrypted_keyword}")
    print()
    
    # Custom checkerboard
    custom_checkerboard = straddling_checkerboard_produce_checkerboard("custom")
    encrypted_custom = straddling_checkerboard_encrypt(plaintext, key, custom_checkerboard)
    decrypted_custom = straddling_checkerboard_decrypt(encrypted_custom, key, custom_checkerboard)
    print(f"Custom Checkerboard:")
    print(f"  Plaintext:  {plaintext}")
    print(f"  Encrypted:  {encrypted_custom}")
    print(f"  Decrypted:  {decrypted_custom}")
    print()
    
    # Checkerboard comparison
    print("4. Checkerboard Comparison")
    print("-" * 40)
    test_text = "HELLO"
    test_key = "12345"
    
    print(f"Same text '{test_text}' with different checkerboards:")
    print(f"  Standard:  {straddling_checkerboard_encrypt(test_text, test_key, standard_checkerboard)}")
    print(f"  Keyword:   {straddling_checkerboard_encrypt(test_text, test_key, keyword_checkerboard)}")
    print(f"  Custom:    {straddling_checkerboard_encrypt(test_text, test_key, custom_checkerboard)}")
    print()
    
    # Random key generation
    print("5. Random Key Generation")
    print("-" * 40)
    
    # Generate numeric key
    numeric_key = straddling_checkerboard_generate_random_key(5, "numeric")
    encrypted_random_numeric = straddling_checkerboard_encrypt(plaintext, numeric_key)
    decrypted_random_numeric = straddling_checkerboard_decrypt(encrypted_random_numeric, numeric_key)
    
    print(f"Random Numeric Key: {numeric_key}")
    print(f"Plaintext:  {plaintext}")
    print(f"Encrypted:  {encrypted_random_numeric}")
    print(f"Decrypted:  {decrypted_random_numeric}")
    print()
    
    # Generate alphabetic key
    alphabetic_key = straddling_checkerboard_generate_random_key(5, "alphabetic")
    encrypted_random_alphabetic = straddling_checkerboard_encrypt(plaintext, alphabetic_key, key_type="alphabetic")
    decrypted_random_alphabetic = straddling_checkerboard_decrypt(encrypted_random_alphabetic, alphabetic_key, key_type="alphabetic")
    
    print(f"Random Alphabetic Key: {alphabetic_key}")
    print(f"Plaintext:  {plaintext}")
    print(f"Encrypted:  {encrypted_random_alphabetic}")
    print(f"Decrypted:  {decrypted_random_alphabetic}")
    print()
    
    # Encrypt with random key
    encrypted_auto, auto_key = straddling_checkerboard_encrypt_with_random_key(plaintext)
    decrypted_auto = straddling_checkerboard_decrypt(encrypted_auto, auto_key)
    
    print(f"Auto-generated Key: {auto_key}")
    print(f"Plaintext:  {plaintext}")
    print(f"Encrypted:  {encrypted_auto}")
    print(f"Decrypted:  {decrypted_auto}")
    print()
    
    # Turkish alphabet support
    print("6. Turkish Alphabet Support")
    print("-" * 40)
    turkish_text = "MERHABA DÜNYA"
    turkish_key = "12345"
    
    encrypted_turkish = straddling_checkerboard_encrypt_turkish(turkish_text, turkish_key)
    decrypted_turkish = straddling_checkerboard_decrypt_turkish(encrypted_turkish, turkish_key)
    
    print(f"Turkish Text: {turkish_text}")
    print(f"Turkish Key:  {turkish_key}")
    print(f"Encrypted:    {encrypted_turkish}")
    print(f"Decrypted:    {decrypted_turkish}")
    print(f"Success:      {turkish_text.replace(' ', '') == decrypted_turkish}")
    print()
    
    # Turkish with custom checkerboard
    turkish_checkerboard = straddling_checkerboard_produce_checkerboard("custom", alphabet=TURKISH_ALPHABET)
    encrypted_turkish_custom = straddling_checkerboard_encrypt(turkish_text, turkish_key, turkish_checkerboard)
    decrypted_turkish_custom = straddling_checkerboard_decrypt(encrypted_turkish_custom, turkish_key, turkish_checkerboard)
    
    print(f"Turkish with Custom Checkerboard:")
    print(f"  Plaintext:  {turkish_text}")
    print(f"  Encrypted:  {encrypted_turkish_custom}")
    print(f"  Decrypted:  {decrypted_turkish_custom}")
    print()
    
    # Long text example
    print("7. Long Text Example")
    print("-" * 40)
    long_text = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
    long_key = "123456789"
    
    encrypted_long = straddling_checkerboard_encrypt(long_text, long_key)
    decrypted_long = straddling_checkerboard_decrypt(encrypted_long, long_key)
    
    print(f"Long Text:   {long_text}")
    print(f"Long Key:    {long_key}")
    print(f"Encrypted:   {encrypted_long}")
    print(f"Decrypted:   {decrypted_long}")
    print(f"Success:     {long_text.replace(' ', '') == decrypted_long}")
    print()
    
    # Key repetition example
    print("8. Key Repetition Example")
    print("-" * 40)
    repeated_text = "HELLO WORLD HELLO WORLD"
    short_key = "123"
    
    encrypted_repeated = straddling_checkerboard_encrypt(repeated_text, short_key)
    decrypted_repeated = straddling_checkerboard_decrypt(encrypted_repeated, short_key)
    
    print(f"Repeated Text: {repeated_text}")
    print(f"Short Key:     {short_key}")
    print(f"Encrypted:     {encrypted_repeated}")
    print(f"Decrypted:     {decrypted_repeated}")
    print(f"Success:       {repeated_text.replace(' ', '') == decrypted_repeated}")
    print()
    
    # Error handling
    print("9. Error Handling")
    print("-" * 40)
    
    try:
        straddling_checkerboard_produce_checkerboard("invalid")
        print("ERROR: Should have raised ValueError for invalid checkerboard type")
    except ValueError as e:
        print(f"✓ Caught expected error: {e}")
    
    try:
        straddling_checkerboard_produce_checkerboard("keyword")
        print("ERROR: Should have raised ValueError for missing keyword")
    except ValueError as e:
        print(f"✓ Caught expected error: {e}")
    
    try:
        straddling_checkerboard_generate_random_key(-1)
        print("ERROR: Should have raised ValueError for negative key length")
    except ValueError as e:
        print(f"✓ Caught expected error: {e}")
    
    try:
        straddling_checkerboard_generate_random_key(5, "invalid")
        print("ERROR: Should have raised ValueError for invalid key type")
    except ValueError as e:
        print(f"✓ Caught expected error: {e}")
    
    print("\n=== All Examples Completed Successfully! ===")


if __name__ == "__main__":
    main()
