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
│   │           ├── fractionated/      # Fractionated substitution
│   │           └── polyalphabetic/   # Multi-alphabet substitution
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
│   │               ├── fractionated/
│   │               └── polyalphabetic/
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

### Polyalphabetic Substitution Ciphers

1. **Alberti Cipher** - Disk-based polyalphabetic substitution
   - Uses two rotating disks (inner and outer alphabets)
   - Deterministic scrambled alphabet generation
   - Complex rotation strategies (fixed, content-based, mathematical, user-defined)
   - Custom alphabet support for both disks

2. **Vigenère Cipher** - Table-based polyalphabetic substitution
   - Uses tabula recta (classical Vigenère table) by default
   - `produce_table()` method for custom table generation
   - Support for classical, Caesar, Affine, Keyword, and Atbash-based tables
   - Random key generation with automatic key communication
   - English (26×26) and Turkish (29×29) table sizes

3. **Beaufort Cipher** - Self-reciprocal polyalphabetic substitution
   - Uses subtraction-based encryption: C = (K - P) mod alphabet_len
   - Self-reciprocal property: encryption and decryption use same algorithm
   - Same table generation strategies as Vigenère
   - Random key generation support
   - Enhanced security through subtraction operation

4. **Auto-key Cipher** - Self-extending key polyalphabetic substitution
   - Automatically extends key using plaintext itself
   - More secure than Vigenère due to key extension mechanism
   - Same table generation strategies as Vigenère
   - Random key generation support
   - Key extension makes frequency analysis more difficult

5. **Chaocipher** - Dynamic alphabet permutation cipher
   - Uses two rotating disks (left and right alphabets) that permute after each character
   - Self-reciprocal: encryption and decryption use identical algorithm
   - Deterministic alphabet generation (no random elements)
   - Support for custom alphabets using monoalphabetic `produce_alphabet()` methods
   - Enhanced security through dynamic alphabet changes

6. **Gronsfeld Cipher** - Numeric key variant of Vigenère
   - Uses numeric keys where each digit specifies a shift amount
   - Same table generation strategies as Vigenère (classical, Caesar, Affine, Keyword, Atbash)
   - Random numeric key generation support
   - Direct digit-to-shift mapping for simplified key management
   - Compatible with all alphabet sizes (26×26 for English, 29×29 for Turkish)

7. **Porta Cipher** - Self-reciprocal polyalphabetic substitution with custom pairing
   - Uses fixed alphabet pairs for substitution
   - Self-reciprocal: encryption and decryption use identical algorithm
   - **Custom pairing strategies**: Frequency-based, Atbash/Symmetric, Caesar-shifted, Affine-based
   - **Turkish alphabet support** with proper 14-pair system
   - **Balanced pairing** for arbitrary alphabet sizes
   - Random key generation with alphabetic keys
   - Enhanced security through flexible pair generation

## Composable Cipher System

The library features a revolutionary **composable cipher system** where monoalphabetic ciphers can produce custom alphabets that are then used by polygraphic, fractionated, and polyalphabetic ciphers:

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
python examples/alberti_example.py
python examples/vigenere_example.py
python examples/beaufort_example.py
python examples/autokey_example.py
python examples/chaocipher_example.py
python examples/gronsfeld_example.py
python examples/porta_example.py
python examples/porta_enhanced_example.py
python examples/custom_pairing_strategies.py
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

# Polyalphabetic ciphers
import cryptology.classical.substitution.polyalphabetic.vigenere as vigenere
encrypted = vigenere.encrypt("HELLO WORLD", "KEY")

import cryptology.classical.substitution.polyalphabetic.beaufort as beaufort
encrypted = beaufort.encrypt("HELLO WORLD", "KEY")

import cryptology.classical.substitution.polyalphabetic.autokey as autokey
encrypted = autokey.encrypt("HELLO WORLD", "KEY")

import cryptology.classical.substitution.polyalphabetic.chaocipher as chaocipher
encrypted = chaocipher.encrypt("HELLO WORLD", "KEY")

import cryptology.classical.substitution.polyalphabetic.gronsfeld as gronsfeld
encrypted = gronsfeld.encrypt("HELLO WORLD", "12345")

import cryptology.classical.substitution.polyalphabetic.porta as porta
encrypted = porta.encrypt("HELLO WORLD", "KEY")

