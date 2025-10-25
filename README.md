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
│   │           ├── monoalphabetic/    # Single-letter substitution
│   │           ├── polygraphic/       # Multi-letter substitution
│   │           └── fractionated/      # Fractionated substitution
│   ├── examples/
│   ├── tests/
│   └── README.md
│
├── c/                   # C implementation
│   ├── include/
│   │   └── cryptology/
│   │       └── classical/
│   │           └── substitution/
│   │               ├── monoalphabetic/
│   │               ├── polygraphic/
│   │               └── fractionated/
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
   - `produce_alphabet()` method for composable system

2. **ROT13** - Fixed shift of 13 (half alphabet)
   - Special case of Caesar where applying twice returns original

3. **Atbash** - Alphabet reversal
   - First letter maps to last, second to second-to-last, etc.
   - `produce_alphabet()` method for composable system

4. **Keyword Cipher** - Keyword-based substitution
   - Uses a keyword to create the cipher alphabet
   - `produce_alphabet()` method for composable system

5. **Affine Cipher** - General linear form
   - Uses formula E(x) = (ax + b) mod m
   - General form of all linear monoalphabetic substitution ciphers
   - `produce_alphabet()` method for composable system

### Polygraphic Substitution Ciphers

1. **Playfair Cipher** - 5×5 square with digram substitution
   - Uses a 5×5 Polybius square for encryption
   - Custom alphabet support with dynamic square sizing
   - Letter combination strategies for non-English languages

2. **Two Square Cipher** - Two 5×5 squares for encryption
   - Uses two separate Polybius squares
   - Enhanced security through dual-square approach

3. **Four Square Cipher** - Four 5×5 squares for encryption
   - Uses four Polybius squares in a 2×2 grid
   - Maximum security for polygraphic substitution

4. **Hill Cipher** - Matrix-based substitution
   - Uses matrix multiplication for encryption
   - Requires invertible key matrix

### Fractionated Substitution Ciphers

1. **Bifid Cipher** - 2D fractionation with 5×5 square
   - Converts letters to coordinates, fractionates them
   - Breaks frequency analysis patterns
   - Custom alphabet support with letter combination

2. **Trifid Cipher** - 3D fractionation with 3×3×3 cube
   - Uses 3D coordinates for maximum security
   - Enhanced fractionation technique
   - Custom alphabet support with letter combination

## Composable Cipher System

The library features a revolutionary **composable cipher system** where monoalphabetic ciphers can produce custom alphabets that are then used by polygraphic and fractionated ciphers:

```python
# Layer 1: Caesar produces custom alphabet
caesar_alphabet = caesar.produce_alphabet(shift=5)

# Layer 2: Keyword rearranges Caesar alphabet  
keyword_alphabet = keyword.produce_alphabet("SECRET", caesar_alphabet)

# Layer 3: Bifid uses keyword alphabet with fractionation
encrypted = bifid.encrypt("SECRET MESSAGE", "FRACTIONATED", keyword_alphabet)

# Layer 4: Trifid uses same alphabet with 3D fractionation
encrypted = trifid.encrypt("SECRET MESSAGE", "FRACTIONATED", keyword_alphabet)
```

This creates **unlimited combinations** of encryption layers for maximum security!

## Custom Alphabet Support

### Multi-Language Support

Both implementations support custom alphabets for any language:

**English (26 letters):**
```python
alphabet_en = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
```

**Turkish (29 letters):**
```python
alphabet_tr = "ABCÇDEFGĞHIJKLMNOÖPRSŞTUÜVYZ"
```

**Russian (33 letters):**
```python
alphabet_ru = "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
```

**German (30 letters):**
```python
alphabet_de = "ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜß"
```

### Letter Combination Strategies

For languages with more letters than standard squares (25 for 5×5), the library automatically:

1. **Detects language** (Turkish, Russian, German, etc.)
2. **Applies combination rules** (ç→c, ğ→g, etc.)
3. **Uses frequency data** to select most important letters
4. **Creates optimal squares** for each cipher type

## Quick Start

### Python

```bash
cd python
pip install -e .
python examples/polygraphic_example.py
python examples/fractionated_example.py
python examples/composable_ciphers.py
```

```python
# Monoalphabetic ciphers
import cryptology.classical.substitution.monoalphabetic.caesar as caesar
encrypted = caesar.encrypt("HELLO", 3)  # Returns: 'khoor'

# Polygraphic ciphers
import cryptology.classical.substitution.polygraphic.playfair as playfair
encrypted = playfair.encrypt("HELLO WORLD", "MONARCHY")

# Fractionated ciphers
import cryptology.classical.substitution.fractionated.bifid as bifid
encrypted = bifid.encrypt("HELLO WORLD", "MONARCHY")

# Composable system
caesar_alphabet = caesar.produce_alphabet(5)
encrypted = playfair.encrypt("HELLO", "KEY", caesar_alphabet)
```

### C

```bash
cd c
make
make run-polygraphic
make run-fractionated
make run-composable
```

