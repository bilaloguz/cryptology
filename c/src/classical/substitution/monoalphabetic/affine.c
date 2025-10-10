/**
 * @file affine.c
 * @brief Affine Cipher implementation
 */

#include "cryptology/classical/substitution/monoalphabetic/affine.h"
#include <string.h>
#include <ctype.h>

#define DEFAULT_ALPHABET "abcdefghijklmnopqrstuvwxyz"

static int gcd(int a, int b) {
    while (b != 0) {
        int temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}

static int mod_inverse(int a, int m) {
    if (gcd(a, m) != 1) {
        return -1;  // No modular inverse exists
    }
    
    // Extended Euclidean Algorithm
    int m0 = m;
    int x0 = 0, x1 = 1;
    
    while (a > 1) {
        int q = a / m;
        int temp = m;
        m = a % m;
        a = temp;
        
        temp = x0;
        x0 = x1 - q * x0;
        x1 = temp;
    }
    
    if (x1 < 0) {
        x1 += m0;
    }
    
    return x1;
}

static int find_char_in_alphabet(char c, const char *alphabet) {
    const char *pos = strchr(alphabet, c);
    return pos ? (int)(pos - alphabet) : -1;
}

int affine_encrypt(const char *plaintext, int a, int b, const char *alphabet,
                   char *result, size_t result_size) {
    if (!plaintext || !result || result_size == 0) {
        return -1;
    }
    
    if (!alphabet) {
        alphabet = DEFAULT_ALPHABET;
    }
    
    size_t alphabet_len = strlen(alphabet);
    
    // Check that a is coprime with m
    if (gcd(a, (int)alphabet_len) != 1) {
        return -1;
    }
    
    size_t plaintext_len = strlen(plaintext);
    if (plaintext_len >= result_size) {
        return -1;
    }
    
    for (size_t i = 0; i < plaintext_len; i++) {
        char c = tolower((unsigned char)plaintext[i]);
        int pos = find_char_in_alphabet(c, alphabet);
        
        if (pos != -1) {
            // Apply affine transformation: E(x) = (ax + b) mod m
            int encrypted_pos = (a * pos + b) % (int)alphabet_len;
            if (encrypted_pos < 0) {
                encrypted_pos += alphabet_len;
            }
            result[i] = alphabet[encrypted_pos];
        } else {
            result[i] = plaintext[i];
        }
    }
    
    result[plaintext_len] = '\0';
    return 0;
}

int affine_decrypt(const char *ciphertext, int a, int b, const char *alphabet,
                   char *result, size_t result_size) {
    if (!ciphertext || !result || result_size == 0) {
        return -1;
    }
    
    if (!alphabet) {
        alphabet = DEFAULT_ALPHABET;
    }
    
    size_t alphabet_len = strlen(alphabet);
    
    // Check that a is coprime with m
    if (gcd(a, (int)alphabet_len) != 1) {
        return -1;
    }
    
    // Calculate modular inverse of a
    int a_inv = mod_inverse(a, (int)alphabet_len);
    if (a_inv == -1) {
        return -1;
    }
    
    size_t ciphertext_len = strlen(ciphertext);
    if (ciphertext_len >= result_size) {
        return -1;
    }
    
    for (size_t i = 0; i < ciphertext_len; i++) {
        char c = tolower((unsigned char)ciphertext[i]);
        int pos = find_char_in_alphabet(c, alphabet);
        
        if (pos != -1) {
            // Apply inverse affine transformation: D(y) = a^(-1) * (y - b) mod m
            int decrypted_pos = (a_inv * (pos - b)) % (int)alphabet_len;
            if (decrypted_pos < 0) {
                decrypted_pos += alphabet_len;
            }
            result[i] = alphabet[decrypted_pos];
        } else {
            result[i] = ciphertext[i];
        }
    }
    
    result[ciphertext_len] = '\0';
    return 0;
}

