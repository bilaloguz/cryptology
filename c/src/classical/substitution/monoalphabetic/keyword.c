/**
 * @file keyword.c
 * @brief Keyword Cipher implementation
 */

#include "cryptology/classical/substitution/monoalphabetic/keyword.h"
#include <string.h>
#include <ctype.h>
#include <stdbool.h>

#define DEFAULT_ALPHABET "abcdefghijklmnopqrstuvwxyz"
#define MAX_ALPHABET_SIZE 256

static int find_char_in_alphabet(char c, const char *alphabet) {
    const char *pos = strchr(alphabet, c);
    return pos ? (int)(pos - alphabet) : -1;
}

static int create_cipher_alphabet(const char *keyword, const char *alphabet,
                                  char *cipher_alphabet, size_t cipher_size) {
    if (!keyword || !alphabet || !cipher_alphabet) {
        return -1;
    }
    
    size_t alphabet_len = strlen(alphabet);
    if (alphabet_len >= cipher_size) {
        return -1;
    }
    
    bool seen[MAX_ALPHABET_SIZE] = {false};
    size_t cipher_pos = 0;
    
    // Add keyword letters (removing duplicates)
    for (size_t i = 0; keyword[i] != '\0'; i++) {
        char c = tolower((unsigned char)keyword[i]);
        int pos = find_char_in_alphabet(c, alphabet);
        
        if (pos != -1 && !seen[pos]) {
            cipher_alphabet[cipher_pos++] = c;
            seen[pos] = true;
        }
    }
    
    // Add remaining alphabet letters
    for (size_t i = 0; i < alphabet_len; i++) {
        if (!seen[i]) {
            cipher_alphabet[cipher_pos++] = alphabet[i];
        }
    }
    
    cipher_alphabet[cipher_pos] = '\0';
    return 0;
}

int keyword_encrypt(const char *plaintext, const char *keyword, const char *alphabet,
                    char *result, size_t result_size) {
    if (!plaintext || !keyword || !result || result_size == 0) {
        return -1;
    }
    
    if (!alphabet) {
        alphabet = DEFAULT_ALPHABET;
    }
    
    char cipher_alphabet[MAX_ALPHABET_SIZE];
    if (create_cipher_alphabet(keyword, alphabet, cipher_alphabet, MAX_ALPHABET_SIZE) != 0) {
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
            result[i] = cipher_alphabet[pos];
        } else {
            result[i] = plaintext[i];
        }
    }
    
    result[plaintext_len] = '\0';
    return 0;
}

int keyword_decrypt(const char *ciphertext, const char *keyword, const char *alphabet,
                    char *result, size_t result_size) {
    if (!ciphertext || !keyword || !result || result_size == 0) {
        return -1;
    }
    
    if (!alphabet) {
        alphabet = DEFAULT_ALPHABET;
    }
    
    char cipher_alphabet[MAX_ALPHABET_SIZE];
    if (create_cipher_alphabet(keyword, alphabet, cipher_alphabet, MAX_ALPHABET_SIZE) != 0) {
        return -1;
    }
    
    size_t ciphertext_len = strlen(ciphertext);
    if (ciphertext_len >= result_size) {
        return -1;
    }
    
    for (size_t i = 0; i < ciphertext_len; i++) {
        char c = tolower((unsigned char)ciphertext[i]);
        int pos = find_char_in_alphabet(c, cipher_alphabet);
        
        if (pos != -1) {
            result[i] = alphabet[pos];
        } else {
            result[i] = ciphertext[i];
        }
    }
    
    result[ciphertext_len] = '\0';
    return 0;
}