```c
#include "cryptology/classical/substitution/monoalphabetic/caesar.h"
#include "cryptology/classical/substitution/polygraphic/playfair.h"
#include "cryptology/classical/substitution/fractionated/bifid.h"

char encrypted[1024];
char caesar_alphabet[1024];

// Monoalphabetic
caesar_encrypt("Hello World", 3, NULL, encrypted, sizeof(encrypted));

// Composable system
caesar_produce_alphabet(5, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", caesar_alphabet, sizeof(caesar_alphabet));
playfair_encrypt_with_alphabet("HELLO", "KEY", caesar_alphabet, encrypted, sizeof(encrypted));
bifid_encrypt_with_alphabet("HELLO", "KEY", caesar_alphabet, encrypted, sizeof(encrypted));
```

## Advanced Features

### Security Enhancements

1. **Fractionation** - Breaks frequency analysis patterns
2. **Custom Alphabets** - Support for any language
3. **Letter Combination** - Intelligent handling of non-English characters
4. **Multi-Layer Encryption** - Unlimited cipher combinations
5. **Dynamic Sizing** - Automatic square/cube sizing based on alphabet

### Language-Specific Optimizations

- **Turkish**: ç→c, ğ→g, ı→i, ö→o, ş→s, ü→u
- **Russian**: ё→е, й→и, ъ→'', ь→''
- **German**: ä→a, ö→o, ü→u, ß→s
- **Spanish**: ñ→n, á→a, é→e, í→i, ó→o, ú→u
- **French**: à→a, â→a, é→e, è→e, ç→c, etc.

## Examples

### Polygraphic Ciphers
```bash
# Python
python examples/polygraphic_example.py
python examples/polygraphic_custom_alphabets.py

# C
make run-polygraphic
```

### Fractionated Ciphers
```bash
# Python
python examples/fractionated_example.py

# C
make run-fractionated
```

### Composable System
```bash
# Python
python examples/composable_ciphers.py

# C
make run-composable
```

### Letter Combination Strategies
```bash
# Python
python examples/letter_combination_demo.py
python examples/letter_combination_test.py
```

## Cipher Relationships

### Mathematical Hierarchy

1. **Affine Cipher** - General form of all linear monoalphabetic substitution ciphers
   - **Caesar**: Affine with `a=1, b=shift`
   - **ROT13**: Caesar with `shift=13`
   - **Atbash** (English): Affine with `a=25, b=25`

2. **Polygraphic Ciphers** - Multi-letter substitution
   - **Playfair**: 5×5 square with digram rules
   - **Two Square**: Two 5×5 squares
   - **Four Square**: Four 5×5 squares
   - **Hill**: Matrix-based substitution

3. **Fractionated Ciphers** - Coordinate fractionation
   - **Bifid**: 2D fractionation (rows, columns)
   - **Trifid**: 3D fractionation (layers, rows, columns)

### Composable System

All monoalphabetic ciphers can produce custom alphabets for use with polygraphic and fractionated ciphers:

```
Monoalphabetic → Custom Alphabet → Polygraphic/Fractionated
     ↓                ↓                    ↓
   Caesar         FGHIJKLMNOPQRSTUVWXYZABCDE    Playfair
   Keyword        SECRTABDFGHIJKLMNOPQUVWXYZ    Bifid
   Affine         FILORUXADGJMPSVYBEHKNQTWZC     Trifid
   Atbash         ZYXWVUTSRQPONMLKJIHGFEDCBA    Hill
```

## Documentation

- [Python README](python/README.md) - Python-specific documentation
- [C README](c/README.md) - C-specific documentation
- [Examples](python/examples/) - Comprehensive examples
- [Tests](python/tests/) - Complete test suites

## Development

### Python
```bash
cd python
pip install -e .
pytest tests/
python examples/polygraphic_example.py
python examples/fractionated_example.py
python examples/composable_ciphers.py
```

### C
```bash
cd c
make
make run-example
make run-polygraphic
make run-fractionated
make run-composable
```

## Features

- ✅ **5 Monoalphabetic** substitution ciphers
- ✅ **4 Polygraphic** substitution ciphers  
- ✅ **2 Fractionated** substitution ciphers
- ✅ **Composable system** for unlimited combinations
- ✅ **Custom alphabet support** (any language/character set)
- ✅ **Letter combination strategies** for non-English languages
- ✅ **Multi-language support** (English, Turkish, Russian, German, Spanish, French)
- ✅ **Comprehensive test suites** for all ciphers
- ✅ **Working examples** and documentation
- ✅ **Multi-language implementation** (Python & C)
- ✅ **Synchronized APIs** between Python and C

## Security Analysis

### Classical Ciphers
- **Monoalphabetic**: Vulnerable to frequency analysis
- **Polygraphic**: Resistant to simple frequency analysis
- **Fractionated**: Highly resistant to frequency analysis

### Modern Applications
- **Educational**: Understanding classical cryptography
- **Steganography**: Hiding messages in plain sight
- **Multi-layer security**: Combining multiple cipher types
- **Language support**: International communication security

## License
GPL v3

## Contributing

Contributions are welcome! Please feel free to submit pull requests.

## Acknowledgments

This library implements classical cryptographic algorithms for educational and research purposes. All algorithms are well-documented with historical context and security analysis.