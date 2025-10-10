"""
Example usage of the cryptology library.
"""

import cryptology.classical.substitution.monoalphabetic.caesar as caesar
import cryptology.classical.substitution.monoalphabetic.rot13 as rot13
import cryptology.classical.substitution.monoalphabetic.atbash as atbash
import cryptology.classical.substitution.monoalphabetic.keyword as keyword
import cryptology.classical.substitution.monoalphabetic.affine as affine


def main():
    # Example 1: Caesar cipher with English
    print("=" * 50)
    print("CAESAR CIPHER - English")
    print("=" * 50)
    plaintext = "Hello World"
    shift = 3
    encrypted = caesar.encrypt(plaintext, shift)
    print(f"Original:  {plaintext}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {caesar.decrypt(encrypted, shift)}")
    print()
    
    # Example 2: Caesar cipher with custom alphabet
    print("=" * 50)
    print("CAESAR CIPHER - Custom Alphabet (Turkish)")
    print("=" * 50)
    turkish = "abcçdefgğhıijklmnoöprsştuüvyz"
    turkish_text = "Merhaba Dünya"
    encrypted_tr = caesar.encrypt(turkish_text, 5, turkish)
    decrypted_tr = caesar.decrypt(encrypted_tr, 5, turkish)
    print(f"Alphabet:  {turkish}")
    print(f"Original:  {turkish_text}")
    print(f"Encrypted: {encrypted_tr}")
    print(f"Decrypted: {decrypted_tr}")
    print()
    
    # Example 3: ROT13 cipher with English
    print("=" * 50)
    print("ROT13 CIPHER - English")
    print("=" * 50)
    message = "This is a Secret Message!"
    encoded = rot13.encrypt(message)
    decoded = rot13.decrypt(encoded)
    print(f"Original: {message}")
    print(f"Encoded:  {encoded}")
    print(f"Decoded:  {decoded}")
    print()
    
    # Example 4: ROT13 double application
    print("ROT13 applied twice returns original (lowercase):")
    print(f"Start:    {message}")
    print(f"ROT13(1): {rot13.encrypt(message)}")
    print(f"ROT13(2): {rot13.encrypt(rot13.encrypt(message))}")
    print()
    
    # Example 5: ROT13 with custom alphabet
    print("=" * 50)
    print("ROT13 CIPHER - Custom Alphabet (Digits)")
    print("=" * 50)
    digits = "0123456789"
    digit_text = "12345"
    encoded_digits = rot13.encrypt(digit_text, digits)
    print(f"Alphabet: {digits}")
    print(f"Original: {digit_text}")
    print(f"Encoded:  {encoded_digits}")
    print(f"Decoded:  {rot13.decrypt(encoded_digits, digits)}")
    print()
    
    # Example 6: Atbash cipher with English
    print("=" * 50)
    print("ATBASH CIPHER - English")
    print("=" * 50)
    atbash_text = "Hello World"
    encrypted_atbash = atbash.encrypt(atbash_text)
    decrypted_atbash = atbash.decrypt(encrypted_atbash)
    print(f"Original:  {atbash_text}")
    print(f"Encrypted: {encrypted_atbash}")
    print(f"Decrypted: {decrypted_atbash}")
    print()
    
    # Example 7: Atbash double application
    print("Atbash applied twice returns original (lowercase):")
    print(f"Start:      {atbash_text}")
    print(f"Atbash(1):  {atbash.encrypt(atbash_text)}")
    print(f"Atbash(2):  {atbash.encrypt(atbash.encrypt(atbash_text))}")
    print()
    
    # Example 8: Atbash with custom alphabet
    print("=" * 50)
    print("ATBASH CIPHER - Custom Alphabet (Digits)")
    print("=" * 50)
    digit_text_atbash = "12345"
    encrypted_atbash_digits = atbash.encrypt(digit_text_atbash, digits)
    print(f"Alphabet: {digits}")
    print(f"Original: {digit_text_atbash}")
    print(f"Encoded:  {encrypted_atbash_digits}")
    print(f"Decoded:  {atbash.decrypt(encrypted_atbash_digits, digits)}")
    print()
    
    # Example 9: Keyword cipher with English
    print("=" * 50)
    print("KEYWORD CIPHER - English")
    print("=" * 50)
    keyword_text = "Hello World"
    key = "secret"
    encrypted_keyword = keyword.encrypt(keyword_text, key)
    decrypted_keyword = keyword.decrypt(encrypted_keyword, key)
    print(f"Keyword:   {key}")
    print(f"Original:  {keyword_text}")
    print(f"Encrypted: {encrypted_keyword}")
    print(f"Decrypted: {decrypted_keyword}")
    print()
    
    # Example 10: Keyword cipher showing cipher alphabet
    print("=" * 50)
    print("KEYWORD CIPHER - Alphabet Demonstration")
    print("=" * 50)
    key_demo = "zebra"
    print(f"Keyword: {key_demo}")
    print(f"Plain alphabet:  abcdefghijklmnopqrstuvwxyz")
    # Create cipher alphabet manually to show
    from cryptology.classical.substitution.monoalphabetic.keyword import _create_cipher_alphabet
    cipher_alpha = _create_cipher_alphabet(key_demo, "abcdefghijklmnopqrstuvwxyz")
    print(f"Cipher alphabet: {cipher_alpha}")
    test_text = "attack at dawn"
    encrypted_demo = keyword.encrypt(test_text, key_demo)
    print(f"\nOriginal:  {test_text}")
    print(f"Encrypted: {encrypted_demo}")
    print(f"Decrypted: {keyword.decrypt(encrypted_demo, key_demo)}")
    print()
    
    # Example 11: Affine cipher with English
    print("=" * 50)
    print("AFFINE CIPHER - English")
    print("=" * 50)
    affine_text = "Hello World"
    a, b = 5, 8
    encrypted_affine = affine.encrypt(affine_text, a, b)
    decrypted_affine = affine.decrypt(encrypted_affine, a, b)
    print(f"Keys: a={a}, b={b}")
    print(f"Original:  {affine_text}")
    print(f"Encrypted: {encrypted_affine}")
    print(f"Decrypted: {decrypted_affine}")
    print()
    
    # Example 12: Affine cipher - General form demonstration
    print("=" * 50)
    print("AFFINE CIPHER - General Form of Linear Ciphers")
    print("=" * 50)
    demo_text = "cryptology"
    print(f"Original text: {demo_text}\n")
    
    # Show that Caesar is a special case (a=1)
    caesar_shift = 3
    affine_as_caesar = affine.encrypt(demo_text, 1, caesar_shift)
    caesar_direct = caesar.encrypt(demo_text, caesar_shift)
    print(f"Caesar (shift={caesar_shift}):       {caesar_direct}")
    print(f"Affine (a=1, b={caesar_shift}):      {affine_as_caesar}")
    print(f"Same result: {affine_as_caesar == caesar_direct}\n")
    
    # Show different affine transformations
    print("Different affine keys produce different results:")
    print(f"Affine (a=5, b=8):  {affine.encrypt(demo_text, 5, 8)}")
    print(f"Affine (a=7, b=3):  {affine.encrypt(demo_text, 7, 3)}")
    print(f"Affine (a=11, b=15): {affine.encrypt(demo_text, 11, 15)}")


if __name__ == "__main__":
    main()

