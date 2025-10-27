/**
 * @file monoalphabetic_squares.c
 * @brief Implementation of shared utilities for generating Polybius squares using monoalphabetic cipher transformations
 */

#include "../../../../include/cryptology/classical/substitution/polygraphic/monoalphabetic_squares.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX_ALPHABET_SIZE 64
#define MAX_SQUARE_SIZE 36
#define MAX_SQUARE_LINES 6

// Helper function to calculate GCD
static int gcd(int x, int y) {
    while (y) {
        int temp = y;
        y = x % y;
        x = temp;
    }
    return x;
}

// Helper function to convert string to uppercase
static void to_upper_string(char *str) {
    for (int i = 0; str[i]; i++) {
        str[i] = toupper(str[i]);
    }
}

// Helper function to remove duplicates from keyword while preserving order
static void remove_duplicates(const char *keyword, char *result) {
    int seen[256] = {0};
    int result_idx = 0;
    
    for (int i = 0; keyword[i]; i++) {
        char c = toupper(keyword[i]);
        if (isalpha(c) && !seen[c]) {
            result[result_idx++] = c;
            seen[c] = 1;
        }
    }
    result[result_idx] = '\0';
}

int create_caesar_alphabet(const char *alphabet, int shift, char *result, size_t result_size) {
    if (!alphabet || !result || result_size < MAX_ALPHABET_SIZE) {
        return -1;
    }
    
    char alphabet_upper[MAX_ALPHABET_SIZE];
    strncpy(alphabet_upper, alphabet, MAX_ALPHABET_SIZE - 1);
    alphabet_upper[MAX_ALPHABET_SIZE - 1] = '\0';
    to_upper_string(alphabet_upper);
    
    int result_idx = 0;
    for (int i = 0; alphabet_upper[i] && result_idx < (int)result_size - 1; i++) {
        if (isalpha(alphabet_upper[i])) {
            // Apply Caesar shift
            char shifted_char = ((alphabet_upper[i] - 'A' + shift) % 26) + 'A';
            result[result_idx++] = shifted_char;
        }
    }
    result[result_idx] = '\0';
    
    return 0;
}

int create_atbash_alphabet(const char *alphabet, char *result, size_t result_size) {
    if (!alphabet || !result || result_size < MAX_ALPHABET_SIZE) {
        return -1;
    }
    
    char alphabet_upper[MAX_ALPHABET_SIZE];
    strncpy(alphabet_upper, alphabet, MAX_ALPHABET_SIZE - 1);
    alphabet_upper[MAX_ALPHABET_SIZE - 1] = '\0';
    to_upper_string(alphabet_upper);
    
    int result_idx = 0;
    for (int i = 0; alphabet_upper[i] && result_idx < (int)result_size - 1; i++) {
        if (isalpha(alphabet_upper[i])) {
            // Apply Atbash reversal
            char reversed_char = 'Z' - (alphabet_upper[i] - 'A');
            result[result_idx++] = reversed_char;
        }
    }
    result[result_idx] = '\0';
    
    return 0;
}

int create_affine_alphabet(const char *alphabet, int a, int b, char *result, size_t result_size) {
    if (!alphabet || !result || result_size < MAX_ALPHABET_SIZE) {
        return -1;
    }
    
    char alphabet_upper[MAX_ALPHABET_SIZE];
    strncpy(alphabet_upper, alphabet, MAX_ALPHABET_SIZE - 1);
    alphabet_upper[MAX_ALPHABET_SIZE - 1] = '\0';
    to_upper_string(alphabet_upper);
    
    int alphabet_len = strlen(alphabet_upper);
    
    // Check that a is coprime with alphabet length
    if (gcd(a, alphabet_len) != 1) {
        return -1; // Invalid parameters
    }
    
    int result_idx = 0;
    for (int i = 0; alphabet_upper[i] && result_idx < (int)result_size - 1; i++) {
        if (isalpha(alphabet_upper[i])) {
            // Apply Affine transformation: E(x) = (ax + b) mod m
            int x = alphabet_upper[i] - 'A';
            int encrypted_pos = (a * x + b) % alphabet_len;
            result[result_idx++] = alphabet_upper[encrypted_pos];
        }
    }
    result[result_idx] = '\0';
    
    return 0;
}

