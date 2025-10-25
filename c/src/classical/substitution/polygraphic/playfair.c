/**
 * @file playfair.c
 * @brief Playfair Cipher implementation with custom alphabet support
 */

#include "cryptology/classical/substitution/polygraphic/playfair.h"
#include "cryptology/classical/substitution/polygraphic/alphabet_utils.h"
#include <string.h>
#include <ctype.h>
#include <stdbool.h>
#include <math.h>
#include <stdlib.h>

#define MAX_KEY_SIZE 256
#define MAX_SQUARE_SIZE 10
#define DEFAULT_ALPHABET "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

static int find_char_in_square(char square[MAX_SQUARE_SIZE][MAX_SQUARE_SIZE], int square_size, char c, int *row, int *col) {
    for (int i = 0; i < square_size; i++) {
        for (int j = 0; j < square_size; j++) {
            if (square[i][j] == c) {
                *row = i;
                *col = j;
                return 0;
            }
        }
    }
    return -1;
}

static int create_key_square(const char *key, const char *alphabet, char square[MAX_SQUARE_SIZE][MAX_SQUARE_SIZE], int *square_size) {
    if (!key || !alphabet) {
        return -1;
    }
    
    // Handle custom alphabets
    char processed_alphabet[MAX_KEY_SIZE];
    if (strcmp(alphabet, DEFAULT_ALPHABET) != 0) {
        // Combine similar letters for non-English alphabets
        if (combine_similar_letters(alphabet, "auto", processed_alphabet, sizeof(processed_alphabet)) != 0) {
            return -1;
        }
        
        // Determine square size
        *square_size = get_square_size(strlen(processed_alphabet));
        if (*square_size > MAX_SQUARE_SIZE) {
            *square_size = MAX_SQUARE_SIZE;
        }
        
        // Create square-sized alphabet
        char square_alphabet[MAX_KEY_SIZE];
        if (create_square_alphabet(processed_alphabet, *square_size, square_alphabet, sizeof(square_alphabet)) != 0) {
            return -1;
        }
        strcpy(processed_alphabet, square_alphabet);
    } else {
        // Standard English alphabet (I and J combined)
        *square_size = 5;
        strcpy(processed_alphabet, "ABCDEFGHIKLMNOPQRSTUVWXYZ");  // No J, I and J are combined
    }
    
    // Remove duplicates while preserving order, convert to uppercase
    char key_clean[MAX_KEY_SIZE];
    bool seen[256] = {false};
    int pos = 0;
    
    for (size_t i = 0; key[i] != '\0' && pos < MAX_KEY_SIZE - 1; i++) {
        char c = toupper((unsigned char)key[i]);
        if (c >= 'A' && c <= 'Z' && !seen[(unsigned char)c]) {
            key_clean[pos++] = c;
            seen[(unsigned char)c] = true;
        }
    }
    key_clean[pos] = '\0';
    
    // Add remaining letters from processed alphabet
    for (size_t i = 0; processed_alphabet[i] != '\0' && pos < MAX_KEY_SIZE - 1; i++) {
        char c = toupper((unsigned char)processed_alphabet[i]);
        if (!seen[(unsigned char)c]) {
            key_clean[pos++] = c;
            seen[(unsigned char)c] = true;
        }
    }
    key_clean[pos] = '\0';
    
    // Fill square
    for (int i = 0; i < *square_size; i++) {
        for (int j = 0; j < *square_size; j++) {
            int index = i * *square_size + j;
            if (index < (int)strlen(key_clean)) {
                square[i][j] = key_clean[index];
            } else {
                square[i][j] = 'X';  // Padding
            }
        }
    }
    
    return 0;
}

static int prepare_text(const char *input, const char *alphabet, char *output, size_t output_size) {
    if (!input || !output || output_size == 0) {
        return -1;
    }
    
    size_t input_len = strlen(input);
    size_t output_pos = 0;
    
    for (size_t i = 0; i < input_len && output_pos < output_size - 1; i++) {
        char c = toupper((unsigned char)input[i]);
        if (c >= 'A' && c <= 'Z') {
            // Handle custom alphabets
            if (strcmp(alphabet, DEFAULT_ALPHABET) != 0) {
                // Apply language-specific replacements
                const char *language = detect_language(alphabet);
                if (strcmp(language, "turkish") == 0) {
                    // Turkish character replacements
                    if (c == 'Ç') c = 'C';
                    else if (c == 'Ğ') c = 'G';
                    else if (c == 'I') c = 'I';
                    else if (c == 'Ö') c = 'O';
                    else if (c == 'Ş') c = 'S';
                    else if (c == 'Ü') c = 'U';
                }
            } else {
                // Standard English: Replace J with I
                if (c == 'J') {
                    c = 'I';
                }
            }
            output[output_pos++] = c;
        }
    }
    
    // Add X padding for odd length
    if (output_pos % 2 == 1) {
        if (output_pos < output_size - 1) {
            output[output_pos++] = 'X';
        }
    }
    
    output[output_pos] = '\0';
    return 0;
}

