/**
 * @file trifid.c
 * @brief Trifid Cipher implementation with custom alphabet support
 */

#include "cryptology/classical/substitution/fractionated/trifid.h"
#include "cryptology/classical/substitution/polygraphic/alphabet_utils.h"
#include <string.h>
#include <ctype.h>
#include <stdbool.h>
#include <math.h>
#include <stdlib.h>

#define MAX_KEY_SIZE 256
#define CUBE_SIZE 3
#define DEFAULT_ALPHABET "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

static int find_char_in_cube(char cube[CUBE_SIZE][CUBE_SIZE][CUBE_SIZE], char c, int *layer, int *row, int *col) {
    for (int l = 0; l < CUBE_SIZE; l++) {
        for (int r = 0; r < CUBE_SIZE; r++) {
            for (int c_idx = 0; c_idx < CUBE_SIZE; c_idx++) {
                if (cube[l][r][c_idx] == c) {
                    *layer = l;
                    *row = r;
                    *col = c_idx;
                    return 0;
                }
            }
        }
    }
    return -1;
}

static int create_trifid_cube(const char *key, const char *alphabet, char cube[CUBE_SIZE][CUBE_SIZE][CUBE_SIZE]) {
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
        
        // For Trifid, we need exactly 27 characters (3x3x3)
        if (strlen(processed_alphabet) > 27) {
            processed_alphabet[27] = '\0';  // Truncate to 27
        } else if (strlen(processed_alphabet) < 27) {
            // Pad with X
            int len = strlen(processed_alphabet);
            for (int i = len; i < 27; i++) {
                processed_alphabet[i] = 'X';
            }
            processed_alphabet[27] = '\0';
        }
    } else {
        // Standard English alphabet (I and J combined, 26 letters + 1 padding)
        strcpy(processed_alphabet, "ABCDEFGHIKLMNOPQRSTUVWXYZ");  // 25 letters
        strcat(processed_alphabet, "X");  // Pad to 26
        strcat(processed_alphabet, "X");  // Pad to 27
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
    
    // Ensure we have exactly 27 characters
    if (strlen(key_clean) > 27) {
        key_clean[27] = '\0';
    } else if (strlen(key_clean) < 27) {
        // Pad with X
        int len = strlen(key_clean);
        for (int i = len; i < 27; i++) {
            key_clean[i] = 'X';
        }
        key_clean[27] = '\0';
    }
    
    // Create 3x3x3 cube
    for (int layer = 0; layer < CUBE_SIZE; layer++) {
        for (int row = 0; row < CUBE_SIZE; row++) {
            for (int col = 0; col < CUBE_SIZE; col++) {
                int index = layer * 9 + row * 3 + col;
                if (index < (int)strlen(key_clean)) {
                    cube[layer][row][col] = key_clean[index];
                } else {
                    cube[layer][row][col] = 'X';  // Padding
                }
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

int trifid_encrypt(const char *plaintext, const char *key, 
                   char *result, size_t result_size) {
    return trifid_encrypt_with_alphabet(plaintext, key, DEFAULT_ALPHABET, result, result_size);
}

int trifid_decrypt(const char *ciphertext, const char *key,
                  char *result, size_t result_size) {
    return trifid_decrypt_with_alphabet(ciphertext, key, DEFAULT_ALPHABET, result, result_size);
}

int trifid_encrypt_with_alphabet(const char *plaintext, const char *key, const char *alphabet,
                                 char *result, size_t result_size) {
    if (!plaintext || !key || !result || result_size == 0) {
        return -1;
    }
    
    char cube[CUBE_SIZE][CUBE_SIZE][CUBE_SIZE];
    
    if (create_trifid_cube(key, alphabet, cube) != 0) {
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
    int *layers = malloc(prepared_len * sizeof(int));
    int *rows = malloc(prepared_len * sizeof(int));
    int *cols = malloc(prepared_len * sizeof(int));
    
    if (!layers || !rows || !cols) {
        free(layers);
        free(rows);
        free(cols);
        return -1;
    }
    
    int coord_count = 0;
    for (size_t i = 0; i < prepared_len; i++) {
        int layer, row, col;
        if (find_char_in_cube(cube, prepared_text[i], &layer, &row, &col) == 0) {
            layers[coord_count] = layer;
            rows[coord_count] = row;
            cols[coord_count] = col;
            coord_count++;
        }
    }
    
    if (coord_count == 0) {
        free(layers);
        free(rows);
        free(cols);
        result[0] = '\0';
        return 0;
    }
    
    // Fractionation: write all layers, then all rows, then all columns
    int *fractionated = malloc(coord_count * 3 * sizeof(int));
    if (!fractionated) {
        free(layers);
        free(rows);
        free(cols);
        return -1;
    }
    
    for (int i = 0; i < coord_count; i++) {
        fractionated[i] = layers[i];
        fractionated[coord_count + i] = rows[i];
        fractionated[coord_count * 2 + i] = cols[i];
    }
    
    // Read triplets of coordinates to get new letters
    size_t result_pos = 0;
    for (int i = 0; i < coord_count * 3 && result_pos < result_size - 1; i += 3) {
        if (i + 2 < coord_count * 3) {
            int layer = fractionated[i];
            int row = fractionated[i + 1];
            int col = fractionated[i + 2];
            if (layer < CUBE_SIZE && row < CUBE_SIZE && col < CUBE_SIZE) {
                result[result_pos++] = cube[layer][row][col];
            }
        }
    }
    
    result[result_pos] = '\0';
    
    free(layers);
    free(rows);
    free(cols);
    free(fractionated);
    
    return 0;
}

int trifid_decrypt_with_alphabet(const char *ciphertext, const char *key, const char *alphabet,
                                 char *result, size_t result_size) {
    if (!ciphertext || !key || !result || result_size == 0) {
        return -1;
    }
    
    char cube[CUBE_SIZE][CUBE_SIZE][CUBE_SIZE];
    
    if (create_trifid_cube(key, alphabet, cube) != 0) {
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
    int *coords = malloc(prepared_len * 3 * sizeof(int));
    if (!coords) {
        return -1;
    }
    
    int coord_count = 0;
    for (size_t i = 0; i < prepared_len; i++) {
        int layer, row, col;
        if (find_char_in_cube(cube, prepared_text[i], &layer, &row, &col) == 0) {
            coords[coord_count * 3] = layer;
            coords[coord_count * 3 + 1] = row;
            coords[coord_count * 3 + 2] = col;
            coord_count++;
        }
    }
    
    if (coord_count == 0) {
        free(coords);
        result[0] = '\0';
        return 0;
    }
    
    // Defractionation: separate layers, rows, and columns
    int *layers = malloc(coord_count * sizeof(int));
    int *rows = malloc(coord_count * sizeof(int));
    int *cols = malloc(coord_count * sizeof(int));
    
    if (!layers || !rows || !cols) {
        free(coords);
        free(layers);
        free(rows);
        free(cols);
        return -1;
    }
    
    for (int i = 0; i < coord_count; i++) {
        layers[i] = coords[i * 3];
        rows[i] = coords[i * 3 + 1];
        cols[i] = coords[i * 3 + 2];
    }
    
    // Interleave layers, rows, and columns
    size_t result_pos = 0;
    for (int i = 0; i < coord_count && result_pos < result_size - 1; i++) {
        int layer = layers[i];
        int row = rows[i];
        int col = cols[i];
        if (layer < CUBE_SIZE && row < CUBE_SIZE && col < CUBE_SIZE) {
            result[result_pos++] = cube[layer][row][col];
        }
    }
    
    result[result_pos] = '\0';
    
    free(coords);
    free(layers);
    free(rows);
    free(cols);
    
    return 0;
}
