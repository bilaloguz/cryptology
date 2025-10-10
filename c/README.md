# Cryptology - C Implementation

A comprehensive C library for classical cryptography algorithms.

## Structure

```
c/
├── include/
│   └── cryptology/
│       └── classical/
│           └── substitution/
│               └── monoalphabetic/
│                   ├── caesar.h
│                   ├── rot13.h
│                   ├── atbash.h
│                   ├── keyword.h
│                   └── affine.h
├── src/
│   └── classical/
│       └── substitution/
│           └── monoalphabetic/
│               ├── caesar.c
│               ├── rot13.c
│               ├── atbash.c
│               ├── keyword.c
│               └── affine.c
├── examples/
│   ├── example.c
│   └── custom_alphabets.c
├── Makefile
└── README.md
```

## Building

```bash
# Build library and examples
make

# Build only library
make build/lib/libcryptology.a

# Build only examples
make examples

# Clean build artifacts
make clean
```

## Usage

### Include Headers

```c
#include "cryptology/classical/substitution/monoalphabetic/caesar.h"
#include "cryptology/classical/substitution/monoalphabetic/rot13.h"
#include "cryptology/classical/substitution/monoalphabetic/atbash.h"
#include "cryptology/classical/substitution/monoalphabetic/keyword.h"
#include "cryptology/classical/substitution/monoalphabetic/affine.h"
```

### Caesar Cipher

```c
char encrypted[1024];
char decrypted[1024];

// Encrypt with default English alphabet
caesar_encrypt("Hello World", 3, NULL, encrypted, sizeof(encrypted));
caesar_decrypt(encrypted, 3, NULL, decrypted, sizeof(decrypted));

// Encrypt with custom alphabet
const char *alphabet = "abcdefghijklmnopqrstuvwxyz";
caesar_encrypt("hello", 3, alphabet, encrypted, sizeof(encrypted));
```

### ROT13 Cipher

```c
char encrypted[1024];

// Encrypt (shifts by half the alphabet)
rot13_encrypt("Hello", NULL, encrypted, sizeof(encrypted));

// Decrypt (same as encrypt - symmetric)
rot13_decrypt(encrypted, NULL, decrypted, sizeof(decrypted));
```

### Atbash Cipher

```c
char encrypted[1024];

// Encrypt (reverses alphabet)
atbash_encrypt("Hello", NULL, encrypted, sizeof(encrypted));

// Decrypt (same as encrypt - symmetric)
atbash_decrypt(encrypted, NULL, decrypted, sizeof(decrypted));
```

### Keyword Cipher

```c
char encrypted[1024];

keyword_encrypt("Hello", "secret", NULL, encrypted, sizeof(encrypted));
keyword_decrypt(encrypted, "secret", NULL, decrypted, sizeof(decrypted));
```

### Affine Cipher

```c
char encrypted[1024];

// E(x) = (ax + b) mod m
// 'a' must be coprime with alphabet length
affine_encrypt("Hello", 5, 8, NULL, encrypted, sizeof(encrypted));
affine_decrypt(encrypted, 5, 8, NULL, decrypted, sizeof(decrypted));
```

## Custom Alphabets

All functions accept a custom alphabet string:

```c
// Digits
const char *digits = "0123456789";
caesar_encrypt("12345", 3, digits, encrypted, sizeof(encrypted));

// Hexadecimal
const char *hex = "0123456789abcdef";
rot13_encrypt("deadbeef", hex, encrypted, sizeof(encrypted));

// Custom symbols
const char *symbols = "!@#$%^&*()_+-=[]";
atbash_encrypt("!@#$", symbols, encrypted, sizeof(encrypted));
```

## Running Examples

```bash
# Main example
make run-example

# Custom alphabets example
make run-custom
```

## API Reference

All encrypt/decrypt functions follow this pattern:

```c
int cipher_encrypt(const char *plaintext, /* parameters */, const char *alphabet,
                   char *result, size_t result_size);

int cipher_decrypt(const char *ciphertext, /* parameters */, const char *alphabet,
                   char *result, size_t result_size);
```

**Returns:**
- `0` on success
- `-1` on error (invalid parameters, buffer too small, invalid keys for affine)

**Notes:**
- If `alphabet` is `NULL`, uses default English alphabet: `"abcdefghijklmnopqrstuvwxyz"`
- All input is converted to lowercase
- Characters not in alphabet are left unchanged
- For Affine cipher, `a` must be coprime with alphabet length

## Cipher Relationships

The **Affine cipher** is the general form of all linear monoalphabetic substitution ciphers:
- **Caesar cipher**: Affine with `a=1, b=shift`
- **ROT13**: Caesar with `shift=13` (or Affine with `a=1, b=13`)
- **Atbash** (for English): Affine with `a=25, b=25`

## License

See root LICENSE file.