int create_keyword_alphabet(const char *alphabet, const char *keyword, char *result, size_t result_size) {
    if (!alphabet || !keyword || !result || result_size < MAX_ALPHABET_SIZE) {
        return -1;
    }
    
    char alphabet_upper[MAX_ALPHABET_SIZE];
    strncpy(alphabet_upper, alphabet, MAX_ALPHABET_SIZE - 1);
    alphabet_upper[MAX_ALPHABET_SIZE - 1] = '\0';
    to_upper_string(alphabet_upper);
    
    char keyword_unique[MAX_ALPHABET_SIZE];
    remove_duplicates(keyword, keyword_unique);
    
    // Add remaining alphabet letters
    int seen[256] = {0};
    int result_idx = 0;
    
    // Add keyword letters first
    for (int i = 0; keyword_unique[i] && result_idx < (int)result_size - 1; i++) {
        result[result_idx++] = keyword_unique[i];
        seen[keyword_unique[i]] = 1;
    }
    
    // Add remaining alphabet letters
    for (int i = 0; alphabet_upper[i] && result_idx < (int)result_size - 1; i++) {
        if (!seen[alphabet_upper[i]]) {
            result[result_idx++] = alphabet_upper[i];
        }
    }
    result[result_idx] = '\0';
    
    return 0;
}

int alphabet_to_square(const char *transformed_alphabet, const char *original_alphabet, char *result, size_t result_size) {
    if (!transformed_alphabet || !original_alphabet || !result || result_size < MAX_SQUARE_SIZE) {
        return -1;
    }
    
    char alphabet_copy[MAX_ALPHABET_SIZE];
    strncpy(alphabet_copy, transformed_alphabet, MAX_ALPHABET_SIZE - 1);
    alphabet_copy[MAX_ALPHABET_SIZE - 1] = '\0';
    
    char original_copy[MAX_ALPHABET_SIZE];
    strncpy(original_copy, original_alphabet, MAX_ALPHABET_SIZE - 1);
    original_copy[MAX_ALPHABET_SIZE - 1] = '\0';
    to_upper_string(original_copy);
    
    // Handle I=J combination for English
    if (strcmp(original_copy, "ABCDEFGHIJKLMNOPQRSTUVWXYZ") == 0) {
        for (int i = 0; alphabet_copy[i]; i++) {
            if (alphabet_copy[i] == 'J') {
                alphabet_copy[i] = 'I';
            }
        }
    }
    
    // Determine square size based on original alphabet
    int size;
    if (strcmp(original_copy, "ABCDEFGHIJKLMNOPQRSTUVWXYZ") == 0) {
        size = 5; // English uses 5x5 (25 letters with I=J)
    } else if (strcmp(original_copy, "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ") == 0) {
        size = 6; // Turkish uses 6x6 (29 letters)
    } else {
        size = (strlen(alphabet_copy) <= 25) ? 5 : 6;
    }
    
    // Pad if needed
    int alphabet_len = strlen(alphabet_copy);
    while (alphabet_len < size * size) {
        alphabet_copy[alphabet_len++] = alphabet_copy[0];
    }
    alphabet_copy[alphabet_len] = '\0';
    
    // Create square
    int result_idx = 0;
    for (int i = 0; i < size && result_idx < (int)result_size - 1; i++) {
        for (int j = 0; j < size && result_idx < (int)result_size - 1; j++) {
            result[result_idx++] = alphabet_copy[i * size + j];
        }
        if (i < size - 1 && result_idx < (int)result_size - 1) {
            result[result_idx++] = '\n';
        }
    }
    result[result_idx] = '\0';
    
    return 0;
}

