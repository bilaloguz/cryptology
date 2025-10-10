/**
 * @file atbash.c
 * @brief Atbash Cipher implementation
 */

#include "cryptology/classical/substitution/monoalphabetic/atbash.h"
#include <string.h>
#include <ctype.h>

#define DEFAULT_ALPHABET "abcdefghijklmnopqrstuvwxyz"

static int find_char_in_alphabet(char c, const char *alphabet) {
    const char *pos = strchr(alphabet, c);
    return pos ? (int)(pos - alphabet) : -1;
}

int atbash_encrypt(const char *plaintext, const char *alphabet,
                   char *result, size_t result_size) {
    if (!plaintext || !result || result_size == 0) {
        return -1;
    }
    
    if (!alphabet) {
        alphabet = DEFAULT_ALPHABET;
    }
    
    size_t alphabet_len = strlen(alphabet);
    size_t plaintext_len = strlen(plaintext);
    
    if (plaintext_len >= result_size) {
        return -1;
    }
    
    for (size_t i = 0; i < plaintext_len; i++) {
        char c = tolower((unsigned char)plaintext[i]);
        int pos = find_char_in_alphabet(c, alphabet);
        
        if (pos != -1) {
            // Character is in alphabet - reverse position
            int reversed_pos = alphabet_len - 1 - pos;
            result[i] = alphabet[reversed_pos];
        } else {
            // Character not in alphabet - keep unchanged
            result[i] = plaintext[i];
        }
    }
    
    result[plaintext_len] = '\0';
    return 0;
}

int atbash_decrypt(const char *ciphertext, const char *alphabet,
                   char *result, size_t result_size) {
    // Atbash is symmetric - encrypt and decrypt are the same
    return atbash_encrypt(ciphertext, alphabet, result, result_size);
}

