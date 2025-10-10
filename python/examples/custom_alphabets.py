"""
Examples of using custom alphabets with various ciphers.
"""

from cryptology.classical.substitution.monoalphabetic import (
    caesar, rot13, atbash, keyword, affine
)


def example_turkish():
    """Turkish alphabet example."""
    print("=" * 60)
    print("TURKISH ALPHABET")
    print("=" * 60)
    
    alphabet_tr = "abcçdefgğhıijklmnoöprsştuüvyz"
    plaintext = "merhaba dünya"
    
    # Caesar
    encrypted = caesar.encrypt(plaintext, 5, alphabet_tr)
    print(f"Original:  {plaintext}")
    print(f"Caesar(5): {encrypted}")
    print(f"Decrypted: {caesar.decrypt(encrypted, 5, alphabet_tr)}")
    print()


def example_russian():
    """Russian (Cyrillic) alphabet example."""
    print("=" * 60)
    print("RUSSIAN (CYRILLIC) ALPHABET")
    print("=" * 60)
    
    alphabet_ru = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
    plaintext = "привет мир"
    
    # ROT13 (will shift by half the alphabet)
    encrypted = rot13.encrypt(plaintext, alphabet_ru)
    print(f"Original: {plaintext}")
    print(f"ROT13:    {encrypted}")
    print(f"Decrypted: {rot13.decrypt(encrypted, alphabet_ru)}")
    print()


def example_digits():
    """Digits alphabet example."""
    print("=" * 60)
    print("DIGITS ALPHABET")
    print("=" * 60)
    
    alphabet_digits = "0123456789"
    plaintext = "20231015"
    
    # Caesar
    encrypted_caesar = caesar.encrypt(plaintext, 3, alphabet_digits)
    print(f"Original:   {plaintext}")
    print(f"Caesar(3):  {encrypted_caesar}")
    
    # Atbash
    encrypted_atbash = atbash.encrypt(plaintext, alphabet_digits)
    print(f"Atbash:     {encrypted_atbash}")
    
    # Affine (a must be coprime with 10: valid values are 1, 3, 7, 9)
    encrypted_affine = affine.encrypt(plaintext, 3, 7, alphabet_digits)
    print(f"Affine(3,7): {encrypted_affine}")
    print()


def example_hexadecimal():
    """Hexadecimal alphabet example."""
    print("=" * 60)
    print("HEXADECIMAL ALPHABET")
    print("=" * 60)
    
    alphabet_hex = "0123456789abcdef"
    plaintext = "deadbeef"
    
    # Caesar
    encrypted = caesar.encrypt(plaintext, 7, alphabet_hex)
    print(f"Original:  {plaintext}")
    print(f"Caesar(7): {encrypted}")
    print(f"Decrypted: {caesar.decrypt(encrypted, 7, alphabet_hex)}")
    print()


def example_multilanguage():
    """Multi-language encryption example."""
    print("=" * 60)
    print("MULTI-LANGUAGE ENCRYPTION")
    print("=" * 60)
    
    languages = {
        "English": ("abcdefghijklmnopqrstuvwxyz", "hello world"),
        "Turkish": ("abcçdefgğhıijklmnoöprsştuüvyz", "merhaba dünya"),
        "Russian": ("абвгдежзийклмнопрстуфхцчшщъыьэюя", "привет мир"),
        "Digits":  ("0123456789", "12345"),
    }
    
    for lang, (alphabet, text) in languages.items():
        encrypted = keyword.encrypt(text, "secret", alphabet)
        print(f"{lang:10s}: {text:20s} -> {encrypted}")
    print()


def example_affine_coprime():
    """Demonstrate Affine cipher coprime requirement."""
    print("=" * 60)
    print("AFFINE CIPHER - COPRIME REQUIREMENT")
    print("=" * 60)
    
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    plaintext = "test"
    
    print(f"Alphabet length: {len(alphabet)}")
    print(f"Valid 'a' values (coprime with 26): 1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25\n")
    
    # Valid keys
    valid_a_values = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]
    for a in valid_a_values[:5]:  # Show first 5
        encrypted = affine.encrypt(plaintext, a, 0, alphabet)
        print(f"a={a:2d}, b=0: {plaintext} -> {encrypted}")
    
    print("\nInvalid 'a' values (not coprime with 26):")
    invalid_a_values = [2, 4, 6, 8, 10, 12, 13]
    for a in invalid_a_values[:3]:  # Show first 3
        try:
            encrypted = affine.encrypt(plaintext, a, 0, alphabet)
        except ValueError as e:
            print(f"a={a:2d}: ❌ {str(e)}")
    print()


if __name__ == "__main__":
    example_turkish()
    example_russian()
    example_digits()
    example_hexadecimal()
    example_multilanguage()
    example_affine_coprime()

