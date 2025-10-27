# Cryptology

A comprehensive multi-language library for classical cryptography algorithms, featuring advanced alphabet support, composable cipher systems, and extensive language compatibility.

## 🌟 Key Features

- **Multi-Language Support**: Complete implementations in Python and C
- **Advanced Alphabet System**: Centralized alphabet management with UTF-8 support
- **Composable Architecture**: Mix and match cipher components for enhanced security
- **Multi-Language Alphabets**: English, Turkish (with Q,W,X support), and custom alphabets
- **Flexible Square Sizing**: 5×5, 6×6, and 7×7 Polybius squares
- **Random Key Generation**: Cryptographically secure key generation for multiple ciphers
- **Comprehensive Testing**: Extensive test suites for all implementations

## 📁 Project Structure

```
cryptology/
├── python/                    # Python implementation
│   ├── cryptology/            # Main Python package
│   │   ├── alphabets.py       # Centralized alphabet system
│   │   └── classical/
│   │       └── substitution/
│   │           ├── monoalphabetic/     # Single-letter substitution
│   │           │   ├── caesar.py       # Caesar cipher
│   │           │   ├── rot13.py        # ROT13 cipher
│   │           │   ├── atbash.py      # Atbash cipher
│   │           │   ├── keyword.py     # Keyword cipher
│   │           │   └── affine.py      # Affine cipher
│   │           ├── polygraphic/        # Multi-letter substitution
│   │           │   ├── playfair.py    # Playfair cipher
│   │           │   ├── two_square.py  # Two Square cipher
│   │           │   ├── four_square.py # Four Square cipher
│   │           │   ├── hill.py        # Hill cipher
│   │           │   ├── monoalphabetic_squares.py  # Shared utilities
│   │           │   └── letter_combination_strategies.py
│   │           ├── fractionated/       # Fractionated substitution
│   │           │   ├── bifid.py       # Bifid cipher
│   │           │   └── trifid.py     # Trifid cipher
│   │           ├── polyalphabetic/    # Multi-alphabet substitution
│   │           │   ├── alberti.py     # Alberti cipher
│   │           │   ├── vigenere.py   # Vigenère cipher
│   │           │   ├── beaufort.py   # Beaufort cipher
│   │           │   ├── autokey.py    # Auto-key cipher
│   │           │   ├── chaocipher.py # Chaocipher
│   │           │   ├── gronsfeld.py  # Gronsfeld cipher
│   │           │   ├── porta.py      # Porta cipher
│   │           │   └── reihenschieber.py  # Reihenschieber cipher
│   │           └── composite/         # Multi-stage ciphers
│   │               ├── straddling_checkerboard.py  # Straddling Checkerboard
│   │               ├── nihilist.py   # Nihilist cipher
│   │               ├── adfgvx.py    # ADFGVX cipher
│   │               └── vic.py        # VIC cipher
│   ├── examples/              # Example programs
│   ├── tests/                 # Test suites
│   ├── pyproject.toml        # Python package configuration
│   └── README.md
│
├── c/                        # C implementation
│   ├── include/              # Header files
│   │   └── cryptology/
│   │       ├── alphabets.h   # Centralized alphabet system
│   │       └── classical/
│   │           └── substitution/
│   │               ├── monoalphabetic/
│   │               ├── polygraphic/
│   │               ├── fractionated/
│   │               ├── polyalphabetic/
│   │               └── composite/
│   ├── src/                  # Source files
│   │   ├── alphabets.c       # Alphabet system implementation
│   │   └── classical/
│   │       └── substitution/
│   │           ├── monoalphabetic/
│   │           ├── polygraphic/
│   │           ├── fractionated/
│   │           ├── polyalphabetic/
│   │           └── composite/
│   ├── examples/             # Example programs
│   ├── Makefile              # Build system
│   └── README.md
│
└── README.md                 # This file
```

## 🚀 Quick Start

### Python Installation

```bash
cd python
pip install -e .
```

### C Building

```bash
cd c
make
```

### Basic Usage

```python
# Python example
import cryptology.classical.substitution.monoalphabetic.caesar as caesar
import cryptology.alphabets as alphabets

# English encryption
encrypted = caesar.encrypt("hello world", 3)
decrypted = caesar.decrypt(encrypted, 3)

# Turkish encryption with UTF-8 support
turkish_text = "merhaba dünya"
encrypted_tr = caesar.encrypt(turkish_text, 5, alphabets.TURKISH_STANDARD)
decrypted_tr = caesar.decrypt(encrypted_tr, 5, alphabets.TURKISH_STANDARD)

# Foreign words with Q,W,X support
foreign_text = "washington quebec"
encrypted_foreign = caesar.encrypt(foreign_text, 3, alphabets.TURKISH_EXTENDED)
```

