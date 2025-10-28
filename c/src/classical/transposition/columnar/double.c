#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "cryptology/classical/transposition/columnar/double.h"
#include "cryptology/classical/transposition/columnar/single.h"

#define MAX_BUFFER_SIZE 2048

int double_columnar_encrypt(const char *plaintext, const char *keyword1, 
                            const char *keyword2, char *output, size_t max_len) {
    if (!plaintext || !keyword1 || !output || max_len == 0) {
        return -1;
    }
    
    // If no second keyword, use the first one
    const char *key2 = keyword2 ? keyword2 : keyword1;
    
    // Temporary buffer for first pass
    char first_pass[MAX_BUFFER_SIZE];
    
    // Apply first transposition
    if (single_columnar_encrypt(plaintext, keyword1, first_pass, MAX_BUFFER_SIZE) != 0) {
        return -1;
    }
    
    // Apply second transposition
    if (single_columnar_encrypt(first_pass, key2, output, max_len) != 0) {
        return -1;
    }
    
    return 0;
}

int double_columnar_decrypt(const char *ciphertext, const char *keyword1, 
                            const char *keyword2, char *output, size_t max_len) {
    if (!ciphertext || !keyword1 || !output || max_len == 0) {
        return -1;
    }
    
    // If no second keyword, use the first one
    const char *key2 = keyword2 ? keyword2 : keyword1;
    
    // Temporary buffer for first pass
    char first_pass[MAX_BUFFER_SIZE];
    
    // Decrypt in reverse order (second transposition first)
    if (single_columnar_decrypt(ciphertext, key2, first_pass, MAX_BUFFER_SIZE) != 0) {
        return -1;
    }
    
    // Decrypt first transposition
    if (single_columnar_decrypt(first_pass, keyword1, output, max_len) != 0) {
        return -1;
    }
    
    return 0;
}

