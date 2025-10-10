# Alphabet Guide - C Implementation

This guide shows how to use custom alphabets with the cryptology C library.

## Using Custom Alphabets

All cipher functions accept an optional `alphabet` parameter (pass `NULL` for default English):

### English (Default)

```c
#include "cryptology/classical/substitution/monoalphabetic/caesar.h"

char encrypted[1024];

// Default English alphabet (lowercase)
caesar_encrypt("hello", 3, NULL, encrypted, sizeof(encrypted));

// Or explicitly specify
const char *alphabet_en = "abcdefghijklmnopqrstuvwxyz";
caesar_encrypt("hello", 3, alphabet_en, encrypted, sizeof(encrypted));
```

### Digits

```c
#include "cryptology/classical/substitution/monoalphabetic/caesar.h"

const char *alphabet_digits = "0123456789";
char encrypted[1024];

caesar_encrypt("12345", 3, alphabet_digits, encrypted, sizeof(encrypted));
```

### Hexadecimal

```c
#include "cryptology/classical/substitution/monoalphabetic/rot13.h"

const char *alphabet_hex = "0123456789abcdef";
char encrypted[1024];

rot13_encrypt("deadbeef", alphabet_hex, encrypted, sizeof(encrypted));
```

### Custom Symbols

```c
#include "cryptology/classical/substitution/monoalphabetic/atbash.h"

const char *alphabet_custom = "!@#$%^&*()_+-=[]{}|;:,.<>?";
char encrypted[1024];

atbash_encrypt("!@#$", alphabet_custom, encrypted, sizeof(encrypted));
```

## Complete Example

```c
#include <stdio.h>
#include "cryptology/classical/substitution/monoalphabetic/caesar.h"
#include "cryptology/classical/substitution/monoalphabetic/affine.h"

int main() {
    char encrypted[1024];
    char decrypted[1024];
    
    // Digits alphabet
    const char *digits = "0123456789";
    const char *plaintext = "20231015";
    
    // Caesar cipher
    caesar_encrypt(plaintext, 3, digits, encrypted, sizeof(encrypted));
    printf("Caesar: %s -> %s\n", plaintext, encrypted);
    
    // Affine cipher (for m=10, valid a: 1, 3, 7, 9)
    affine_encrypt(plaintext, 3, 7, digits, encrypted, sizeof(encrypted));
    affine_decrypt(encrypted, 3, 7, digits, decrypted, sizeof(decrypted));
    printf("Affine: %s -> %s -> %s\n", plaintext, encrypted, decrypted);
    
    return 0;
}
```

## Important Notes

1. **Lowercase Only**: All alphabets should be lowercase. Input text is automatically converted to lowercase.

2. **No Duplicates**: Alphabets should not contain duplicate characters.

3. **Consistent Usage**: Use the same alphabet for both encryption and decryption.

4. **Buffer Size**: Ensure result buffer is large enough (at least `strlen(plaintext) + 1`).

5. **Affine Cipher Constraint**: For the Affine cipher, the multiplicative key `a` must be coprime with the alphabet length.
   - For m=26 (English): valid a = 1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25
   - For m=10 (digits): valid a = 1, 3, 7, 9
   - For m=16 (hex): valid a = 1, 3, 5, 7, 9, 11, 13, 15

## Error Handling

All functions return:
- `0` on success
- `-1` on error

Check return values:

```c
if (caesar_encrypt(text, 3, alphabet, result, sizeof(result)) != 0) {
    fprintf(stderr, "Encryption failed\n");
    return 1;
}
```

## See Also

- [README.md](README.md) - Main documentation
- [examples/custom_alphabets.c](examples/custom_alphabets.c) - Working code examples