```c
// C example
#include <cryptology/classical/substitution/monoalphabetic/caesar.h>
#include <cryptology/alphabets.h>

int main() {
    char plaintext[] = "hello world";
    char encrypted[256];
    char decrypted[256];
    
    caesar_encrypt(plaintext, 3, encrypted);
    caesar_decrypt(encrypted, 3, decrypted);
    
    return 0;
}
```

## 🔤 Alphabet System

Our centralized alphabet system provides standardized, UTF-8 compatible alphabets for all ciphers:

### English Alphabets
- **Standard**: 26 letters (`abcdefghijklmnopqrstuvwxyz`)
- **With Digits**: 36 chars for 6×6 squares
- **7×7 Square**: 49 chars with practical symbols

### Turkish Alphabets
- **Standard**: 29 letters (`abcçdefgğhıijklmnoöprsştuüvyz`)
- **Extended**: 32 letters (includes Q,W,X for foreign words)
- **With Digits**: 36-42 chars for different square sizes
- **7×7 Square**: 49 chars with practical symbols

### Key Features
- **Lowercase Standardization**: All alphabets use lowercase letters
- **UTF-8 Support**: Full support for Turkish characters (ç, ğ, ı, ö, ş, ü)
- **Q,W,X Support**: Extended Turkish alphabet includes foreign letters
- **No Duplicates**: All alphabets are validated for uniqueness
- **Flexible Sizing**: Perfect fit for 5×5, 6×6, and 7×7 squares

## 🔐 Implemented Ciphers

### Monoalphabetic Substitution Ciphers

**Single-letter substitution with fixed alphabet mapping**

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

**Multi-letter substitution using Polybius squares**

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

**Letter-to-coordinate conversion with fractionation**

1. **Bifid Cipher** - 2D fractionation with 5×5 square
   - Converts letters to coordinates, fractionates them
   - Breaks frequency analysis patterns
   - Custom alphabet support with letter combination

2. **Trifid Cipher** - 3D fractionation with 3×3×3 cube
   - Uses 3D coordinates for maximum security
   - Enhanced fractionation technique
   - Custom alphabet support with letter combination

### Polyalphabetic Substitution Ciphers

**Multi-alphabet substitution with varying encryption**

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
   - Self-reciprocal property: encryption and decryption use same algorithm
   - Custom pairing strategies: default, frequency-based, symmetric, Caesar-shifted, Atbash-based, Affine-based, security-focused
   - Turkish alphabet support with proper handling of unpaired letters
   - Enhanced security through custom alphabet pair generation

8. **Reihenschieber Cipher** - Mechanical Vigenère cipher with progressive shifting
   - Uses mechanical slide-based encryption with progressive shifts
   - Multiple shift modes: fixed, progressive, custom
   - Shift directions: forward (default), backward
   - Custom shift patterns and mathematical sequences
   - Enhanced security through progressive key modification

### Composite Ciphers

**Multi-stage encryption combining multiple techniques**

1. **Straddling Checkerboard Cipher** - Substitution + fractionation
   - Uses a 10×3 grid to convert letters to 1 or 2 digits
   - Multiple layout strategies: alphabetical, frequency-based, vowel-consonant separation, keyword-based, custom
   - Followed by numeric key addition
   - Enhanced security through fractionation

2. **Nihilist Cipher** - Polybius square + numeric key addition
   - Uses Polybius square for letter-to-coordinate conversion
   - Multiple square types: standard, frequency, keyword, custom, Caesar, Atbash, Affine
   - Numeric key addition using modular arithmetic
   - Enhanced security through coordinate-based encryption

3. **ADFGVX Cipher** - Polybius square + columnar transposition
   - Uses 6×6 Polybius square for letter-to-coordinate conversion
   - Multiple square formation options: standard, Caesar, Atbash, Affine, keyword
   - Columnar transposition for additional security
   - UTF-8 support for Turkish characters
   - Enhanced security through multi-stage encryption

4. **VIC Cipher** - Complex multi-stage encryption
   - **Stage 1**: Polybius square substitution (6×6)
   - **Stage 2**: Fractionation (letters to digits)
   - **Stage 3**: Straddling checkerboard (digits to letters)
   - **Stage 4**: Columnar transposition (multiple passes)
   - **Stage 5**: Numeric key addition (modular arithmetic)
   - **Stage 6**: Chain addition (progressive key modification)
   - Multiple square types: standard, Caesar, Atbash, Affine, keyword
   - English and Turkish support with 7×7 squares
   - Random key generation for all stages
   - Maximum security through six-stage encryption

## 🔧 Advanced Features

### Composable Cipher System

Our composable architecture allows mixing and matching cipher components:

```python
# Create custom alphabet using monoalphabetic cipher
import cryptology.classical.substitution.monoalphabetic.caesar as caesar
import cryptology.classical.substitution.polygraphic.playfair as playfair

# Generate Caesar-shifted alphabet
custom_alphabet = caesar.produce_alphabet(5)  # Shift by 5

# Use custom alphabet in Playfair
encrypted = playfair.encrypt("hello", "secret", alphabet=custom_alphabet)
```

### Random Key Generation

Multiple ciphers support cryptographically secure random key generation:

```python
# Vigenère with random key
import cryptology.classical.substitution.polyalphabetic.vigenere as vigenere

encrypted, generated_key = vigenere.encrypt_with_random_key("hello", key_length=10)
decrypted = vigenere.decrypt(encrypted, generated_key)
```

### Square Formation Options

Polybius-based ciphers support multiple square generation methods:

- **Standard**: Alphabetical arrangement
- **Frequency**: Most frequent letters prioritized
- **Keyword**: Custom arrangement based on keyword
- **Custom**: User-defined alphabet arrangement
- **Caesar**: Caesar-shifted alphabet
- **Atbash**: Reversed alphabet
- **Affine**: Affine-transformed alphabet

### Multi-Language Support

Full support for multiple languages with proper UTF-8 handling:

```python
# Turkish with foreign words
import cryptology.alphabets as alphabets

# Standard Turkish (29 letters)
turkish_standard = alphabets.TURKISH_STANDARD

# Extended Turkish (32 letters, includes Q,W,X)
turkish_extended = alphabets.TURKISH_EXTENDED

# 7×7 square for composite ciphers
turkish_7x7 = alphabets.TURKISH_EXTENDED_FULL_SQUARE
```

## 📊 Alphabet Specifications

| Alphabet Type | English | Turkish Standard | Turkish Extended |
|---------------|---------|------------------|------------------|
| **Letters** | 26 | 29 | 32 |
| **6×6 Square** | 36 chars | 36 chars | 42 chars |
| **7×7 Square** | 49 chars | - | 49 chars |
| **Q,W,X Support** | ✅ | ❌ | ✅ |
| **UTF-8 Support** | ✅ | ✅ | ✅ |

## 🧪 Testing

Comprehensive test suites ensure reliability:

```bash
# Python tests
cd python
python -m pytest tests/

# C tests
cd c
make test

# Comprehensive alphabet system tests
python test_focused_ciphers.py
```

## 📚 Examples

### Basic Encryption

```python
# Caesar cipher
import cryptology.classical.substitution.monoalphabetic.caesar as caesar
encrypted = caesar.encrypt("hello world", 3)
decrypted = caesar.decrypt(encrypted, 3)

# Vigenère cipher
import cryptology.classical.substitution.polyalphabetic.vigenere as vigenere
encrypted = vigenere.encrypt("hello world", "secret")
decrypted = vigenere.decrypt(encrypted, "secret")
```

### Advanced Usage

```python
# VIC cipher with custom square
import cryptology.classical.substitution.composite.vic as vic

encrypted = vic.vic_encrypt(
    "hello world",
    polybius_key="secret",
    checkerboard_key="key",
    transposition_key="cipher",
    numeric_key="12345",
    square_type="caesar",
    language="english"
)
```

### Turkish Support

```python
# Turkish encryption
import cryptology.alphabets as alphabets

turkish_text = "merhaba dünya"
encrypted = caesar.encrypt(turkish_text, 5, alphabets.TURKISH_STANDARD)
decrypted = caesar.decrypt(encrypted, 5, alphabets.TURKISH_STANDARD)

# Foreign words with Q,W,X
foreign_text = "washington quebec"
encrypted_foreign = caesar.encrypt(foreign_text, 3, alphabets.TURKISH_EXTENDED)
```

## 🔒 Security Features

- **Cryptographically Secure Random**: Uses `secrets` module for key generation
- **UTF-8 Safety**: Proper handling of multi-byte characters
- **Input Validation**: Comprehensive input sanitization
- **Memory Safety**: C implementation with proper memory management
- **No Side Channels**: Constant-time operations where applicable

## 🌍 Language Support

- **English**: Full support with 26-letter alphabet
- **Turkish**: Full support with 29-letter alphabet + UTF-8
- **Extended Turkish**: 32-letter alphabet including Q,W,X for foreign words
- **Custom Alphabets**: Support for any alphabet specification

## 📖 Documentation

- **Python**: Comprehensive docstrings and type hints
- **C**: Detailed header documentation
- **Examples**: Extensive example programs for all ciphers
- **Tests**: Complete test coverage for all functionality

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure both Python and C implementations are synchronized
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🎯 Roadmap

- [ ] Great Cipher implementation (17th century nomenclator)
- [ ] Additional language support
- [ ] Performance optimizations
- [ ] Web interface
- [ ] Mobile applications

---

**Cryptology** - Comprehensive classical cryptography library with advanced alphabet support and composable architecture.