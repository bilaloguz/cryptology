"""
Reihenschieber Cipher Examples

Demonstrates the mechanical polyalphabetic substitution cipher with
multiple shift modes, directions, and custom patterns.
"""

from cryptology.classical.substitution.polyalphabetic.reihenschieber import (
    reihenschieber_encrypt,
    reihenschieber_decrypt,
    reihenschieber_generate_random_key,
    reihenschieber_generate_key_for_text,
    reihenschieber_encrypt_with_random_key,
    reihenschieber_produce_custom_shifts,
    reihenschieber_encrypt_turkish,
    reihenschieber_decrypt_turkish,
    TURKISH_ALPHABET
)


def main():
    print("=== Reihenschieber Cipher Examples ===\n")
    
    # Basic usage
    print("1. Basic Encryption/Decryption")
    print("-" * 40)
    plaintext = "HELLO WORLD"
    key = "SECRET"
    
    encrypted = reihenschieber_encrypt(plaintext, key)
    decrypted = reihenschieber_decrypt(encrypted, key)
    
    print(f"Plaintext:  {plaintext}")
    print(f"Key:        {key}")
    print(f"Encrypted:  {encrypted}")
    print(f"Decrypted:  {decrypted}")
    print(f"Success:    {plaintext == decrypted}")
    print()
    
    # Different shift modes
    print("2. Shift Modes")
    print("-" * 40)
    plaintext = "HELLO"
    key = "KEY"
    
    # Fixed mode
    encrypted_fixed = reihenschieber_encrypt(plaintext, key, shift_mode="fixed", shift_amount=2)
    decrypted_fixed = reihenschieber_decrypt(encrypted_fixed, key, shift_mode="fixed", shift_amount=2)
    print(f"Fixed Mode:")
    print(f"  Plaintext:  {plaintext}")
    print(f"  Encrypted:  {encrypted_fixed}")
    print(f"  Decrypted:  {decrypted_fixed}")
    print()
    
    # Progressive mode
    encrypted_progressive = reihenschieber_encrypt(plaintext, key, shift_mode="progressive", shift_amount=1)
    decrypted_progressive = reihenschieber_decrypt(encrypted_progressive, key, shift_mode="progressive", shift_amount=1)
    print(f"Progressive Mode:")
    print(f"  Plaintext:  {plaintext}")
    print(f"  Encrypted:  {encrypted_progressive}")
    print(f"  Decrypted:  {decrypted_progressive}")
    print()
    
    # Custom mode
    custom_shifts = [1, -1, 2, -2, 0]
    encrypted_custom = reihenschieber_encrypt(plaintext, key, shift_mode="custom", custom_shifts=custom_shifts)
    decrypted_custom = reihenschieber_decrypt(encrypted_custom, key, shift_mode="custom", custom_shifts=custom_shifts)
    print(f"Custom Mode:")
    print(f"  Plaintext:  {plaintext}")
    print(f"  Encrypted:  {encrypted_custom}")
    print(f"  Decrypted:  {decrypted_custom}")
    print()
    
    # Shift directions
    print("3. Shift Directions")
    print("-" * 40)
    plaintext = "HELLO"
    key = "KEY"
    
    # Forward (default)
    encrypted_forward = reihenschieber_encrypt(plaintext, key, shift_direction="forward", shift_amount=2)
    decrypted_forward = reihenschieber_decrypt(encrypted_forward, key, shift_direction="forward", shift_amount=2)
    print(f"Forward Direction:")
    print(f"  Plaintext:  {plaintext}")
    print(f"  Encrypted:  {encrypted_forward}")
    print(f"  Decrypted:  {decrypted_forward}")
    print()
    
    # Backward
    encrypted_backward = reihenschieber_encrypt(plaintext, key, shift_direction="backward", shift_amount=2)
    decrypted_backward = reihenschieber_decrypt(encrypted_backward, key, shift_direction="backward", shift_amount=2)
    print(f"Backward Direction:")
    print(f"  Plaintext:  {plaintext}")
    print(f"  Encrypted:  {encrypted_backward}")
    print(f"  Decrypted:  {decrypted_backward}")
    print()
    
    # Custom shift patterns
    print("4. Custom Shift Patterns")
    print("-" * 40)
    plaintext = "HELLO"
    key = "KEY"
    
    # Alternating pattern
    alternating_shifts = reihenschieber_produce_custom_shifts("alternating", 5)
    encrypted_alt = reihenschieber_encrypt(plaintext, key, shift_mode="custom", custom_shifts=alternating_shifts)
    decrypted_alt = reihenschieber_decrypt(encrypted_alt, key, shift_mode="custom", custom_shifts=alternating_shifts)
    print(f"Alternating Pattern: {alternating_shifts}")
    print(f"  Plaintext:  {plaintext}")
    print(f"  Encrypted:  {encrypted_alt}")
    print(f"  Decrypted:  {decrypted_alt}")
    print()
    
    # Fibonacci pattern
    fibonacci_shifts = reihenschieber_produce_custom_shifts("fibonacci", 5)
    encrypted_fib = reihenschieber_encrypt(plaintext, key, shift_mode="custom", custom_shifts=fibonacci_shifts)
    decrypted_fib = reihenschieber_decrypt(encrypted_fib, key, shift_mode="custom", custom_shifts=fibonacci_shifts)
    print(f"Fibonacci Pattern: {fibonacci_shifts}")
    print(f"  Plaintext:  {plaintext}")
    print(f"  Encrypted:  {encrypted_fib}")
    print(f"  Decrypted:  {decrypted_fib}")
    print()
    
    # Prime pattern
    prime_shifts = reihenschieber_produce_custom_shifts("prime", 5)
    encrypted_prime = reihenschieber_encrypt(plaintext, key, shift_mode="custom", custom_shifts=prime_shifts)
    decrypted_prime = reihenschieber_decrypt(encrypted_prime, key, shift_mode="custom", custom_shifts=prime_shifts)
    print(f"Prime Pattern: {prime_shifts}")
    print(f"  Plaintext:  {plaintext}")
    print(f"  Encrypted:  {encrypted_prime}")
    print(f"  Decrypted:  {decrypted_prime}")
    print()
    
    # Random key generation
    print("5. Random Key Generation")
    print("-" * 40)
    plaintext = "HELLO WORLD"
    
    # Generate random key
    random_key = reihenschieber_generate_random_key(5)
    encrypted_random = reihenschieber_encrypt(plaintext, random_key)
    decrypted_random = reihenschieber_decrypt(encrypted_random, random_key)
    
    print(f"Random Key: {random_key}")
    print(f"Plaintext:  {plaintext}")
    print(f"Encrypted:  {encrypted_random}")
    print(f"Decrypted:  {decrypted_random}")
    print()
    
    # Encrypt with random key
    encrypted_auto, auto_key = reihenschieber_encrypt_with_random_key(plaintext)
    decrypted_auto = reihenschieber_decrypt(encrypted_auto, auto_key)
    
    print(f"Auto-generated Key: {auto_key}")
    print(f"Plaintext:  {plaintext}")
    print(f"Encrypted:  {encrypted_auto}")
    print(f"Decrypted:  {decrypted_auto}")
    print()
    
    # Turkish alphabet support
    print("6. Turkish Alphabet Support")
    print("-" * 40)
    turkish_text = "MERHABA DÜNYA"
    turkish_key = "ANAHTAR"
    
    encrypted_turkish = reihenschieber_encrypt_turkish(turkish_text, turkish_key)
    decrypted_turkish = reihenschieber_decrypt_turkish(encrypted_turkish, turkish_key)
    
    print(f"Turkish Text: {turkish_text}")
    print(f"Turkish Key:  {turkish_key}")
    print(f"Encrypted:    {encrypted_turkish}")
    print(f"Decrypted:    {decrypted_turkish}")
    print(f"Success:      {turkish_text == decrypted_turkish}")
    print()
    
    # Long text example
    print("7. Long Text Example")
    print("-" * 40)
    long_text = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
    long_key = "SECRETKEY"
    
    encrypted_long = reihenschieber_encrypt(long_text, long_key, shift_mode="progressive", shift_amount=1)
    decrypted_long = reihenschieber_decrypt(encrypted_long, long_key, shift_mode="progressive", shift_amount=1)
    
    print(f"Long Text:   {long_text}")
    print(f"Long Key:    {long_key}")
    print(f"Encrypted:   {encrypted_long}")
    print(f"Decrypted:   {decrypted_long}")
    print(f"Success:     {long_text == decrypted_long}")
    print()
    
    # Error handling
    print("8. Error Handling")
    print("-" * 40)
    
    try:
        reihenschieber_encrypt("HELLO123", "KEY")
        print("ERROR: Should have raised ValueError for invalid characters")
    except ValueError as e:
        print(f"✓ Caught expected error: {e}")
    
    try:
        reihenschieber_encrypt("HELLO", "KEY", shift_mode="invalid")
        print("ERROR: Should have raised ValueError for invalid shift mode")
    except ValueError as e:
        print(f"✓ Caught expected error: {e}")
    
    try:
        reihenschieber_generate_random_key(-1)
        print("ERROR: Should have raised ValueError for negative key length")
    except ValueError as e:
        print(f"✓ Caught expected error: {e}")
    
    print("\n=== All Examples Completed Successfully! ===")


if __name__ == "__main__":
    main()
