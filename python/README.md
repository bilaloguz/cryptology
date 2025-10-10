# Cryptology

A comprehensive Python library for classical and modern cryptography algorithms.

## Structure

```
cryptology/
├── cryptology/
│   └── classical/
│       └── substitution/
│           └── monoalphabetic/
│               ├── caesar.py
│               ├── rot13.py
│               ├── atbash.py
│               ├── keyword.py
│               └── affine.py
├── examples/
│   └── custom_alphabets.py
├── tests/
├── ALPHABETS.md
├── README.md
└── example.py
```

## Installation

```bash
pip install -e .
```

## Usage

```python
import cryptology.classical.substitution.monoalphabetic.caesar as caesar
import cryptology.classical.substitution.monoalphabetic.rot13 as rot13
import cryptology.classical.substitution.monoalphabetic.atbash as atbash
import cryptology.classical.substitution.monoalphabetic.keyword as keyword
import cryptology.classical.substitution.monoalphabetic.affine as affine

# Caesar cipher - shift-based substitution
encrypted = caesar.encrypt("HELLO", 3)  # Returns: 'khoor'
decrypted = caesar.decrypt(encrypted, 3)  # Returns: 'hello'

# ROT13 cipher - shift by 13 (half alphabet)
encoded = rot13.encrypt("HELLO")  # Returns: 'uryyb'
decoded = rot13.decrypt(encoded)  # Returns: 'hello'

# Atbash cipher - alphabet reversal
encoded = atbash.encrypt("HELLO")  # Returns: 'svool'
decoded = atbash.decrypt(encoded)  # Returns: 'hello'

# Keyword cipher - keyword-based substitution
encrypted = keyword.encrypt("HELLO", "secret")  # Returns: 'dibbl'
decrypted = keyword.decrypt(encrypted, "secret")  # Returns: 'hello'

# Affine cipher - general form using E(x) = (ax + b) mod m
encrypted = affine.encrypt("HELLO", 5, 8)  # Returns: 'rclla'
decrypted = affine.decrypt(encrypted, 5, 8)  # Returns: 'hello'
# Note: 'a' must be coprime with alphabet length
```

### Cipher Relationships

The **Affine cipher** is the general form of all linear monoalphabetic substitution ciphers:
- **Caesar cipher**: Affine with `a=1, b=shift`
- **ROT13**: Caesar with `shift=13` (or Affine with `a=1, b=13`)
- **Atbash** (for English): Affine with `a=25, b=25`

### Custom Alphabets

All ciphers support custom alphabets by passing an `alphabet` parameter:

```python
# Turkish
alphabet_tr = "abcçdefgğhıijklmnoöprsştuüvyz"
caesar.encrypt("merhaba", 5, alphabet_tr)

# Russian (Cyrillic)
alphabet_ru = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
rot13.encrypt("привет", alphabet_ru)

# Digits
alphabet_digits = "0123456789"
atbash.encrypt("12345", alphabet_digits)

# Custom symbols
alphabet_custom = "!@#$%^&*()_+-=[]"
keyword.encrypt("!@#", "key", alphabet_custom)
```

See [ALPHABETS.md](ALPHABETS.md) for more examples and [examples/custom_alphabets.py](examples/custom_alphabets.py) for working code.

**Note:** All alphabets should be lowercase only. Input text is automatically converted to lowercase.

## Development

This library provides implementations of various cryptographic algorithms organized by type and era.