int create_monoalphabetic_square(
    const char *square_type,
    const char *alphabet,
    const char *mono_params,
    char *result,
    size_t result_size
) {
    if (!square_type || !result || result_size < MAX_SQUARE_SIZE) {
        return -1;
    }
    
    const char *default_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
    const char *use_alphabet = alphabet ? alphabet : default_alphabet;
    
    char transformed_alphabet[MAX_ALPHABET_SIZE];
    
    if (strcmp(square_type, "caesar") == 0) {
        // Parse shift from mono_params (simplified - assumes JSON format)
        int shift = 3; // Default shift
        if (mono_params && strstr(mono_params, "shift")) {
            // Simple parsing - look for "shift":number
            const char *shift_start = strstr(mono_params, "shift");
            if (shift_start) {
                const char *colon = strchr(shift_start, ':');
                if (colon) {
                    shift = atoi(colon + 1);
                }
            }
        }
        
        if (create_caesar_alphabet(use_alphabet, shift, transformed_alphabet, sizeof(transformed_alphabet)) != 0) {
            return -1;
        }
        
    } else if (strcmp(square_type, "atbash") == 0) {
        if (create_atbash_alphabet(use_alphabet, transformed_alphabet, sizeof(transformed_alphabet)) != 0) {
            return -1;
        }
        
    } else if (strcmp(square_type, "affine") == 0) {
        // Parse a and b from mono_params (simplified - assumes JSON format)
        int a = 1, b = 0; // Default values
        if (mono_params) {
            const char *a_start = strstr(mono_params, "a");
            if (a_start) {
                const char *colon = strchr(a_start, ':');
                if (colon) {
                    a = atoi(colon + 1);
                }
            }
            
            const char *b_start = strstr(mono_params, "b");
            if (b_start) {
                const char *colon = strchr(b_start, ':');
                if (colon) {
                    b = atoi(colon + 1);
                }
            }
        }
        
        if (create_affine_alphabet(use_alphabet, a, b, transformed_alphabet, sizeof(transformed_alphabet)) != 0) {
            return -1;
        }
        
    } else if (strcmp(square_type, "keyword") == 0) {
        const char *keyword = "SECRET"; // Default keyword
        if (mono_params && strstr(mono_params, "keyword")) {
            // Simple parsing - look for "keyword":"value"
            const char *keyword_start = strstr(mono_params, "keyword");
            if (keyword_start) {
                const char *colon = strchr(keyword_start, ':');
                if (colon) {
                    const char *quote = strchr(colon, '"');
                    if (quote) {
                        const char *end_quote = strchr(quote + 1, '"');
                        if (end_quote) {
                            // Extract keyword (simplified)
                            keyword = "SECRET"; // For now, use default
                        }
                    }
                }
            }
        }
        
        if (create_keyword_alphabet(use_alphabet, keyword, transformed_alphabet, sizeof(transformed_alphabet)) != 0) {
            return -1;
        }
        
    } else {
        return -1; // Invalid square type
    }
    
    // Convert transformed alphabet to Polybius square
    return alphabet_to_square(transformed_alphabet, use_alphabet, result, result_size);
}

int get_available_monoalphabetic_types(char *types, size_t types_size) {
    if (!types || types_size < 32) {
        return -1;
    }
    
    strncpy(types, "caesar,atbash,affine,keyword", types_size - 1);
    types[types_size - 1] = '\0';
    
    return 0;
}

int validate_mono_params(const char *square_type, const char *mono_params) {
    if (!square_type) {
        return 0;
    }
    
    if (strcmp(square_type, "caesar") == 0) {
        return (mono_params && strstr(mono_params, "shift")) ? 1 : 0;
    } else if (strcmp(square_type, "atbash") == 0) {
        return 1; // No parameters needed
    } else if (strcmp(square_type, "affine") == 0) {
        return (mono_params && strstr(mono_params, "a") && strstr(mono_params, "b")) ? 1 : 0;
    } else if (strcmp(square_type, "keyword") == 0) {
        return (mono_params && strstr(mono_params, "keyword")) ? 1 : 0;
    }
    
    return 0;
}
