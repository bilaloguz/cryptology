# Cryptology

A comprehensive Python library for classical and modern cryptography algorithms.

## Structure

```
cryptology/
├── cryptology/
│   └── classical/
│       └── substitution/
│           ├── monoalphabetic/
│           │   ├── caesar.py
│           │   ├── rot13.py
│           │   ├── atbash.py
│           │   ├── keyword.py
│           │   └── affine.py
│           ├── polygraphic/
│           │   ├── playfair.py
│           │   ├── two_square.py
│           │   ├── four_square.py
│           │   └── hill.py
│           ├── fractionated/
│           │   ├── bifid.py
│           │   └── trifid.py
│           └── polyalphabetic/
│               ├── alberti.py
│               ├── vigenere.py
│               ├── beaufort.py
│               ├── autokey.py
│               ├── chaocipher.py
│               ├── gronsfeld.py
│               └── porta.py
├── examples/
│   ├── custom_alphabets.py
│   ├── polygraphic_example.py
│   ├── fractionated_example.py
│   ├── alberti_example.py
│   ├── vigenere_example.py
│   ├── beaufort_example.py
│   ├── autokey_example.py
│   ├── chaocipher_example.py
│   ├── gronsfeld_example.py
│   ├── porta_example.py
│   ├── porta_enhanced_example.py
│   ├── custom_pairing_strategies.py
│   └── composable_ciphers.py
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

### Polyalphabetic Substitution Ciphers

```python
import cryptology.classical.substitution.polyalphabetic.vigenere as vigenere
import cryptology.classical.substitution.polyalphabetic.beaufort as beaufort
import cryptology.classical.substitution.polyalphabetic.autokey as autokey
import cryptology.classical.substitution.polyalphabetic.chaocipher as chaocipher
import cryptology.classical.substitution.polyalphabetic.gronsfeld as gronsfeld
import cryptology.classical.substitution.polyalphabetic.porta as porta

# Vigenère cipher - table-based polyalphabetic substitution
encrypted = vigenere.encrypt("HELLO WORLD", "KEY")
decrypted = vigenere.decrypt(encrypted, "KEY")

# Beaufort cipher - self-reciprocal subtraction-based
encrypted = beaufort.encrypt("HELLO WORLD", "KEY")
decrypted = beaufort.decrypt(encrypted, "KEY")  # Same as encrypt

# Auto-key cipher - self-extending key
encrypted = autokey.encrypt("HELLO WORLD", "KEY")
decrypted = autokey.decrypt(encrypted, "KEY")

# Chaocipher - dynamic alphabet permutation
encrypted = chaocipher.encrypt("HELLO WORLD", "KEY")
decrypted = chaocipher.decrypt(encrypted, "KEY")  # Same as encrypt

# Gronsfeld cipher - numeric key variant of Vigenère
encrypted = gronsfeld.encrypt("HELLO WORLD", "12345")
decrypted = gronsfeld.decrypt(encrypted, "12345")

# Porta cipher - self-reciprocal with custom pairing
encrypted = porta.encrypt("HELLO WORLD", "KEY")
decrypted = porta.decrypt(encrypted, "KEY")  # Same as encrypt

# Custom pairing strategies for Porta
from cryptology.classical.substitution.polyalphabetic import porta_produce_pairs
pairs = porta_produce_pairs('frequency', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ')
encrypted = porta.encrypt("HELLO WORLD", "KEY", pairs=pairs)
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

