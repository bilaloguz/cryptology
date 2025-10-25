/**
 * @file caesar.c
 * @brief Caesar Cipher implementation
 */

#include "cryptology/classical/substitution/monoalphabetic/caesar.h"
#include <string.h>
#include <ctype.h>

#define DEFAULT_ALPHABET "abcdefghijklmnopqrstuvwxyz"

static int find_char_in_alphabet(char c, const char *alphabet) {
    const char *pos = strchr(alphabet, c);
    return pos ? (int)(pos - alphabet) : -1;
}

int caesar_encrypt(const char *plaintext, int shift, const char *alphabet,
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
    
    // Normalize shift to be positive
    shift = ((shift % (int)alphabet_len) + (int)alphabet_len) % (int)alphabet_len;
    
    for (size_t i = 0; i < plaintext_len; i++) {
        char c = tolower((unsigned char)plaintext[i]);
        int pos = find_char_in_alphabet(c, alphabet);
        
        if (pos != -1) {
            // Character is in alphabet - shift it
            int new_pos = (pos + shift) % alphabet_len;
            result[i] = alphabet[new_pos];
        } else {
            // Character not in alphabet - keep unchanged
            result[i] = plaintext[i];
        }
    }
    
    result[plaintext_len] = '\0';
    return 0;
}

int caesar_decrypt(const char *ciphertext, int shift, const char *alphabet,
                   char *result, size_t result_size) {
    return caesar_encrypt(ciphertext, -shift, alphabet, result, result_size);
}

int caesar_produce_alphabet(int shift, const char *alphabet, char *result, size_t result_size) {
    if (!alphabet || !result || result_size == 0) {
        return -1;
    }
    
    size_t alphabet_len = strlen(alphabet);
    if (alphabet_len >= result_size) {
        return -1;
    }
    
    shift = shift % (int)alphabet_len;
    if (shift < 0) {
        shift += (int)alphabet_len;
    }
    
    strcpy(result, alphabet + shift);
    strncat(result, alphabet, shift);
    result[result_size - 1] = '\0';
    
    return 0;
}

