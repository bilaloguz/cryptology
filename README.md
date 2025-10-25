# Cryptology

A comprehensive multi-language library for classical and modern cryptography algorithms.

## Overview

This project provides implementations of various cryptographic algorithms in multiple programming languages. Currently supports:
- **Python** - Complete implementation with tests and examples
- **C** - Complete implementation with tests and examples

## Project Structure

```
cryptology/
├── python/              # Python implementation
│   ├── cryptology/      # Main Python package
│   │   └── classical/
│   │       └── substitution/
│   │           └── monoalphabetic/
│   │               ├── caesar.py
│   │               ├── rot13.py
│   │               ├── atbash.py
│   │               ├── keyword.py
│   │               └── affine.py
│   ├── examples/
│   ├── tests/
│   └── README.md
│
├── c/                   # C implementation
│   ├── include/
│   │   └── cryptology/
│   │       └── classical/
│   │           └── substitution/
│   │               └── monoalphabetic/
│   │                   ├── caesar.h
│   │                   ├── rot13.h
│   │                   ├── atbash.h
│   │                   ├── keyword.h
│   │                   └── affine.h
│   ├── src/
│   ├── examples/
│   ├── Makefile
│   └── README.md
│
└── README.md            # This file
```

## Implemented Ciphers

### Monoalphabetic Substitution Ciphers

1. **Caesar Cipher** - Shift-based substitution
   - Shifts each letter by a fixed number of positions

2. **ROT13** - Fixed shift of 13 (half alphabet)
   - Special case of Caesar where applying twice returns original

3. **Atbash** - Alphabet reversal
   - First letter maps to last, second to second-to-last, etc.

4. **Keyword Cipher** - Keyword-based substitution
   - Uses a keyword to create the cipher alphabet

5. **Affine Cipher** - General linear form
   - Uses formula E(x) = (ax + b) mod m
   - General form of all linear monoalphabetic substitution ciphers

## Quick Start

### Python

```bash
cd python
pip install -e .
python example.py
```

```python
import cryptology.classical.substitution.monoalphabetic.caesar as caesar

encrypted = caesar.encrypt("HELLO", 3)  # Returns: 'khoor'
decrypted = caesar.decrypt(encrypted, 3)  # Returns: 'hello'
```

### C

```bash
cd c
make
./build/bin/example
```

```c
#include "cryptology/classical/substitution/monoalphabetic/caesar.h"

char encrypted[1024];
char decrypted[1024];

caesar_encrypt("Hello World", 3, NULL, encrypted, sizeof(encrypted));
caesar_decrypt(encrypted, 3, NULL, decrypted, sizeof(decrypted));
```

## Custom Alphabets

Both implementations support custom alphabets for any language or character set:

**Python:**
```python
# Turkish
alphabet_tr = "abcçdefgğhıijklmnoöprsştuüvyz"
caesar.encrypt("merhaba", 5, alphabet_tr)

# Digits
alphabet_digits = "0123456789"
rot13.encrypt("12345", alphabet_digits)
```

**C:**
```c
// Digits
const char *digits = "0123456789";
caesar_encrypt("12345", 3, digits, encrypted, sizeof(encrypted));

// Hexadecimal
const char *hex = "0123456789abcdef";
rot13_encrypt("deadbeef", hex, encrypted, sizeof(encrypted));
```

See language-specific ALPHABETS.md for detailed examples.

## Cipher Relationships

The **Affine cipher** is the general form of all linear monoalphabetic substitution ciphers:
- **Caesar cipher**: Affine with `a=1, b=shift`
- **ROT13**: Caesar with `shift=13` (or Affine with `a=1, b=13`)
- **Atbash** (for English): Affine with `a=25, b=25`

## Documentation

- [Python README](python/README.md) - Python-specific documentation
- [Python ALPHABETS.md](python/ALPHABETS.md) - Python custom alphabet guide
- [C README](c/README.md) - C-specific documentation
- [C ALPHABETS.md](c/ALPHABETS.md) - C custom alphabet guide

## Development

### Python
```bash
cd python
pip install -e .
pytest tests/
```

### C
```bash
cd c
make
make run-example
```

## Features

- ✅ 5 monoalphabetic substitution ciphers
- ✅ Custom alphabet support (any language/character set)
- ✅ Lowercase-only implementation
- ✅ Comprehensive test suites
- ✅ Working examples and documentation
- ✅ Multi-language support (Python & C)

## License
GPL v3

## Contributing

Contributions are welcome! Please feel free to submit pull requests.
