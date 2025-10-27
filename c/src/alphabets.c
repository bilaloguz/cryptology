#include "../include/cryptology/alphabets.h"
#include <string.h>
#include <ctype.h>
#include <stdio.h>

int get_alphabet(const char* language, bool include_digits, char* result, size_t result_size) {
    if (!language || !result || result_size == 0) return -1;
    
    if (strcmp(language, "turkish") == 0) {
        if (include_digits) {
            if (result_size < strlen(TURKISH_WITH_DIGITS) + 1) return -1;
            strcpy(result, TURKISH_WITH_DIGITS);
        } else {
            if (result_size < strlen(TURKISH_ALPHABET) + 1) return -1;
            strcpy(result, TURKISH_ALPHABET);
        }
    } else {  // english
        if (include_digits) {
            if (result_size < strlen(ENGLISH_WITH_DIGITS) + 1) return -1;
            strcpy(result, ENGLISH_WITH_DIGITS);
        } else {
            if (result_size < strlen(ENGLISH_ALPHABET) + 1) return -1;
            strcpy(result, ENGLISH_ALPHABET);
        }
    }
    
    return 0;
}

int normalize_text(const char* text, char* result, size_t result_size) {
    if (!text || !result || result_size == 0) return -1;
    
    size_t len = strlen(text);
    if (len >= result_size) return -1;
    
    for (size_t i = 0; i < len; i++) {
        result[i] = tolower(text[i]);
    }
    result[len] = '\0';
    
    return 0;
}

bool validate_alphabet(const char* alphabet) {
    if (!alphabet) return false;
    
    size_t len = strlen(alphabet);
    int seen[256] = {0};
    
    for (size_t i = 0; i < len; i++) {
        unsigned char c = (unsigned char)alphabet[i];
        if (seen[c]) {
            return false;  // Duplicate found
        }
        seen[c] = 1;
    }
    
    return true;
}

size_t get_alphabet_length(const char* alphabet) {
    if (!alphabet) return 0;
    
    // For now, return string length
    // TODO: Implement proper UTF-8 character counting
    return strlen(alphabet);
}