# Custom pairing strategies for Porta
from cryptology.classical.substitution.polyalphabetic import porta_produce_pairs
pairs = porta_produce_pairs('frequency', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ')
encrypted = porta.encrypt("HELLO WORLD", "KEY", pairs=pairs)

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
make run-alberti
make run-vigenere
make run-beaufort
make run-autokey
make run-chaocipher
make run-gronsfeld
make run-porta
make run-composable
```

```c
#include "cryptology/classical/substitution/monoalphabetic/caesar.h"
#include "cryptology/classical/substitution/polygraphic/playfair.h"
#include "cryptology/classical/substitution/fractionated/bifid.h"
#include "cryptology/classical/substitution/polyalphabetic/vigenere.h"
#include "cryptology/classical/substitution/polyalphabetic/beaufort.h"
#include "cryptology/classical/substitution/polyalphabetic/autokey.h"
#include "cryptology/classical/substitution/polyalphabetic/chaocipher.h"
#include "cryptology/classical/substitution/polyalphabetic/gronsfeld.h"
#include "cryptology/classical/substitution/polyalphabetic/porta.h"

char encrypted[1024];
char caesar_alphabet[1024];

// Monoalphabetic
caesar_encrypt("Hello World", 3, NULL, encrypted, sizeof(encrypted));

// Polyalphabetic
vigenere_encrypt("HELLO WORLD", "KEY", NULL, NULL, encrypted, sizeof(encrypted));
beaufort_encrypt("HELLO WORLD", "KEY", NULL, NULL, encrypted, sizeof(encrypted));
autokey_encrypt("HELLO WORLD", "KEY", NULL, NULL, encrypted, sizeof(encrypted));
chaocipher_encrypt("HELLO WORLD", "KEY", NULL, NULL, encrypted, sizeof(encrypted));
gronsfeld_encrypt("HELLO WORLD", "12345", NULL, NULL, encrypted, sizeof(encrypted));
porta_encrypt("HELLO WORLD", "KEY", NULL, NULL, 0, encrypted, sizeof(encrypted));

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

### Polyalphabetic Ciphers
```bash
# Python
python examples/alberti_example.py
python examples/vigenere_example.py
python examples/vigenere_random_key_example.py
python examples/beaufort_example.py
python examples/autokey_example.py

# C
make run-alberti
make run-vigenere
make run-beaufort
make run-autokey
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

4. **Polyalphabetic Ciphers** - Multiple alphabet substitution
   - **Alberti**: Disk-based with rotation strategies
   - **Vigenère**: Table-based with tabula recta
   - **Beaufort**: Self-reciprocal subtraction-based
   - **Auto-key**: Self-extending key mechanism

### Composable System

All monoalphabetic ciphers can produce custom alphabets for use with polygraphic, fractionated, and polyalphabetic ciphers:

```
Monoalphabetic → Custom Alphabet → Polygraphic/Fractionated/Polyalphabetic
     ↓                ↓                    ↓
   Caesar         FGHIJKLMNOPQRSTUVWXYZABCDE    Playfair
   Keyword        SECRTABDFGHIJKLMNOPQUVWXYZ    Bifid
   Affine         FILORUXADGJMPSVYBEHKNQTWZC     Trifid
   Atbash         ZYXWVUTSRQPONMLKJIHGFEDCBA    Hill
                                                      Vigenère
                                                      Beaufort
                                                      Auto-key
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
- ✅ **7 Polyalphabetic** substitution ciphers
- ✅ **Composable system** for unlimited combinations
- ✅ **Custom alphabet support** (any language/character set)
- ✅ **Letter combination strategies** for non-English languages
- ✅ **Multi-language support** (English, Turkish, Russian, German, Spanish, French)
- ✅ **Comprehensive test suites** for all ciphers
- ✅ **Working examples** and documentation
- ✅ **Multi-language implementation** (Python & C)
- ✅ **Synchronized APIs** between Python and C
- ✅ **Custom pairing strategies** for Porta cipher
- ✅ **Turkish alphabet support** with proper pairing

## Custom Pairing Strategies (Porta Cipher)

The Porta cipher supports advanced custom pairing strategies for enhanced security:

### Available Strategies

1. **Frequency-Based Pairs** ⭐ **RECOMMENDED**
   - Pairs common letters with rare letters
   - Best resistance to frequency analysis
   - Example: `('E', 'Z'), ('T', 'Q'), ('A', 'X')`

2. **Atbash/Symmetric Pairs**
   - Mirror positions in alphabet
   - Educational purposes
   - Example: `('A', 'Z'), ('B', 'Y'), ('C', 'X')`

3. **Caesar-Shifted Pairs**
   - Mathematical shift patterns
   - Example: `('A', 'D'), ('B', 'E'), ('C', 'F')`

4. **Affine-Based Pairs**
   - Based on Affine cipher transformation
   - Multiple parameter sets (a=3,b=1), (a=5,b=2)
   - Example: `('A', 'D'), ('B', 'G'), ('C', 'J')`

### Usage Examples

```python
from cryptology.classical.substitution.polyalphabetic import porta_produce_pairs, porta_encrypt

# Generate frequency-based pairs
pairs = porta_produce_pairs('frequency', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ')
encrypted = porta_encrypt("HELLO WORLD", "KEY", pairs=pairs)

# Generate Affine-based pairs
pairs = porta_produce_pairs('affine', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', a=3, b=1)
encrypted = porta_encrypt("HELLO WORLD", "KEY", pairs=pairs)

# Turkish alphabet with proper pairing
turkish_pairs = porta_produce_pairs('turkish', 'ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ')
encrypted = porta_encrypt("MERHABA", "KEY", alphabet='ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ', pairs=turkish_pairs)
```

### Security Ranking

1. **🥇 Frequency-Based** - Best security (disrupts frequency patterns)
2. **🥈 Affine-Based** - Good security with mathematical foundation  
3. **🥉 Caesar-Shifted** - Moderate security
4. **⚠️ Atbash/Symmetric** - Educational only (predictable)

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