/**
 * @file bifid.c
 * @brief Bifid Cipher implementation with custom alphabet support
 */

#include "cryptology/classical/substitution/fractionated/bifid.h"
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

static int create_polybius_square(const char *key, const char *alphabet, char square[MAX_SQUARE_SIZE][MAX_SQUARE_SIZE], int *square_size) {
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
    
    output[output_pos] = '\0';
    return 0;
}

int bifid_encrypt(const char *plaintext, const char *key, 
                  char *result, size_t result_size) {
    return bifid_encrypt_with_alphabet(plaintext, key, DEFAULT_ALPHABET, result, result_size);
}

int bifid_decrypt(const char *ciphertext, const char *key,
                  char *result, size_t result_size) {
    return bifid_decrypt_with_alphabet(ciphertext, key, DEFAULT_ALPHABET, result, result_size);
}

int bifid_encrypt_with_alphabet(const char *plaintext, const char *key, const char *alphabet,
                                char *result, size_t result_size) {
    if (!plaintext || !key || !result || result_size == 0) {
        return -1;
    }
    
    char square[MAX_SQUARE_SIZE][MAX_SQUARE_SIZE];
    int square_size;
    
    if (create_polybius_square(key, alphabet, square, &square_size) != 0) {
        return -1;
    }
    
    char prepared_text[MAX_KEY_SIZE];
    if (prepare_text(plaintext, alphabet, prepared_text, sizeof(prepared_text)) != 0) {
        return -1;
    }
    
    size_t prepared_len = strlen(prepared_text);
    if (prepared_len == 0) {
        result[0] = '\0';
        return 0;
    }
    
    // Convert each letter to coordinates
    int *rows = malloc(prepared_len * sizeof(int));
    int *cols = malloc(prepared_len * sizeof(int));
    
    if (!rows || !cols) {
        free(rows);
        free(cols);
        return -1;
    }
    
    int coord_count = 0;
    for (size_t i = 0; i < prepared_len; i++) {
        int row, col;
        if (find_char_in_square(square, square_size, prepared_text[i], &row, &col) == 0) {
            rows[coord_count] = row;
            cols[coord_count] = col;
            coord_count++;
        }
    }
    
    if (coord_count == 0) {
        free(rows);
        free(cols);
        result[0] = '\0';
        return 0;
    }
    
    // Fractionation: write all rows, then all columns
    int *fractionated = malloc(coord_count * 2 * sizeof(int));
    if (!fractionated) {
        free(rows);
        free(cols);
        return -1;
    }
    
    for (int i = 0; i < coord_count; i++) {
        fractionated[i] = rows[i];
        fractionated[coord_count + i] = cols[i];
    }
    
    // Read pairs of coordinates to get new letters
    size_t result_pos = 0;
    for (int i = 0; i < coord_count * 2 && result_pos < result_size - 1; i += 2) {
        if (i + 1 < coord_count * 2) {
            int row = fractionated[i];
            int col = fractionated[i + 1];
            if (row < square_size && col < square_size) {
                result[result_pos++] = square[row][col];
            }
        }
    }
    
    result[result_pos] = '\0';
    
    free(rows);
    free(cols);
    free(fractionated);
    
    return 0;
}

int bifid_decrypt_with_alphabet(const char *ciphertext, const char *key, const char *alphabet,
                                char *result, size_t result_size) {
    if (!ciphertext || !key || !result || result_size == 0) {
        return -1;
    }
    
    char square[MAX_SQUARE_SIZE][MAX_SQUARE_SIZE];
    int square_size;
    
    if (create_polybius_square(key, alphabet, square, &square_size) != 0) {
        return -1;
    }
    
    char prepared_text[MAX_KEY_SIZE];
    if (prepare_text(ciphertext, alphabet, prepared_text, sizeof(prepared_text)) != 0) {
        return -1;
    }
    
    size_t prepared_len = strlen(prepared_text);
    if (prepared_len == 0) {
        result[0] = '\0';
        return 0;
    }
    
    // Convert each letter to coordinates
    int *coords = malloc(prepared_len * 2 * sizeof(int));
    if (!coords) {
        return -1;
    }
    
    int coord_count = 0;
    for (size_t i = 0; i < prepared_len; i++) {
        int row, col;
        if (find_char_in_square(square, square_size, prepared_text[i], &row, &col) == 0) {
            coords[coord_count * 2] = row;
            coords[coord_count * 2 + 1] = col;
            coord_count++;
        }
    }
    
    if (coord_count == 0) {
        free(coords);
        result[0] = '\0';
        return 0;
    }
    
    // Defractionation: separate rows and columns
    int *rows = malloc(coord_count * sizeof(int));
    int *cols = malloc(coord_count * sizeof(int));
    
    if (!rows || !cols) {
        free(coords);
        free(rows);
        free(cols);
        return -1;
    }
    
    for (int i = 0; i < coord_count; i++) {
        rows[i] = coords[i * 2];
        cols[i] = coords[i * 2 + 1];
    }
    
    // Interleave rows and columns
    size_t result_pos = 0;
    for (int i = 0; i < coord_count && result_pos < result_size - 1; i++) {
        int row = rows[i];
        int col = cols[i];
        if (row < square_size && col < square_size) {
            result[result_pos++] = square[row][col];
        }
    }
    
    result[result_pos] = '\0';
    
    free(coords);
    free(rows);
    free(cols);
    
    return 0;
}