static int encrypt_digram(char square[MAX_SQUARE_SIZE][MAX_SQUARE_SIZE], int square_size, char char1, char char2, char *result) {
    int row1, col1, row2, col2;
    
    if (find_char_in_square(square, square_size, char1, &row1, &col1) != 0 ||
        find_char_in_square(square, square_size, char2, &row2, &col2) != 0) {
        return -1;
    }
    
    // Same row: shift right (wrap around)
    if (row1 == row2) {
        int new_col1 = (col1 + 1) % square_size;
        int new_col2 = (col2 + 1) % square_size;
        result[0] = square[row1][new_col1];
        result[1] = square[row2][new_col2];
    }
    // Same column: shift down (wrap around)
    else if (col1 == col2) {
        int new_row1 = (row1 + 1) % square_size;
        int new_row2 = (row2 + 1) % square_size;
        result[0] = square[new_row1][col1];
        result[1] = square[new_row2][col2];
    }
    // Rectangle: use opposite corners
    else {
        result[0] = square[row1][col2];
        result[1] = square[row2][col1];
    }
    
    return 0;
}

static int decrypt_digram(char square[MAX_SQUARE_SIZE][MAX_SQUARE_SIZE], int square_size, char char1, char char2, char *result) {
    int row1, col1, row2, col2;
    
    if (find_char_in_square(square, square_size, char1, &row1, &col1) != 0 ||
        find_char_in_square(square, square_size, char2, &row2, &col2) != 0) {
        return -1;
    }
    
    // Same row: shift left (wrap around)
    if (row1 == row2) {
        int new_col1 = (col1 - 1 + square_size) % square_size;
        int new_col2 = (col2 - 1 + square_size) % square_size;
        result[0] = square[row1][new_col1];
        result[1] = square[row2][new_col2];
    }
    // Same column: shift up (wrap around)
    else if (col1 == col2) {
        int new_row1 = (row1 - 1 + square_size) % square_size;
        int new_row2 = (row2 - 1 + square_size) % square_size;
        result[0] = square[new_row1][col1];
        result[1] = square[new_row2][col2];
    }
    // Rectangle: use opposite corners
    else {
        result[0] = square[row1][col2];
        result[1] = square[row2][col1];
    }
    
    return 0;
}

int playfair_encrypt(const char *plaintext, const char *key, 
                     char *result, size_t result_size) {
    return playfair_encrypt_with_alphabet(plaintext, key, DEFAULT_ALPHABET, result, result_size);
}

int playfair_decrypt(const char *ciphertext, const char *key,
                     char *result, size_t result_size) {
    return playfair_decrypt_with_alphabet(ciphertext, key, DEFAULT_ALPHABET, result, result_size);
}

int playfair_encrypt_with_alphabet(const char *plaintext, const char *key, const char *alphabet,
                                   char *result, size_t result_size) {
    if (!plaintext || !key || !result || result_size == 0) {
        return -1;
    }
    
    char square[MAX_SQUARE_SIZE][MAX_SQUARE_SIZE];
    int square_size;
    
    if (create_key_square(key, alphabet, square, &square_size) != 0) {
        return -1;
    }
    
    char prepared_text[MAX_KEY_SIZE];
    if (prepare_text(plaintext, alphabet, prepared_text, sizeof(prepared_text)) != 0) {
        return -1;
    }
    
    size_t prepared_len = strlen(prepared_text);
    if (prepared_len >= result_size) {
        return -1;
    }
    
    for (size_t i = 0; i < prepared_len; i += 2) {
        if (i + 1 < prepared_len) {
            char digram_result[2];
            if (encrypt_digram(square, square_size, prepared_text[i], prepared_text[i + 1], digram_result) != 0) {
                return -1;
            }
            result[i] = digram_result[0];
            result[i + 1] = digram_result[1];
        }
    }
    
    result[prepared_len] = '\0';
    return 0;
}

int playfair_decrypt_with_alphabet(const char *ciphertext, const char *key, const char *alphabet,
                                   char *result, size_t result_size) {
    if (!ciphertext || !key || !result || result_size == 0) {
        return -1;
    }
    
    char square[MAX_SQUARE_SIZE][MAX_SQUARE_SIZE];
    int square_size;
    
    if (create_key_square(key, alphabet, square, &square_size) != 0) {
        return -1;
    }
    
    char prepared_text[MAX_KEY_SIZE];
    if (prepare_text(ciphertext, alphabet, prepared_text, sizeof(prepared_text)) != 0) {
        return -1;
    }
    
    size_t prepared_len = strlen(prepared_text);
    if (prepared_len >= result_size) {
        return -1;
    }
    
    for (size_t i = 0; i < prepared_len; i += 2) {
        if (i + 1 < prepared_len) {
            char digram_result[2];
            if (decrypt_digram(square, square_size, prepared_text[i], prepared_text[i + 1], digram_result) != 0) {
                return -1;
            }
            result[i] = digram_result[0];
            result[i + 1] = digram_result[1];
        }
    }
    
    result[prepared_len] = '\0';
    return 0;
}