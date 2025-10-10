# Alphabet Guide

This guide shows how to use custom alphabets with the cryptology library.

## Using Custom Alphabets

All ciphers accept an optional `alphabet` parameter. Simply pass your custom alphabet string:

### English (Default)
```python
from cryptology.classical.substitution.monoalphabetic import caesar

# Default English alphabet (lowercase)
encrypted = caesar.encrypt("hello", 3)  # Uses default: "abcdefghijklmnopqrstuvwxyz"

# Or explicitly specify
alphabet_en = "abcdefghijklmnopqrstuvwxyz"
encrypted = caesar.encrypt("hello", 3, alphabet_en)
```

### Turkish
```python
from cryptology.classical.substitution.monoalphabetic import caesar

alphabet_tr = "abcçdefgğhıijklmnoöprsştuüvyz"
plaintext = "merhaba dünya"
encrypted = caesar.encrypt(plaintext, 5, alphabet_tr)
decrypted = caesar.decrypt(encrypted, 5, alphabet_tr)
```

### Russian (Cyrillic)
```python
from cryptology.classical.substitution.monoalphabetic import rot13

alphabet_ru = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
plaintext = "привет мир"
encrypted = rot13.encrypt(plaintext, alphabet_ru)
decrypted = rot13.decrypt(encrypted, alphabet_ru)
```

### Greek
```python
from cryptology.classical.substitution.monoalphabetic import atbash

alphabet_gr = "αβγδεζηθικλμνξοπρστυφχψω"
plaintext = "γεια σου κόσμος"
encrypted = atbash.encrypt(plaintext, alphabet_gr)
decrypted = atbash.decrypt(encrypted, alphabet_gr)
```

### Arabic
```python
from cryptology.classical.substitution.monoalphabetic import keyword

alphabet_ar = "ابتثجحخدذرزسشصضطظعغفقكلمنهوي"
plaintext = "مرحبا"
keyword = "سر"
encrypted = keyword.encrypt(plaintext, keyword, alphabet_ar)
decrypted = keyword.decrypt(encrypted, keyword, alphabet_ar)
```

### Digits
```python
from cryptology.classical.substitution.monoalphabetic import affine

alphabet_digits = "0123456789"
plaintext = "12345"
# For digits (m=10), valid 'a' values: 1, 3, 7, 9
encrypted = affine.encrypt(plaintext, 3, 5, alphabet_digits)
decrypted = affine.decrypt(encrypted, 3, 5, alphabet_digits)
```

### Hexadecimal
```python
from cryptology.classical.substitution.monoalphabetic import caesar

alphabet_hex = "0123456789abcdef"
plaintext = "deadbeef"
encrypted = caesar.encrypt(plaintext, 7, alphabet_hex)
decrypted = caesar.decrypt(encrypted, 7, alphabet_hex)
```

### Custom Symbols
```python
from cryptology.classical.substitution.monoalphabetic import caesar

alphabet_custom = "!@#$%^&*()_+-=[]{}|;:,.<>?"
plaintext = "!@#$"
encrypted = caesar.encrypt(plaintext, 5, alphabet_custom)
decrypted = caesar.decrypt(encrypted, 5, alphabet_custom)
```

## Important Notes

1. **Lowercase Only**: All alphabets should be lowercase. Input text is automatically converted to lowercase.

2. **No Duplicates**: Alphabets should not contain duplicate characters.

3. **Consistent Usage**: Use the same alphabet for both encryption and decryption.

4. **Affine Cipher Constraint**: For the Affine cipher, the multiplicative key `a` must be coprime with the alphabet length.
   - For m=26 (English): valid a = 1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25
   - For m=10 (digits): valid a = 1, 3, 7, 9
   - For m=16 (hex): valid a = 1, 3, 5, 7, 9, 11, 13, 15

## Example: Complete Multi-Language Support

```python
from cryptology.classical.substitution.monoalphabetic import caesar, affine, keyword

# Define alphabets
alphabets = {
    "english": "abcdefghijklmnopqrstuvwxyz",
    "turkish": "abcçdefgğhıijklmnoöprsştuüvyz",
    "russian": "абвгдежзийклмнопрстуфхцчшщъыьэюя",
    "digits": "0123456789",
}

# Encrypt in different languages
texts = {
    "english": "hello world",
    "turkish": "merhaba dünya",
    "russian": "привет мир",
    "digits": "12345",
}

for lang, alphabet in alphabets.items():
    plaintext = texts[lang]
    
    # Caesar cipher
    encrypted = caesar.encrypt(plaintext, 3, alphabet)
    print(f"{lang}: {plaintext} -> {encrypted}")
    
    # Keyword cipher
    encrypted = keyword.encrypt(plaintext, "secret", alphabet)
    print(f"{lang} (keyword): {plaintext} -> {encrypted}")
```

